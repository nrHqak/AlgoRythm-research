"""Smoke-only model freeze. This command never loads the scientific candidate frame."""
from __future__ import annotations
import argparse
import json
import secrets
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlsplit

from experiments.models import load_manifest
from experiments.prompts import build_prompt_pair
from experiments.run_pilot import make_provider, run_one, load_prior_map, utc_now, append_experiment_log
from experiments.storage import file_sha256, write_json_new
from experiments.safety import SafetyViolation
from experiments.providers.routing import add_routing_settings, add_routing_arguments

ROOT = Path(__file__).resolve().parents[1]
SMOKE = ROOT / 'data/smoke/manifest.json'
SYSTEM = ROOT / 'pilot/v2/prompts/system_v2.txt'
TEMPLATE = ROOT / 'pilot/prompts/control.txt'
PRIORS = [ROOT/'pilot/v2/generic_placebo_prior.json', ROOT/'pilot/pattern_priors.json']


def freeze_asset_paths():
    manifest = load_manifest(SMOKE)
    return [SMOKE, SYSTEM, TEMPLATE, *PRIORS,
            *(path for p in manifest.included for path in (p.buggy_source_path, p.fixed_source_path, p.tests_path))]


def validate_identity_choice(model, kind, reference, alias_risk):
    if not model.strip() or not reference.strip():
        raise SafetyViolation('exact model ID and provider model-version reference are required')
    if kind == 'pinned' and 'latest' in model.lower():
        raise SafetyViolation('latest is a moving alias, not a pinned ID')
    if kind == 'alias_only' and not alias_risk.strip():
        raise SafetyViolation('alias-only provider requires explicit accepted-risk explanation')


def assert_committed(path):
    path = path.resolve()
    try:
        relative = str(path.relative_to(ROOT))
    except ValueError as exc:
        raise SafetyViolation('freeze record must be committed inside repository') from exc
    result = subprocess.run(['git','show',f'HEAD:{relative}'],cwd=ROOT,capture_output=True)
    if result.returncode or result.stdout != path.read_bytes():
        raise SafetyViolation('freeze record must be committed unchanged before main run')


def validate_freeze(args, repetitions):
    path = getattr(args, 'model_freeze', None)
    if path is None:
        raise SafetyViolation('real v2 execution requires --model-freeze; run smoke protocol first')
    assert_committed(path)
    freeze = json.loads(path.read_text())
    if freeze.get('status') != 'PASS' or freeze.get('engineering_only') is not True:
        raise SafetyViolation('model freeze did not pass engineering smoke check')
    expected = dict(provider=args.provider_label or args.provider, provider_type=args.provider,
                    base_url=args.base_url.rstrip('/'), model=args.model, temperature=args.temperature,
                    max_tokens=args.max_tokens, timeout=args.timeout)
    reasoning_effort = getattr(args, 'reasoning_effort', None)
    if reasoning_effort is not None:
        expected['reasoning'] = {'effort': reasoning_effort}
    add_routing_settings(expected, args)
    if freeze.get('settings') != expected:
        raise SafetyViolation('model/provider/settings differ from committed freeze')
    validate_identity_choice(args.model, freeze['model_kind'], freeze['model_reference'], freeze['accepted_alias_risk'])
    if args.temperature != 0 or args.max_tokens < 1024 or repetitions != 5 or args.condition_order != 'counterbalanced':
        raise SafetyViolation('frozen v2 requires temperature 0, >=1024 tokens, 5 repetitions, counterbalanced order')
    frozen_reasoning = freeze.get('settings', {}).get('reasoning', {}).get('effort')
    if frozen_reasoning is not None and reasoning_effort != frozen_reasoning:
        raise SafetyViolation('reasoning effort differs from committed execution freeze')
    if freeze.get('echoed_models') != [args.model] or freeze.get('calls',0) < 10 or freeze.get('parse_successes') != freeze.get('calls'):
        raise SafetyViolation('freeze has insufficient or invalid smoke evidence')
    if 'openrouter_routing' in expected:
        name = expected['openrouter_routing']['expected_provider_name']
        if freeze.get('echoed_underlying_providers') != [name]:
            raise SafetyViolation('freeze lacks exact underlying provider identity evidence')
    if freeze.get('session_order') not in (['G','P'], ['P','G']):
        raise SafetyViolation('missing session-order coin flip')
    workers = getattr(args, 'workers', 1)
    frozen_workers = freeze.get('execution', {}).get('workers', 1)
    if workers != frozen_workers:
        raise SafetyViolation('worker count differs from committed execution freeze')
    asset_hashes = freeze.get('asset_hashes', {})
    if not isinstance(asset_hashes, dict) or not asset_hashes:
        raise SafetyViolation('freeze lacks immutable smoke asset hashes')
    for relative, expected_hash in asset_hashes.items():
        source = ROOT / relative
        if not source.is_file() or file_sha256(source) != expected_hash:
            raise SafetyViolation('smoke/prompt/prior changed after model freeze')
    for source in (SYSTEM, TEMPLATE, *PRIORS):
        if asset_hashes.get(str(source.relative_to(ROOT))) != file_sha256(source):
            raise SafetyViolation('freeze lacks current frozen prompt/prior evidence')
    if file_sha256(args.system_prompt) != file_sha256(SYSTEM) or file_sha256(args.user_template) != file_sha256(TEMPLATE):
        raise SafetyViolation('real v2 must use frozen v2 system and shared template')
    return freeze


def check_smoke_record(record, raw):
    if record.status != 'ok':
        raise SafetyViolation(f'smoke call failed: {record.status}/{record.error_type}')
    if not record.raw_response or not record.raw_response.strip():
        raise SafetyViolation('empty completion')
    if raw['response_metadata'].get('finish_reason') == 'length':
        raise SafetyViolation('truncated completion: raise max_tokens and repeat smoke check')
    if all(item.score == 0 for item in record.parsed_response.ranking):
        raise SafetyViolation('all-zero suspicion scores: smoke mechanical validity failed')
    # No accuracy or fault-hit criterion is evaluated here.


def run(args):
    validate_identity_choice(args.model, args.model_kind, args.model_reference, args.accepted_alias_risk)
    if args.temperature != 0 or args.max_tokens < 1024 or args.timeout <= 0:
        raise SafetyViolation('smoke requires temperature 0, max_tokens >=1024, positive timeout')
    url = urlsplit(args.base_url)
    if url.scheme not in ('http','https') or not url.netloc:
        raise SafetyViolation('absolute HTTP(S) endpoint required')
    if args.output.exists():
        raise SafetyViolation('freeze output already exists; never overwrite prior evidence')
    # No .env discovery; credentials must be explicitly supplied in the invoking environment.
    provider = make_provider(args)
    manifest = load_manifest(SMOKE)
    stamp = utc_now().strftime('%Y%m%dT%H%M%S%fZ')
    session_dir = args.artifacts / stamp
    session_dir.mkdir(parents=True, exist_ok=False)
    system, template = SYSTEM.read_text(), TEMPLATE.read_text()
    records, echoed, finish_reasons, underlying = [], set(), set(), set()
    settings = dict(provider=provider.name, provider_type=args.provider, base_url=args.base_url.rstrip('/'),
                    model=args.model, temperature=args.temperature, max_tokens=args.max_tokens, timeout=args.timeout)
    add_routing_settings(settings, args)
    write_json_new(session_dir/'session_manifest.json', {'engineering_only':True,'purpose':'SMOKE DATA — NEVER SCIENTIFIC DATA','settings':settings})
    try:
        for prior_path, suffix in zip(PRIORS, ('G','P')):
            priors = load_prior_map(prior_path)
            for program in manifest.included:
                pair = build_prompt_pair(system,template,program,priors[program.pattern_label])
                for condition, prompt, prior in [('no_prior',pair.control_user_prompt,None),
                     ('generic_prior' if suffix=='G' else 'pattern_prior',pair.treatment_user_prompt,pair.prior_hash)]:
                    record = run_one(provider=provider,program=program,condition=condition,repetition=1,
                        experiment_name=f'smoke_freeze_{suffix}',session_id=stamp,system_prompt=system,user_prompt=prompt,
                        shared_prompt_hash=pair.shared_prompt_hash,prior_hash=prior,manifest_hash=file_sha256(SMOKE),
                        model=args.model,temperature=args.temperature,max_tokens=args.max_tokens,
                        raw_session_dir=session_dir/'raw',processed_session_dir=session_dir/'processed')
                    records.append(record)
                    append_experiment_log(args.experiment_log,record)
                    raw = json.loads((ROOT/record.raw_response_path).read_text()) if record.raw_response_path else {}
                    check_smoke_record(record, raw)
                    if 'openrouter_routing' in settings:
                        actual = raw['response_metadata'].get('actual_underlying_provider')
                        expected = settings['openrouter_routing']['expected_provider_name']
                        if actual != expected:
                            raise SafetyViolation('underlying provider identity missing or mismatched')
                        underlying.add(actual)
                    echoed.add(raw['actual_model'])
                    finish_reasons.add(raw['response_metadata'].get('finish_reason'))
    except (ValueError, OSError, KeyError) as exc:
        write_json_new(session_dir/'VOID.json',{'status':'VOID','engineering_only':True,'reason':str(exc),'calls':len(records)})
        with args.experiment_log.open('a') as log:
            log.write(f'\nSmoke freeze VOID {stamp}: {exc}. Do not proceed; record correction before a new attempt.\n')
        raise
    freeze = {'status':'PASS','engineering_only':True,'purpose':'SMOKE DATA — NEVER SCIENTIFIC DATA',
        'date':utc_now().isoformat(), 'settings':settings, 'model_kind':args.model_kind,
        'model_reference':args.model_reference,'accepted_alias_risk':args.accepted_alias_risk,
        'echoed_models':sorted(echoed),'calls':len(records),'parse_successes':len(records),
        'finish_reasons':sorted(finish_reasons,key=str), 'artifacts':str(session_dir.resolve()),
        'session_order':['G','P'] if secrets.randbits(1)==0 else ['P','G'],
        'coin_flip_method':'one secrets.randbits(1), 0=G first; recorded once after successful mechanical check',
        'asset_hashes':{str(p.relative_to(ROOT)):file_sha256(p) for p in freeze_asset_paths()}}
    if 'openrouter_routing' in settings:
        freeze['echoed_underlying_providers'] = sorted(underlying)
    write_json_new(args.output,freeze)
    return freeze


def parser():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--provider',choices=['openai_compatible'],required=True)
    p.add_argument('--provider-label',required=True)
    add_routing_arguments(p)
    p.add_argument('--base-url',required=True)
    p.add_argument('--model',required=True)
    p.add_argument('--model-kind',choices=['pinned','alias_only'],required=True)
    p.add_argument('--model-reference',required=True,help='Provider documentation identifying this exact version; no automatic alias guessing')
    p.add_argument('--accepted-alias-risk',default='')
    p.add_argument('--temperature',type=float,default=0)
    p.add_argument('--max-tokens',type=int,default=1024)
    p.add_argument('--timeout',type=float,default=120)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--artifacts',type=Path,default=ROOT/'results/smoke-freeze')
    p.add_argument('--experiment-log',type=Path,default=ROOT/'EXPERIMENT_LOG.md')
    return p


def main():
    try:
        freeze=run(parser().parse_args())
        print(json.dumps(freeze,indent=2))
    except (ValueError,OSError,KeyError) as exc:
        print(f'model freeze aborted: {exc}',file=sys.stderr)
        raise SystemExit(1) from exc


if __name__=='__main__':
    main()
