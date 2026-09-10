"""Analytically known artificial sessions; never use any scientific candidate."""
from __future__ import annotations
import json
from pathlib import Path
from unittest.mock import patch

import pytest

from analysis.compare_v2_sessions import run as compare, parser as compare_parser, validate_sessions, build_report
from experiments.models import load_manifest
from experiments.model_preflight import run as smoke_run, parser as smoke_parser, validate_identity_choice
from experiments.prompts import build_prompt_pair, PRIOR_OPEN, PRIOR_CLOSE
from experiments.providers.base import LLMProvider, ProviderReply
from experiments.run_pilot import run as run_pilot, parser as runner_parser, load_prior_map
from experiments.safety import SafetyViolation

ROOT=Path(__file__).resolve().parents[1]


class SyntheticProvider(LLMProvider):
    name='mock'
    def __init__(self, scenario='C'):
        self.scenario=scenario
        self.counts={}
        self.calls=0
    def complete(self, request):
        self.calls+=1
        arm='A' if PRIOR_OPEN not in request.user_prompt else ('B' if 'This program contains a logical fault.' in request.user_prompt else 'C')
        key=(arm,request.user_prompt)
        r=self.counts.get(key,0)+1;self.counts[key]=r
        hit=arm==self.scenario
        raw=None
        if self.scenario=='tie': hit=False
        if self.scenario=='aggregation': hit=(arm=='C' and r<=3) or (arm=='B' and r<=2)
        if self.scenario=='failures':
            hit=arm=='C'
            # 3 parser failures for one program in C: 3/80 <20%, retained as misses.
            if arm=='C' and 'synthetic-0' in request.user_prompt and r<=3: raw='malformed'
        if self.scenario=='drift':
            hit=(arm=='C') or (arm=='A' and r>5)
        if self.scenario=='invalid': raw='malformed'
        if self.scenario=='transport': raise ConnectionError('synthetic offline transport failure')
        if raw is None:
            if self.scenario=='ranks' and arm=='C':
                ranking=[{'line':line,'score':1-i*.1} for i,line in enumerate([10,11,2])]
            else: ranking=[{'line':2 if hit else 10,'score':1}]
            raw=json.dumps({'ranking':ranking})
        model='wrong-snapshot' if self.scenario=='identity' else request.model
        if self.scenario=='empty': raw='  '
        if self.scenario=='zero': raw=json.dumps({'ranking':[{'line':2,'score':0}]})
        return ProviderReply(raw_response=raw,latency=.001,provider=self.name,model=model,
            response_metadata={'finish_reason':'length' if self.scenario=='truncated' else 'stop'})


def make_sessions(tmp_path, scenario='C', n=8):
    # Original code, created here from scratch; no dataset read.
    source='def total(values):\n    result = 1\n    for value in values:\n        result += value\n    return result\n'+'# synthetic padding\n'*25
    (tmp_path/'buggy.py').write_text(source)
    (tmp_path/'fixed.py').write_text(source.replace('result = 1','result = 0'))
    (tmp_path/'tests.json').write_text('{}')
    labels=['binary_search','hash_map_counting','brute_force_implementation','simulation']
    programs=[dict(program_id=f'synthetic-{i}',task_id=f'synthetic-task-{i}',buggy_source_path='buggy.py',
        fixed_source_path='fixed.py',tests_path='tests.json',faulty_lines=[2],pattern_label=labels[i%4],
        pattern_source='synthetic-only',loc=30,difficulty='synthetic',inclusion_status='included') for i in range(n)]
    manifest=tmp_path/'manifest.json'
    manifest.write_text(json.dumps(dict(manifest_version=1,dataset_name='synthetic-only',created_at='2020-01-01T00:00:00Z',
        selection_frozen_at='2020-01-02T00:00:00Z',programs=programs)))
    log=tmp_path/'log.md';log.write_text('# Synthetic log\n')
    provider=SyntheticProvider(scenario)
    dirs=[]
    with patch('experiments.run_pilot.make_provider',return_value=provider):
        for session,treatment,prior in [('G','generic_prior','pilot/v2/generic_placebo_prior.json'),('P','pattern_prior','pilot/pattern_priors.json')]:
            config=tmp_path/f'{session}.json'
            config.write_text(json.dumps(dict(experiment_name=f'synthetic_{session}',dataset=dict(target='synthetic-only',target_n=n),
                conditions=dict(control='no_prior',treatment=treatment),metrics=['top1','top3','top5','exam'],
                repetitions=5,statistics=dict(primary='exact_mcnemar'))))
            args=runner_parser().parse_args(['--config',str(config),'--manifest',str(manifest),
                '--system-prompt',str(ROOT/'pilot/v2/prompts/system_v2.txt'),'--user-template',str(ROOT/'pilot/prompts/control.txt'),
                '--priors',str(ROOT/prior),'--provider','mock','--allow-mock','--model','synthetic-snapshot-2026-09-10',
                '--condition-order','counterbalanced','--session-id',session,'--output-root',str(tmp_path/'results'),
                '--experiment-log',str(log)])
            run_pilot(args)
            dirs.append(tmp_path/f'results/processed/synthetic_{session}/{session}')
    return dirs,manifest


def analyze(tmp_path, dirs, manifest, allow=True):
    args=compare_parser().parse_args(['--generic-session',str(dirs[0]),'--pattern-session',str(dirs[1]),
        '--manifest',str(manifest),'--output',str(tmp_path/'comparison.json')]+(['--allow-mock-analysis'] if allow else []))
    return compare(args)


@pytest.mark.parametrize('scenario,delta,b,c,p',[('C',1,8,0,1/128),('B',-1,0,8,1/128),('tie',0,0,0,1)])
def test_analytic_extremes(tmp_path,scenario,delta,b,c,p):
    dirs,manifest=make_sessions(tmp_path,scenario)
    report=analyze(tmp_path,dirs,manifest)
    primary=report['primary_C_vs_B']
    assert report['n_programs']==8
    assert primary['delta']==delta and primary['b']==b and primary['c']==c
    assert primary['exact_two_sided_p']==p
    assert primary['bootstrap']['percentile_95_ci']==[delta,delta]
    assert report['secondary']['EXAM*']['mean_difference_treatment_minus_control']==pytest.approx(-delta*29/30)
    assert report['secondary']['EXAM*']['bootstrap']['percentile_95_ci']==pytest.approx([-delta*29/30]*2)
    assert report['secondary']['EXAM*']['wilcoxon_two_sided_p']==p
    assert report['null_calibration']['primary_interpretable']==bool(b+c)
    assert all(x['raw_byte_identical_rate']==1 for x in report['run_integrity']['determinism'].values())
    assert len(report['robustness_all_five_repetitions']['A_vs_C']['top1'])==5
    if scenario=='tie': assert report['confirmatory_sizing']['N_range'] is None


def test_majority_not_call_means(tmp_path):
    dirs,manifest=make_sessions(tmp_path,'aggregation')
    report=analyze(tmp_path,dirs,manifest)
    assert report['primary_C_vs_B']['delta']==1 # NOT 0.6 - 0.4 = 0.2
    assert report['primary_C_vs_B']['n_programs']==8 # NOT 40
    assert report['secondary']['EXAM*']['mean_difference_treatment_minus_control']==pytest.approx(-.2*29/30)
    assert report['run_integrity']['determinism']['C']['top1_agreement_rate']==0


def test_top3_top5_and_censored_exam(tmp_path):
    dirs,manifest=make_sessions(tmp_path,'ranks')
    report=analyze(tmp_path,dirs,manifest)
    assert report['primary_C_vs_B']['delta']==0
    assert report['secondary']['top3']['delta']==1
    assert report['secondary']['top5']['delta']==1
    assert report['secondary']['EXAM*']['treatment_mean']==pytest.approx(3/30)


def test_failures_count_as_misses_without_dropping(tmp_path):
    dirs,manifest=make_sessions(tmp_path,'failures')
    report=analyze(tmp_path,dirs,manifest)
    assert report['primary_C_vs_B']['b']==7
    assert report['n_programs']==8
    assert report['run_integrity']['parser_diagnostics']['C']['parser_failures']==3
    assert report['primary_C_vs_B']['bootstrap']['percentile_95_ci']==[5/8,1]
    assert report['secondary']['EXAM*']['treatment_mean']==pytest.approx((37/30+3)/40)


def test_null_drift_gate_including_equal_discordance(tmp_path):
    dirs,manifest=make_sessions(tmp_path,'drift')
    report=analyze(tmp_path,dirs,manifest)
    assert report['null_calibration']['discordant_pairs']==8
    assert report['primary_C_vs_B']['d']==8
    assert not report['null_calibration']['primary_interpretable']


@pytest.mark.parametrize('field,value',[('model','other'),('provider','other'),('temperature',1),('max_tokens',2048),
    ('timeout',3),('base_url','https://different.example'),('manifest_hash','different-sample'),('repetitions',4),
    ('system_prompt_hash','other'),('user_template_hash','other'),('condition_order','control_first'),('model_freeze_hash','other')])
def test_cross_session_setting_mismatch_fails_without_output(tmp_path,field,value):
    dirs,manifest=make_sessions(tmp_path)
    path=dirs[1]/'session_manifest.json';data=json.loads(path.read_text());data[field]=value;path.write_text(json.dumps(data))
    with pytest.raises(SafetyViolation,match='mismatch'): analyze(tmp_path,dirs,manifest)
    assert not (tmp_path/'comparison.json').exists()


@pytest.mark.parametrize('mutation',['missing_program','both_missing_program','missing_rep','duplicate','raw_leak','delimiter','record_model','sample_changed','mock_guard','VOID'])
def test_integrity_tampering(tmp_path,mutation):
    dirs,manifest=make_sessions(tmp_path)
    files=[p for p in dirs[1].glob('*.json') if 'run_id' in json.loads(p.read_text())]
    target=files[0];data=json.loads(target.read_text())
    if mutation in ('missing_program','both_missing_program'):
        for directory in (dirs if mutation=='both_missing_program' else dirs[1:]):
            for path in directory.glob('*.json'):
                if json.loads(path.read_text()).get('program_id')=='synthetic-0':path.unlink()
    elif mutation=='missing_rep':target.unlink()
    elif mutation=='duplicate':(dirs[1]/'duplicate.json').write_text(target.read_text())
    elif mutation in ('raw_leak','delimiter'):
        treatment_file=next(p for p in files if json.loads(p.read_text())['condition']=='pattern_prior')
        data=json.loads(treatment_file.read_text());raw_path=Path(data['raw_response_path']);raw=json.loads(raw_path.read_text())
        raw['user_prompt']=raw['user_prompt']+'\nfaulty_lines: [2]' if mutation=='raw_leak' else raw['user_prompt'].replace('DEBUGGING_PRIOR','ALGORITHMIC_PATTERN_PRIOR')
        raw_path.write_text(json.dumps(raw))
    elif mutation=='record_model':data['model']='other';target.write_text(json.dumps(data))
    elif mutation=='sample_changed':manifest.write_text(manifest.read_text()+'\n')
    elif mutation=='VOID':(dirs[1]/'VOID.json').write_text('{}')
    with pytest.raises((SafetyViolation,ValueError)): analyze(tmp_path,dirs,manifest,allow=mutation!='mock_guard')
    assert not (tmp_path/'comparison.json').exists()


def test_all_labels_only_prior_content_differs_and_truth_invariant():
    program=load_manifest(ROOT/'data/smoke/manifest.json').included[0]
    system=(ROOT/'pilot/v2/prompts/system_v2.txt').read_text();template=(ROOT/'pilot/prompts/control.txt').read_text()
    b=load_prior_map(ROOT/'pilot/v2/generic_placebo_prior.json');c=load_prior_map(ROOT/'pilot/pattern_priors.json')
    assert len(b)==len(c)==12
    assert PRIOR_OPEN=='<DEBUGGING_PRIOR>' and PRIOR_CLOSE=='</DEBUGGING_PRIOR>'
    for label in c:
        p=program.model_copy(update={'pattern_label':label})
        pairs=[build_prompt_pair(system,template,p,prior[label]) for prior in (b,c)]
        assert pairs[0].control_user_prompt==pairs[1].control_user_prompt
        for pair,prior in zip(pairs,(b,c)):
            assert pair.treatment_user_prompt==pair.control_user_prompt+'\n\n'+PRIOR_OPEN+'\n'+prior[label]+'\n'+PRIOR_CLOSE
        changed=p.model_copy(update={'faulty_lines':[1],'fixed_source_path':Path('/NEVER_READ_SECRET')})
        assert build_prompt_pair(system,template,changed,c[label])==pairs[1]
        assert abs(len(b[label].split())-len(c[label].split()))<=10
        assert sum(s[:1].isdigit() for s in b[label].splitlines())==sum(s[:1].isdigit() for s in c[label].splitlines())


def test_handwritten_smoke_fixtures_are_runnable():
    manifest=load_manifest(ROOT/'data/smoke/manifest.json')
    assert len(manifest.included)==3 and 'NEVER SCIENTIFIC' in manifest.dataset_name
    for p in manifest.included:
        spec=json.loads(p.tests_path.read_text())
        counts=[]
        for path in (p.buggy_source_path,p.fixed_source_path):
            namespace={};exec(compile(path.read_text(),str(path),'exec'),namespace)
            counts.append(sum(namespace[spec['function']](*case['args'])==case['expected'] for case in spec['cases']))
        assert counts[0]<len(spec['cases']) and counts[1]==len(spec['cases'])
        changed=[i for i,(a,b) in enumerate(zip(p.buggy_source_path.read_text().splitlines(),p.fixed_source_path.read_text().splitlines()),1) if a!=b]
        assert changed==p.faulty_lines


@pytest.mark.parametrize('scenario',['transport','identity','empty','truncated','invalid'])
def test_operational_failure_voids_runner(tmp_path,scenario):
    with pytest.raises(SafetyViolation):make_sessions(tmp_path,scenario)
    assert list((tmp_path/'results/processed').glob('*/*/VOID.json'))
    assert not (tmp_path/'results/pilot_metrics.json').exists()


def smoke_args(tmp_path):
    log=tmp_path/'log.md';log.write_text('# Smoke test\n')
    return smoke_parser().parse_args(['--provider','openai_compatible','--provider-label','offline-test',
        '--base-url','https://offline.invalid/v1','--model','test-snapshot-2026-09-10','--model-kind','pinned',
        '--model-reference','offline synthetic test version','--output',str(tmp_path/'freeze.json'),
        '--artifacts',str(tmp_path/'artifacts'),'--experiment-log',str(log)])


@pytest.mark.parametrize('scenario',['identity','transport','empty','truncated','invalid','zero'])
def test_smoke_failure_never_produces_freeze(tmp_path,scenario):
    with patch('experiments.model_preflight.make_provider',return_value=SyntheticProvider(scenario)):
        with pytest.raises(SafetyViolation):smoke_run(smoke_args(tmp_path))
    assert not (tmp_path/'freeze.json').exists()
    assert list((tmp_path/'artifacts').glob('*/VOID.json'))


def test_smoke_12_calls_both_shapes_both_priors(tmp_path):
    provider=SyntheticProvider('tie') # All hits wrong is acceptable; mechanical validity only.
    # Smoke sources have at least 5 lines, so choose a valid but arbitrary line.
    original=provider.complete
    def complete(request):
        reply=original(request)
        return ProviderReply(raw_response=reply.raw_response.replace('10','1'),latency=.001,provider=reply.provider,
                             model=reply.model,response_metadata=reply.response_metadata)
    provider.complete=complete
    with patch('experiments.model_preflight.make_provider',return_value=provider):freeze=smoke_run(smoke_args(tmp_path))
    assert provider.calls==freeze['calls']==freeze['parse_successes']==12
    assert freeze['engineering_only'] and freeze['session_order'] in (['G','P'],['P','G'])
    raws=[json.loads(p.read_text()) for p in (tmp_path/'artifacts').glob('*/raw/*.json')]
    assert sum(PRIOR_OPEN not in r['user_prompt'] for r in raws)==6
    assert sum(r['condition']=='generic_prior' for r in raws)==3
    assert sum(r['condition']=='pattern_prior' for r in raws)==3


def test_latest_alias_rejected_and_alias_exception_explicit():
    with pytest.raises(SafetyViolation):validate_identity_choice('model-latest','pinned','doc','')
    with pytest.raises(SafetyViolation):validate_identity_choice('model-latest','alias_only','doc','')
    validate_identity_choice('model-latest','alias_only','doc','Provider exposes aliases only; accepted risk recorded')


def test_provider_failure_thresholds_and_no_zero_accuracy_abort():
    from datetime import datetime, timezone, timedelta
    from types import SimpleNamespace
    from experiments.health import assert_session_health
    start=datetime(2020,1,1,tzinfo=timezone.utc)
    def record(i,status='ok'):
        return SimpleNamespace(status=status,error_type=None,timestamp=start+timedelta(seconds=i),run_id=str(i))
    records=[record(i) for i in range(100)]
    # Exactly 5% at call 20 is allowed; second failure at 21 exceeds 5% immediately.
    records[19]=record(19,'provider_failure')
    assert_session_health(records)
    records[20]=record(20,'provider_failure')
    with pytest.raises(SafetyViolation,match='5%'):assert_session_health(records)
    records=[record(i,'parser_failure' if i<20 else 'ok') for i in range(100)]
    assert_session_health(records) # exactly 80% ok allowed
    records[20]=record(20,'parser_failure')
    with pytest.raises(SafetyViolation,match='80%'):assert_session_health(records)
    with pytest.raises(SafetyViolation):assert_session_health([record(i,'parser_failure') for i in range(100)])
    assert_session_health([record(i) for i in range(100)]) # no hit/accuracy criterion


def test_http_requires_echoed_identity_and_records_finish_reason():
    from experiments.providers.http import OpenAICompatibleProvider
    from experiments.providers.base import CompletionRequest
    from unittest.mock import Mock
    provider=OpenAICompatibleProvider(base_url='https://offline.invalid/v1',api_key='synthetic-not-secret')
    request=CompletionRequest('system','user','snapshot-2026-09-10',0,1024)
    body={'choices':[{'message':{'content':'{"ranking":[{"line":1,"score":1}]}'},'finish_reason':'stop'}]}
    response=Mock();response.json.return_value=body
    with patch('experiments.providers.http.requests.post',return_value=response) as post:
        reply=provider.complete(request)
        assert reply.model=='' and reply.response_metadata['model_identity_exposed'] is False
        body['model']='snapshot-2026-09-10'
        reply=provider.complete(request)
        assert reply.model==request.model and reply.response_metadata['finish_reason']=='stop'
        assert post.call_args.kwargs['json']['model']==request.model


def test_freeze_required_committed_and_settings_immutable(tmp_path):
    from experiments.model_preflight import validate_freeze, freeze_asset_paths
    from experiments.storage import file_sha256
    from types import SimpleNamespace
    args=SimpleNamespace(model_freeze=None)
    with pytest.raises(SafetyViolation,match='requires --model-freeze'):validate_freeze(args,5)
    freeze_path=tmp_path/'freeze.json';freeze_path.write_text('{}');args.model_freeze=freeze_path
    with pytest.raises(SafetyViolation,match='committed'):validate_freeze(args,5)
    settings=dict(provider='test',provider_type='openai_compatible',base_url='https://offline.invalid/v1',
        model='pinned-snapshot',temperature=0,max_tokens=1024,timeout=120)
    args=SimpleNamespace(model_freeze=freeze_path,provider='openai_compatible',provider_label='test',
        base_url=settings['base_url'],model=settings['model'],temperature=0,max_tokens=1024,timeout=120,
        condition_order='counterbalanced',system_prompt=ROOT/'pilot/v2/prompts/system_v2.txt',user_template=ROOT/'pilot/prompts/control.txt')
    frozen=dict(status='PASS',engineering_only=True,settings=settings,model_kind='pinned',model_reference='offline docs',
        accepted_alias_risk='',echoed_models=['pinned-snapshot'],calls=12,parse_successes=12,session_order=['G','P'],
        asset_hashes={str(p.relative_to(ROOT)):file_sha256(p) for p in freeze_asset_paths()})
    freeze_path.write_text(json.dumps(frozen))
    with patch('experiments.model_preflight.assert_committed'):
        validate_freeze(args,5)
        args.timeout=121
        with pytest.raises(SafetyViolation,match='settings'):validate_freeze(args,5)
        args.timeout=120
        with pytest.raises(SafetyViolation,match='5 repetitions'):validate_freeze(args,3)
        frozen['echoed_models']=['other'];freeze_path.write_text(json.dumps(frozen))
        with pytest.raises(SafetyViolation,match='smoke evidence'):validate_freeze(args,5)


def test_exact_v2_call_budget_from_frozen_configs_and_runner_order():
    from experiments.run_pilot import load_yaml_object, condition_order
    totals=[]
    for name in ('generic','pattern'):
        config=load_yaml_object(ROOT/f'pilot/v2/config/pilot_v2_{name}.yaml')
        names=tuple(config['conditions'][key] for key in ('control','treatment'))
        calls=[condition for i in range(config['dataset']['target_n'])
               for r in range(1,config['repetitions']+1)
               for condition in condition_order('counterbalanced',i,r,names)]
        assert calls.count('no_prior')==150
        totals.append(len(calls))
    assert totals==[300,300] and sum(totals)==600
