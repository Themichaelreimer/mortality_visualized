from covid.models import *
from typing import List
import datetime

def ensure_region(name:str, parent=None):
    if parent:
        res, _ = Region.objects.get_or_create(name=name,parent=parent)
    else:
        res, _ = Region.objects.get_or_create(name=name)

    return res
    
def new_cases(row:dict):
    """ Row is a dict with the keys and values matching Cases in models.py """
    Cases.objects.create(**row)

def new_deaths(row:dict):
    """ Row is a dict with the keys and values matching Deaths in models.py """
    Deaths.objects.create(**row)

def get_regions():
    """
        Returns all the regions as a dictionary mapping the name to the object
        Used to implement a cache to reduce database calls
    """
    result = {}
    regions = Region.objects.all()
    for region in regions:
        result[region.name] = region
    return result

def get_region_cases(region:Region, date_start:datetime.datetime, date_end:datetime.datetime):
    
    query = {
        'region':region,
    }
    
    if date_start:
        query['date__gte'] = date_start
    if date_end:
        query['date__lte'] = date_end

    result = Cases.objects.filter(**query)
