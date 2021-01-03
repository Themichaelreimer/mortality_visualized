from django.shortcuts import render
from django.http import JsonResponse

import covid.business as business


def get_cases(request) -> JsonResponse:
    body = request.POST

    region_name = body.get('region')
    parent = body.get('country')

    if parent and not region_name:
        region_name = parent
        parent = None

    region = business.lookup_region(region_name, parent)
    cases = business.get_region_cases_timeseries(region)

    return JsonResponse(cases)


def get_deaths(request) -> JsonResponse:
    body = request.POST

    region_name = body.get('region')
    parent = body.get('country')

    if parent and not region_name:
        region_name = parent
        parent = None

    region = business.lookup_region(region_name, parent)
    cases = business.get_region_deaths_timeseries(region)

    return JsonResponse(cases)


def get_regions(request) -> JsonResponse:
    return JsonResponse(business.get_regions_tree(), safe=False)