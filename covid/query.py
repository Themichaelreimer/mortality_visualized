from covid.models import *
from typing import List

import covid.helpers as helpers


def ensure_region(name: str, parent=None):
    if parent:
        parent_obj = ensure_region(parent)
        res, _ = Region.objects.get_or_create(name=name, parent=parent_obj)
    else:
        res, _ = Region.objects.get_or_create(name=name)

    return res


def lookup_region(region_name: str, parent_name: str):
    if parent_name:
        return Region.objects.get(name=region_name, parent__name=parent_name)
    return Region.objects.get(name=region_name)


def get_regions_children(region: Region):
    return list(Region.objects.filter(parent=region))

'''
def new_cases(row: dict):
    """ Row is a dict with the keys and values matching Cases in models.py """
    Cases.objects.update_or_create(**row)


def new_deaths(row: dict):
    """ Row is a dict with the keys and values matching Deaths in models.py """
    Deaths.objects.update_or_create(**row)


def get_regions() -> dict:
    """
        Returns all the regions as a dictionary mapping the name to the object
        Used to implement a cache to reduce database calls
    """
    result = {}
    regions = Region.objects.all()
    for region in regions:
        result[str(region)] = region
    return result


def get_region_cases_delta(region: Region, date_start=None, date_end=None) -> dict:
    """
    Dict mapping dates to new cases
    :param region:
    :param date_start:
    :param date_end:
    :return:
    """
    
    query = {
        'region': region,
    }
    
    if date_start:
        query['date__gte'] = date_start
    if date_end:
        query['date__lte'] = date_end

    cases = Cases.objects.filter(**query).order_by("date")
    result = dict()

    for i, case in enumerate(cases):
        if i == 0:
            continue
        result[helpers.date_fmt(case.date)] = case.cumulative - cases[i-1].cumulative

    return result


def get_region_deaths_delta(region: Region, date_start=None, date_end=None) -> dict:
    """
    Dict mapping dates to new cases
    :param region:
    :param date_start:
    :param date_end:
    :return:
    """

    query = {
        'region': region,
    }

    if date_start:
        query['date__gte'] = date_start
    if date_end:
        query['date__lte'] = date_end

    deaths = Deaths.objects.filter(**query).order_by("date")
    result = dict()

    for i, death in enumerate(deaths):
        if i == 0:
            continue
        result[helpers.date_fmt(death.date)] = death.cumulative - deaths[i - 1].cumulative

    return result


def get_region_cases_cumulative(region: Region, date_start=None, date_end=None) -> List[Cases]:
    query = {
        'region': region,
    }

    if date_start:
        query['date__gte'] = date_start
    if date_end:
        query['date__lte'] = date_end

    result = Cases.objects.filter(**query).order_by("date")
    return list(result)

'''