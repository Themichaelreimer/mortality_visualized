from wiki.models import *
from typing import List


def make_disease(params: dict) -> WikiDisease:

    simple_props = {
        'name': params.get('name'),
        'frequency': params.get('frequency'),
        'mortality_rate': params.get('mortality_rate'),
        'case_fatality_rate': params.get('case_fatality_rate'),
        'deaths': params.get('deaths')
    }

    if params.get('other_names'):
        simple_props['other_names'] = params.get('other_names')

    if params.get('icd10'):
        simple_props['icd10'] = params.get('icd10')

    disease, _ = WikiDisease.objects.get_or_create(**simple_props)

    # Unpacks all m2m values/columns (which is most of the table)
    for k in params:
        v = params.get(k)
        if k in ['name', 'other_names', 'icd10', 'frequency', 'mortality_rate', 'case_fatality_rate', 'deaths']:
            continue
        field = getattr(disease, k)
        field.add(*v)

    return disease


def ensure_article(params: dict) -> Article:
    res, _ = Article.objects.get_or_create(**params)
    return res


def ensure_speciality(name: str) -> WikiSpecialty:
    res, _ = WikiSpecialty.objects.get_or_create(name=name.lower())
    return res


def ensure_medication(name: str) -> WikiMedication:
    res, _ = WikiMedication.objects.get_or_create(name=name.lower())
    return res


def ensure_diagnostic_method(name: str) -> WikiDiagnosticMethod:
    res, _ = WikiDiagnosticMethod.objects.get_or_create(name=name.lower())
    return res


def ensure_prevention(name: str) -> WikiPrevention:
    res, _ = WikiPrevention.objects.get_or_create(name=name.lower())
    return res


def ensure_treatment(name: str) -> WikiTreatment:
    res, _ = WikiTreatment.objects.get_or_create(name=name.lower())
    return res


def ensure_risk_factor(name: str) -> WikiRiskFactor:
    res, _ = WikiRiskFactor.objects.get_or_create(name=name.lower())
    return res


def ensure_symptom(name: str) -> WikiSymptom:
    res, _ = WikiSymptom.objects.get_or_create(name=name.lower())
    return res


def ensure_cause(name: str) -> WikiCause:
    res, _ = WikiCause.objects.get_or_create(name=name.lower())
    return res


def ensure_mortality_rate(params: dict) -> WikiMortalityRate:
    res, _ = WikiMortalityRate.objects.get_or_create(**params)
    return res


def ensure_case_fatality_rate(params: dict) -> WikiCaseFatalityRate:
    res, _ = WikiCaseFatalityRate.objects.get_or_create(**params)
    return res


def ensure_deaths(params: dict) -> WikiDeath:
    res, _ = WikiDeath.objects.get_or_create(**params)
    return res


def ensure_frequency(params: dict) -> WikiFrequency:
    res, _ = WikiFrequency.objects.get_or_create(**params)
    return res


def get_nonempty_diseases() -> List[WikiDisease]:
    results = WikiDisease.objects.all()  # TODO
    return results