from covid.models import *

import covid.query as query
import covid.helpers as helpers

from typing import List

'''

regions_cache = query.get_regions()

def __cache_get(region: str, parent_region: str) -> Region:
    """
    Implements a cache for regions to avoid repeatedly querying the same object

    :param region:
    :param parent_region:
    :return:
    """
    key = region
    if parent_region:
        key = f"{region},{parent_region}"

    # Return from cache
    if region in regions_cache.keys():
        return regions_cache[key]

    # Set cache value
    new_region = query.ensure_region(region, parent=parent_region)
    regions_cache[key] = new_region
    return new_region


def get_top_level_regions() -> List[Region]:
    """ Returns all regions with null parent"""
    return query.get_regions_children(None)


def get_subregions(region: Region):
    """ Returns all children of a given region"""
    return query.get_regions_children(region)


def get_regions_tree(serialize=False) -> List[dict]:
    """
    Builds a list of all countries with their territories nested
    If serialize=True, then regions will be represented as dicts for JsonResponses
    """
    countries = get_top_level_regions()
    result = []
    for country in countries:
        result.append({
            'country': country.to_dict(),
            'children': [x.to_dict() for x in get_subregions(country)]
        })
    return result


def lookup_region(region_name: str, subregion_name: str) -> Region:
    return query.lookup_region(region_name,subregion_name)


def get_region_cases_timeseries(region: Region) -> dict:
    """
    Returns a dict mapping dates to case numbers.
    Note that we're returning the number of new cases, not cumulative

    :param region: Region we're concerned with
    :return: dict mapping dates to new cases
    """
    children = query.get_regions_children(region)
    if len(children) == 0:
        cases = query.get_region_cases_delta(region)
        return cases
    else:
        result = {}
        for child in children:
            cases = query.get_region_cases_delta(child)
            for date in cases.keys():
                if date in result.keys():
                    result[date] += cases[date]
                else:
                    result[date] = cases[date]

        return result


def get_region_deaths_timeseries(region: Region) -> dict:
    """
    Returns a dict mapping dates to case numbers.
    Note that we're returning the number of new cases, not cumulative

    :param region: Region we're concerned with
    :return: dict mapping dates to new cases
    """
    children = query.get_regions_children(region)
    if len(children) == 0:
        deaths = query.get_region_deaths_delta(region)
        return deaths
    else:
        result = {}
        for child in children:
            deaths = query.get_region_deaths_delta(child)
            for date in deaths.keys():
                if date in result.keys():
                    result[date] += deaths[date]
                else:
                    result[date] = deaths[date]

        return result


def get_region_timeseries(region: Region) -> dict:
    pass
    # TODO: This should give cases *and* deaths


def process_row(row: dict, is_cases: bool):
    """
        Loads a row into the database. Assumes the input has the following keys:
        'region' - name of region
        'parent region' - name of parent region. May be blank
        'date' - parseable date string
        'value' - Number of cases

        is_cases = true => This is a cases entry. Otherwise, the number is interpreted as deaths
    """
    new_row = {}
    new_row['region'] = __cache_get(row.get('region'), row.get('parent_region'))
    new_row['date'] = helpers.parsedate(row.get('date'))
    new_row['cumulative'] = row.get('value')

    if is_cases:
        query.new_cases(new_row)
    else:
        query.new_deaths(new_row)

'''