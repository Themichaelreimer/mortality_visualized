from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
# Create your views here.

import wiki.business as business

@csrf_exempt
def disease_index(request):

    diseases = business.get_diseases_list()
    response = JsonResponse(diseases, safe=False)

    if settings.DEBUG:
        response["Access-Control-Allow-Origin"] = "*"
    else:
        response["Access-Control-Allow-Origin"] = "medistat.online"

    response["Access-Control-Allow-Methods"] = "GET"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
    return response
