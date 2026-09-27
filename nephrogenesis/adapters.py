"""Neutral interchange receipts, not untested drop-in upstream API integrations."""
from __future__ import annotations
from .common import digest


def review_envelope(report: dict) -> dict:
    """Export an intentionally small stable contract for external review systems."""
    return {'schema':'nephrogenesis-review-envelope-v1',
            'experiment_id':report['experiment'],'book_sections':report['book_sections'],
            'evidence_kind':report['status'],'result_digest':digest(report),
            'DIKWP':{'D':{'parameters':report['parameters'],'patient_identifiers_required':False},
                     'I':{'units_embedded':True,'assumptions':report.get('notes',report.get('assumptions',[]))},
                     'K':{'model_claim':'Conditional on declared implementation and inputs','empirical_validation':False},
                     'W':{'clinical_authority':False,'value_is_not_energy_or_information':True},
                     'P':{'task':'Reproduce, challenge and revise the attached book-companion experiment'}},
            'compatibility':'Neutral export; adapters to AgentTrace, ProofLedger or PRAXIS require mapping and contract tests against their actual schemas.'}
