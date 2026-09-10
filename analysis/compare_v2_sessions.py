"""Frozen v2 program-level analysis. No network access; synthetic inputs require opt-in."""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from analysis.metrics import evaluate_record
from analysis.run_analysis import load_session_records
from analysis.statistics import clustered_bootstrap_delta, exact_mcnemar, exam_comparison
from experiments.health import assert_session_health
from experiments.models import load_manifest
from experiments.parsing import ResponseParseError, parse_ranking
from experiments.prompts import build_prompt_pair, sha256_text, PRIOR_OPEN, PRIOR_CLOSE
from experiments.run_pilot import load_prior_map, execution_key_for
from experiments.safety import SafetyViolation, assert_condition_balance, assert_unique_execution_keys
from experiments.storage import file_sha256, path_sha256, write_json_new

ROOT = Path(__file__).resolve().parents[1]
SEED = 20260908
ITERATIONS = 10000
ASSETS = {
    'system_prompt': ROOT / 'pilot/v2/prompts/system_v2.txt',
    'user_template': ROOT / 'pilot/prompts/control.txt',
}
PRIOR_PATHS = [ROOT / 'pilot/v2/generic_placebo_prior.json', ROOT / 'pilot/pattern_priors.json']
INVARIANTS = ('manifest_hash', 'system_prompt_hash', 'user_template_hash', 'provider',
              'model', 'temperature', 'max_tokens', 'timeout', 'base_url', 'repetitions',
              'condition_order', 'engineering_only', 'program_input_hashes', 'model_freeze_hash')


def require(condition, message):
    if not condition:
        raise SafetyViolation(message)


def resolve(path):
    p = Path(path)
    return p if p.is_absolute() else ROOT / p


def input_hashes(manifest):
    return {p.program_id: {
        'buggy_source': path_sha256(p.buggy_source_path),
        'fixed_source': path_sha256(p.fixed_source_path),
        'tests': path_sha256(p.tests_path),
        'problem_context': path_sha256(p.problem_context_path) if p.problem_context_path else None,
    } for p in manifest.programs}


def validate_sessions(generic, pattern, manifest_path, allow_mock=False):
    manifest = load_manifest(manifest_path)
    programs = {p.program_id: p for p in manifest.included}
    sessions = [json.loads((d / 'session_manifest.json').read_text()) for d in (generic, pattern)]
    g, p = sessions
    for field in INVARIANTS:
        require(field in g and field in p and g[field] == p[field], f'cross-session {field} mismatch')
    require(type(g['engineering_only']) is bool, 'engineering_only must be explicit boolean')
    engineering = g['engineering_only']
    require(not engineering or allow_mock, 'engineering-only inputs require --allow-mock-analysis')
    require(g['provider'] != 'mock' or engineering, 'mock cannot masquerade as science')
    require(g['experiment_name'] != p['experiment_name'], 'sessions need different experiment names')
    require(g['session_id'] != p['session_id'], 'sessions need distinct session IDs')
    require(g['manifest_hash'] == file_sha256(manifest_path), 'sample freeze manifest mismatch')
    require(g['program_input_hashes'] == input_hashes(manifest), 'frozen program inputs changed')
    require(g['repetitions'] == 5, 'v2 requires exactly five repetitions')
    require(g['condition_order'] == 'counterbalanced', 'v2 requires counterbalanced order')
    require(g['temperature'] == 0 and g['max_tokens'] >= 1024 and g['timeout'] > 0,
            'v2 frozen settings violated')
    if not engineering:
        require(len(programs) == 30 and manifest.dataset_name == 'ConDefects-Python', 'scientific sample must be 30 ConDefects-Python programs')
        require(bool(g['model_freeze_hash']), 'missing model freeze identifier')
        require(len({x.task_id for x in programs.values()}) == len(programs), 'task IDs must be unique')
        for x in programs.values():
            require(not x.program_id.startswith('smoke-') and ROOT / 'data/smoke' not in x.buggy_source_path.parents,
                    'smoke data can never be scientific data')
            require(25 <= x.source_line_count <= 300 and x.exam_denominator == x.source_line_count
                    and x.loc == x.source_line_count and len(x.faulty_lines) == 1,
                    'v2 line-count/ground-truth convention violated')
    require(all(x.problem_context_path is None for x in programs.values()), 'v2 omits problem context uniformly')
    system, template = [ASSETS[key].read_text() for key in ('system_prompt', 'user_template')]
    for key, value in [('system_prompt', system), ('user_template', template)]:
        require(g[key + '_hash'] == sha256_text(value), f'frozen {key} mismatch')
    all_records, rows = [], []
    prompt_pairs = {}
    for directory, session, prior_path, treatment, control_arm, treatment_arm in zip(
        (generic, pattern), sessions, PRIOR_PATHS, ('generic_prior', 'pattern_prior'), ('A_G', 'A_P'), ('B', 'C')
    ):
        require(session['priors_hash'] == sha256_text(prior_path.read_text()), 'frozen prior file mismatch')
        require(not (directory / "VOID.json").exists(), "VOID session cannot be analyzed")
        records = load_session_records(directory)
        assert_condition_balance(records, repetitions=5, control_name='no_prior', treatment_name=treatment,
                                 expected_program_ids=set(programs))
        assert_session_health(records)
        priors = load_prior_map(prior_path)
        for record in records:
            program = programs[record.program_id]
            pair = build_prompt_pair(system, template, program, priors[program.pattern_label])
            prompt_pairs[(record.program_id, treatment_arm)] = pair
            is_treatment = record.condition == treatment
            expected_prompt = pair.treatment_user_prompt if is_treatment else pair.control_user_prompt
            expected_prior = pair.prior_hash if is_treatment else None
            for key in ('session_id', 'experiment_name', 'manifest_hash', 'system_prompt_hash', 'provider', 'model', 'temperature', 'max_tokens'):
                require(getattr(record, key) == session[key], f'record {key} mismatch')
            for key, expected in dict(task_id=program.task_id, faulty_lines=program.faulty_lines,
                source_line_count=program.source_line_count, loc=program.loc, evaluation_denominator=program.exam_denominator,
                pattern_label=program.pattern_label, difficulty=program.difficulty,
                shared_prompt_hash=pair.shared_prompt_hash, prior_hash=expected_prior,
                prompt_chars=len(system)+len(expected_prompt), prompt_tokens_estimate=(len(system)+len(expected_prompt)+3)//4).items():
                require(getattr(record, key) == expected, f'record {key} mismatch or leakage')
            key = execution_key_for(experiment_name=session['experiment_name'], manifest_hash=session['manifest_hash'],
                program=program, condition=record.condition, repetition=record.repetition, provider=record.provider,
                model=record.model, temperature=record.temperature, max_tokens=record.max_tokens,
                system_prompt_hash=record.system_prompt_hash, shared_prompt_hash=pair.shared_prompt_hash, prior_hash=expected_prior)
            require(record.execution_key == key, 'execution key mismatch')
            require(record.status in ('ok', 'parser_failure', 'provider_failure'), 'unknown run status')
            if record.raw_response_path:
                raw = json.loads(resolve(record.raw_response_path).read_text())
                # Exact reconstruction detects literal appended truth, not merely forbidden template placeholders.
                require(raw['system_prompt'] == system and raw['user_prompt'] == expected_prompt,
                        'raw prompt mismatch: delimiter, prior, or ground-truth leakage')
                require(raw.get('prompt_input_fields') == ['program_id','task_id','problem_context','numbered_buggy_source'],
                        'ground-truth input provenance violation')
                for field in ('run_id', 'execution_key', 'shared_prompt_hash', 'prior_hash', 'manifest_hash'):
                    require(raw.get(field) == getattr(record, field), f'raw {field} mismatch')
                require(raw['actual_provider'] == record.provider and raw['actual_model'] == record.model,
                        'raw model identity mismatch')
                require(raw['raw_response'] == record.raw_response, 'raw/processed response mismatch')
                if record.status == 'ok':
                    require(bool(raw['raw_response'].strip()) and raw['response_metadata'].get('finish_reason') != 'length',
                            'operationally invalid completion cannot be ok')
                if record.status != 'provider_failure':
                    try:
                        parsed = parse_ranking(raw['raw_response'], source_line_count=program.source_line_count, loc=program.exam_denominator)
                    except ResponseParseError:
                        require(record.status == 'parser_failure' and record.parsed_response is None, 'parser status mismatch')
                    else:
                        require(record.status == 'ok' and parsed == record.parsed_response, 'parsed ranking mismatch')
            else:
                require(record.status == 'provider_failure' and record.parsed_response is None,
                        'missing raw response for non-provider failure')
            arm = treatment_arm if is_treatment else control_arm
            row = evaluate_record(record)
            row.update(condition=arm, raw_response=record.raw_response,
                       ranking_length=len(record.parsed_response.ranking) if record.parsed_response else 0,
                       prompt_words=len((system + '\n' + expected_prompt).split()))
            rows.append(row)
        all_records.extend(records)
    assert_unique_execution_keys(all_records)
    require(len({r.run_id for r in all_records}) == len(all_records), 'duplicate run IDs')
    for id in programs:
        b, c = prompt_pairs[(id, 'B')], prompt_pairs[(id, 'C')]
        require(b.control_user_prompt == c.control_user_prompt, 'per-program shared prompt mismatch')
        for pair in (b, c):
            require(pair.treatment_user_prompt.count(PRIOR_OPEN) == 1 and pair.treatment_user_prompt.count(PRIOR_CLOSE) == 1,
                    'neutral delimiter must occur exactly once')
        label = programs[id].pattern_label
        btext, ctext = (load_prior_map(path)[label] for path in PRIOR_PATHS)
        items = lambda text: sum(line[:1].isdigit() for line in text.splitlines())
        require(abs(len(btext.split())-len(ctext.split())) <= 10 and items(btext) == items(ctext), 'prior length/checkpoint parity violation')
    return pd.DataFrame(rows), engineering, sessions


def aggregate(frame):
    # Assertions precede aggregation; groupby must never hide a missing repetition.
    grouped = frame.groupby(['program_id', 'condition'], sort=True)
    require((grouped.size() == 5).all(), 'five repeated measurements required per program/arm')
    result = grouped[['top1', 'top3', 'top5']].sum().ge(3).astype(int)
    result['exam'] = grouped.exam.mean()
    result['pattern_label'] = grouped.pattern_label.first()
    return result.reset_index()


def comparison(aggregated, control, treatment, metric):
    pivot = aggregated.pivot(index='program_id', columns='condition', values=metric)
    require(not pivot[[control,treatment]].isna().any().any(), 'unpaired program: cannot drop rows')
    return {'n_programs': len(pivot), 'control': control, 'treatment': treatment,
            'control_rate': float(pivot[control].mean()), 'treatment_rate': float(pivot[treatment].mean()),
            'delta': float((pivot[treatment]-pivot[control]).mean()),
            **exact_mcnemar(pivot[control].to_numpy(), pivot[treatment].to_numpy())}


def bootstrap(frame, metric):
    result = clustered_bootstrap_delta(frame, metric=metric, control_name='B', treatment_name='C', iterations=ITERATIONS, seed=SEED)
    result['unit'] = 'program; majority-of-five Top-K / mean-of-five EXAM*'
    return result


def build_report(frame, engineering):
    a = aggregate(frame)
    determinism = {}
    for arm, part in frame.groupby('condition'):
        cells = part.groupby('program_id')
        # A missing response is never a byte-identical completion.
        identical = [bool(cell.raw_response.notna().all() and cell.raw_response.nunique() == 1) for _,cell in cells]
        determinism[arm] = {'raw_byte_identical_rate': float(np.mean(identical)),
                           'top1_agreement_rate': float((cells.top1.nunique() == 1).mean())}
    parser = {arm: {'total': len(part), 'parser_failures': int((part.status=='parser_failure').sum()),
                    'parser_failure_rate': float((part.status=='parser_failure').mean()),
                    'provider_failures': int((part.status=='provider_failure').sum())}
              for arm, part in frame.groupby('condition')}
    null = comparison(a, 'A_G', 'A_P', 'top1')
    primary = comparison(a, 'B', 'C', 'top1')
    d = primary['discordant_pairs']; b = primary['control_miss_treatment_hit']; c = primary['control_hit_treatment_miss']
    null['primary_interpretable'] = null['discordant_pairs'] < d
    null['gate'] = 'PASS' if null['primary_interpretable'] else 'UNINTERPRETABLE AT THIS SAMPLE SIZE'
    primary.update(endpoint='primary; exploratory calibration only', b=b, c=c, d=d,
                   pi_d=d/primary['n_programs'], bootstrap=bootstrap(a, 'top1'),
                   interpretation=null['gate'])
    secondary = {'label': 'secondary/descriptive, no alpha adjustment',
        'top3': {**comparison(a, 'B', 'C', 'top3'), 'bootstrap': bootstrap(a, 'top3')},
        'top5': {**comparison(a, 'B', 'C', 'top5'), 'bootstrap': bootstrap(a, 'top5')},
        'EXAM*': {**exam_comparison(a, 'B', 'C'), 'bootstrap': bootstrap(a, 'exam'),
                  'warning': 'Censored physical-line denominator; not comparable to published EXAM.'},
        'A_vs_B': {m: comparison(a, 'A_G', 'B', m) for m in ('top1','top3','top5')},
        'A_vs_C': {m: comparison(a, 'A_P', 'C', m) for m in ('top1','top3','top5')},
        'A_disclosure': 'Arm A already contains generic debugging guidance; only the prior block is absent.'}
    secondary['A_vs_B']['EXAM*'] = exam_comparison(a, 'A_G', 'B')
    secondary['A_vs_C']['EXAM*'] = exam_comparison(a, 'A_P', 'C')
    # All five tests, for all endpoints and both native within-session comparisons.
    robustness = {name: {metric: [dict(repetition=r, **comparison(frame[frame.repetition==r], control, treatment, metric))
                                  for r in range(1,6)] for metric in ('top1','top3','top5')}
                  for name, control, treatment in [('A_vs_B','A_G','B'), ('A_vs_C','A_P','C')]}
    per_class = {}
    for label, part in a.groupby('pattern_label'):
        pivot = part.pivot(index='program_id', columns='condition', values='top1')
        per_class[label] = {'n_programs': len(pivot), 'top1_C_minus_B': float((pivot.C-pivot.B).mean()), 'descriptive_only': True}
    pivot = a.pivot(index='program_id', columns='condition', values='top1')
    discordant = (pivot.B != pivot.C).to_numpy(dtype=float)
    rng = np.random.default_rng(SEED)
    draws = discordant[rng.integers(0,len(pivot),size=(ITERATIONS,len(pivot)))].mean(axis=1)
    lo, hi = np.percentile(draws,[2.5,97.5])
    psi = b/d if d else None
    sizing = {'pi_d': d/len(pivot), 'pi_d_percentile_95_ci': [float(lo),float(hi)], 'psi':psi,
              'bootstrap_iterations':ITERATIONS, 'seed':SEED,
              'caveat':'Approximation conditional on pilot psi; single model, sampled classes, single-line faults. Not confirmatory evidence.'}
    if not d or b == c:
        sizing.update(status='PILOT COULD NOT SIZE THE STUDY', N_range=None,
                      reason='No discordance or psi=0.5; approximation is undefined/unbounded.')
    else:
        nd = 7.84/(2*psi-1)**2
        sizing.update(status='EXPLORATORY APPROXIMATION', n_discordant=nd,
                      N_range=[math.ceil(nd/hi), math.ceil(nd/lo) if lo else None],
                      upper_unbounded=bool(lo==0), direction='C' if b>c else 'B',
                      null_calibration_warning=not null['primary_interpretable'])
    diagnostics = {arm: {'mean_ranking_entries_per_call':float(part.ranking_length.mean()),
        'mean_ranking_entries_parse_success_only':float(part[part.status=='ok'].ranking_length.mean()) if (part.status=='ok').any() else None,
        'mean_prompt_chars':float(part.prompt_chars.mean()), 'mean_prompt_words':float(part.prompt_words.mean()),
        'mean_prompt_tokens_estimate':float(part.prompt_tokens_estimate.mean())} for arm,part in frame.groupby('condition')}
    return {'schema_version':2, 'engineering_only':engineering, 'experimental_unit':'program',
        'n_programs':int(frame.program_id.nunique()), 'repetitions':5,
        'effective_paired_observations_per_comparison':int(frame.program_id.nunique()),
        'run_integrity':{'invariants':'PASS', 'parser_failure_policy':'count_as_failure', 'parser_diagnostics':parser, 'determinism':determinism},
        'null_calibration':null, 'primary_C_vs_B':primary, 'secondary':secondary,
        'robustness_all_five_repetitions':robustness,
        'diagnostics':{'by_arm':diagnostics, 'prior_word_tolerance':10, 'prior_parity':'PASS', 'per_class':per_class},
        'confirmatory_sizing':sizing,
        'claim_boundary':'Calibration only; a null is not evidence of absence. Apply CLAIM_BOUNDARIES_V2.md before writing scientific claims.',
        'program_aggregates':a.to_dict(orient='records')}


def run(args):
    frame, engineering, sessions = validate_sessions(args.generic_session, args.pattern_session, args.manifest, args.allow_mock_analysis)
    report = build_report(frame, engineering)
    report['provenance'] = {'sessions':sessions, 'analysis_seed':SEED, 'bootstrap_iterations':ITERATIONS}
    # All validation finishes before the first output is created; never overwrite a previous report.
    write_json_new(args.output, report)
    return report


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--generic-session',type=Path,required=True)
    p.add_argument('--pattern-session',type=Path,required=True)
    p.add_argument('--manifest',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--allow-mock-analysis',action='store_true')
    return p


def main():
    try:
        run(parser().parse_args())
    except (ValueError, OSError, KeyError) as exc:
        print(f'v2 analysis aborted: {exc}',file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == '__main__':
    main()
