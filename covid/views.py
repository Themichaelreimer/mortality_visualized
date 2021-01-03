from django.shortcuts import render
from django.http import JsonResponse

import covid.business as business


def get_cases(request) -> JsonResponse:
    body = request.POST

    region_name = body.get('region')
    parent = body.get('country')
    region = business.lookup_region(region_name, parent)

    cases = business.get_region_timeseries(region)
    return JsonResponse(cases)


def get_deaths(request) -> JsonResponse:
    pass


def get_regions(request) -> JsonResponse:
    return JsonResponse(business.get_regions_tree(), safe=False)