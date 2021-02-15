from django.shortcuts import render

# Create your views here.

import wiki.business as business

def disease_index(request):

    # TODO: Paginate, cache, make generally efficent
    # Right now, I just want something on the screen
    diseases = business.get_diseases_list()
    disease_dicts = []
