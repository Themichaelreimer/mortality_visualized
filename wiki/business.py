import re
from typing import Union, List

from django.core.cache import cache
from wiki.query import *


#region scraper

def is_float(text: str) -> bool:
    try:
        float(text)
        return True
    except:
        return False


def is_int(text: str) -> bool:
    try:
        int(text)
        return True
    except:
        return False


def pre_process_string(text: str) -> str:
    """
    Preprocesses text by stripping spaces, lowercasing, and removing wiki citation brackets [0][1]
    :param text: input
    :return: output
    """
    text = text.strip().lower()
    return re.sub(r'(\[.*\])', r'', text)


def __extract_objects(comma_seperated_list: str, function) -> list:
    """
    Given a string representing a set of objects, and a function that maps the tokens to objects,
    this function returns a list of the objects represented by that string
    :param comma_seperated_list: string representing objects seperated by spaces
    :param function: function that maps a token to an object
    :return: list of objects
    """
    props = comma_seperated_list.split(',')
    objs = [function(pre_process_string(x)) for x in props]
    return objs


def __combine_adjacent_numbers(tokens:List[str]) -> List[str]:
    """
    Given a list of tokens, if any two adjacent tokens are numbers, they are combined by multiplication
    :param tokens: Tokenized string
    :return: Tokenized string, with the above property
    """
    result = []
    skip_next = False
    for i, token in enumerate(tokens):
        if skip_next:
            skip_next = False
            continue

        if i+1 < len(tokens) and is_float(token) and is_float(tokens[i+1]):
            result.append(float(token) * float(tokens[i+1]))
            skip_next = True
        else:
            result.append(token)

    return result


def __try_recognise_ratio(text: str) -> Union[float, None]:
    """
    If a ratio can be recognised in the input string, that ratio is returned. None otherwise
    :param text: input
    :return: float representing the ratio if detected, None otherwise
    """
    # Maybe use this regex? \d+\.?\d* ?(per|\/)? ?\d+

    input = re.sub(r",|'", r'', pre_process_string(text))
    input = re.sub(r"thousand", r"1000 ", input)
    input = re.sub(r"million", r"1000000 ", input)
    input = re.sub(r"billion", r"1000000000 ", input)

    tokens = [x for x in input.split()]

    # Multiplies adjacent numbers and combines the tokens, eg ['2', '1000', 'per' 'year' -> '2000', 'per', 'year']
    tokens = __combine_adjacent_numbers(tokens)

    numerator = None
    should_divide = False

    for token in tokens:
        if token in ['per', '/', 'in']:
            should_divide = True
            continue
        if is_float(token):
            if not numerator:
                numerator = token
            elif should_divide:
                denominator = token
                return float(numerator)/float(denominator)  # Greedy detect first fraction

    if numerator:
        if is_int(numerator):
            return int(numerator)
        return float(numerator)


def create_article(params: dict) -> 'Article':
    return ensure_article(params)


def handle_infobox(params: dict) -> 'WikiDisease':
    disease = {}

    name = params.get('name')
    disease['name'] = name

    other_names = params.get('other_names')
    disease['other_names'] = other_names

    icd10 = params.get('ICD-10')
    if not icd10:
        icd10 = params.get('icd-10')
    if icd10:
        disease['icd10'] = icd10

    specialty = params.get('specialty')
    if specialty:
        disease['specialty'] = __extract_objects(specialty, ensure_speciality)

    frequency = params.get('frequency')
    if frequency:
        val = None
        freq = __try_recognise_ratio(frequency)
        if type(freq) == int:
            val = ensure_frequency({'frequency_int': freq})
        if type(freq) == float:
            val = ensure_frequency({'frequency_ratio': freq})
        if val:
            disease['frequency'] = val

    mortality_rate = params.get('mortality rate')
    if mortality_rate:
        val = None
        freq = __try_recognise_ratio(mortality_rate)
        if type(freq) == int:
            val = ensure_mortality_rate({'frequency_int': freq})
        if type(freq) == float:
            val = ensure_mortality_rate({'frequency_ratio': freq})
        if val:
            disease['mortality_rate'] = val

    cfr = params.get('case fatality rate')
    if cfr:
        val = None
        freq = __try_recognise_ratio(cfr)
        if type(freq) == int:
            val = ensure_case_fatality_rate({'frequency_int': freq})
        if type(freq) == float:
            val = ensure_case_fatality_rate({'frequency_ratio': freq})
        if val:
            disease['case_fatality_rate'] = val

    deaths = params.get('deaths')
    if deaths:
        val = None
        freq = __try_recognise_ratio(deaths)
        if type(freq) == int:
            val = ensure_deaths({'frequency_int': freq})
        if type(freq) == float:
            val = ensure_deaths({'frequency_ratio': freq})
        if val:
            disease['deaths'] = val

    # Try infer mortality rate from frequency and deaths
    if not disease.get('mortality_rate'):
        if type(disease.get('deaths')) == int and type(disease.get('frequency')) == int and not (disease.get('deaths') == 0):
            disease['mortality_rate'] = disease.get('frequency') / disease.get('deaths')

    symptoms = params.get('symptoms')
    if symptoms:
        disease['symptoms'] = __extract_objects(symptoms, ensure_symptom)

    risks = params.get('risk factors')
    if risks:
        disease['risk_factors'] = __extract_objects(risks, ensure_risk_factor)

    treatments = params.get('treatment')
    if treatments:
        disease['treatments'] = __extract_objects(treatments, ensure_treatment)

    preventions = params.get('prevention')
    if preventions:
        disease['preventions'] = __extract_objects(preventions, ensure_prevention)

    diagnostic_methods = params.get('diagnostic methods')
    if diagnostic_methods:
        disease['diagnostic_methods'] = __extract_objects(diagnostic_methods, ensure_diagnostic_method)

    medications = params.get('medication')
    if medications:
        disease['medications'] = __extract_objects(medications, ensure_medication)

    causes = params.get('causes')
    if causes:
        disease['causes'] = __extract_objects(causes, ensure_cause)

    return make_disease(disease)

#endregion


def get_disease_info(disease: WikiDisease) -> dict:

    result = {
        'name': disease.name,
        'other_names': disease.other_names,
        'icd10': disease.icd10,
        'specialty': [x for x in disease.specialty.all()],
        'frequency': disease.frequency,
        'mortality_rate': disease.mortality_rate,
        'deaths': disease.deaths,
        'symptoms': [x for x in disease.symptoms.all()],
        'risk_factors': [x for x in disease.risk_factors.all()],
        'treatments': [x for x in disease.treatments.all()],
        'preventions': [x for x in disease.preventions.all()],
        'diagnostic_methods': [x for x in disease.diagnostic_methods.all()],
        'medications': [x for x in disease.medications.all()],
        'causes': [x for x in disease.causes.all()]
    }
    return result


def get_diseases_by_symptom(symptom: WikiSymptom) -> List[WikiDisease]:
    return list(symptom.wikidisease_set.all())


def get_diseases_list():
    cache_key = "disease_list"
    result = cache.get(cache_key)
    if result:
        return result
    
    result = [ x.to_dict() for x in get_nonempty_diseases() ]
    cache.set(cache_key, result)
    return result