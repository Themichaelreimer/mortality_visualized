from disease.models import *

from django.core.cache import cache
from django.utils import timezone

from typing import List, Union, Optional


def create_disease(params: dict) -> Disease:
    """
    Gets or creates a disease object using params. Params can be a dict of 'primitives' (strings, ints, floats),
    or domain objects
    :param params: dict who's keys match disease/models.py Disease
    :return: Disease object
    """
    disease, _ = Disease.objects.get_or_create(**params)
    return disease


def ensure_category_type(name: str) -> CategoryType:
    category_type, _ = CategoryType.objects.get_or_create(name=name.lower())
    return category_type


def create_categorical_value(category: Union[CategoryType, str], value:str) -> CategoricalValue:
    """
    Ensures a category value exists. Eg: (Symptom, 'Cough')
    :param category: Category the value is associated with. Note that the category doesn't have to exist yet
    :param value: Value being associated with a category
    :return: CategoricalValue
    """
    category_obj = ensure_category_type(category) if type(category) == str else category
    result, _ = CategoricalValue.objects.get_or_create(category_type=category_obj, value=value.lower())
    return result


def create_category_tag(cv: CategoricalValue, citation: Citation, disease: Disease) -> CategoricalTag:
    """
    Tags a disease with a categoricalValue and a citation for the source of the categoricalValue
    :param cv: Categorical Value
    :param citation: Citation
    :param disease: Disease Object
    :return: CategoricalTag
    """
    result, _ = CategoricalTag.objects.get_or_create(
        categorical_value=cv,
        citation=citation,
        disease=disease
    )
    return result


def create_citation(source: str, link: str, timestamp: Optional['datetime']) -> Citation:
    """
    Creates a new citation object.
    :param source: Display name of source
    :param link: Hyperlink to source
    :param timestamp: Time accessed. If none given, timezone.now is used
    :return: Citation object
    """
    result = Citation.objects.create(
        source_name=source,
        link=link,
        timestamp=timestamp if timestamp else timezone.now()
    )
    return result


def create_statistic(statistic_type: Union[str, StatisticType],
                     citation: Citation,
                     value: 'Number',
                     disease: Disease
                     ):
    result, _ = Statistic.objects.get_or_create(statistic_type=statistic_type, citation=citation, value=value, disease=disease)
    return result