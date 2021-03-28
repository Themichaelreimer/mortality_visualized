from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from hmd.models import *


def add_access_control_headers(resp):
    response = resp
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
    return response


@csrf_exempt
def get_countries(request) -> JsonResponse:
    countries = Country.objects.all().values('id', 'name').order_by('name')
    data = list(countries)
    return add_access_control_headers(JsonResponse(data, safe=False))


@csrf_exempt
def get_lifetable_years(request) -> JsonResponse:
    country = request.POST.get('country')
    years = [x['year'] for x in LifeTable.objects
                .filter(country__name=country)
                .values('year')
                .distinct()
                .order_by('-year')
                ]
    return add_access_control_headers(JsonResponse(years, safe=False))


@csrf_exempt
def get_life_table(request) -> JsonResponse:
    country = request.POST.get('country')
    sex = request.POST.get('sex').lower()[0]
    year = request.POST.get('year')

    life_table = LifeTable.objects.filter(
        country__name=country,
        year=year,
        sex=sex,
        age__lte=109
    ).order_by('age').values('age', 'probability', 'cumulative_probability')
    life_table = list(life_table)
    return add_access_control_headers(JsonResponse(life_table, safe=False))
