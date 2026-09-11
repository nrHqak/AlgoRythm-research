"""Operational validity gates; never infer validity from localization accuracy."""
from experiments.safety import SafetyViolation


def assert_session_health(records, *, completed=True):
    if not records:
        raise SafetyViolation('empty session is void')
    if any(r.error_type == 'ModelIdentityMismatch' for r in records):
        raise SafetyViolation('ModelIdentityMismatch: session is void; do not resume')
    if any(r.error_type == 'UnderlyingProviderMismatch' for r in records):
        raise SafetyViolation('UnderlyingProviderMismatch: session is void; do not resume')
    # The first-50 gate is evaluated on each chronological prefix, as during execution.
    first = sorted(records, key=lambda r: (r.timestamp, r.run_id))[:50]
    failures = 0
    for count, record in enumerate(first, 1):
        failures += record.status == 'provider_failure'
        if failures / count > .05:
            raise SafetyViolation('provider_failure rate >5% within first 50 calls; session is void')
    if completed and sum(r.status == 'ok' for r in records) / len(records) < .8:
        raise SafetyViolation('overall ok rate <80% (including all-non-ok): session is void')
