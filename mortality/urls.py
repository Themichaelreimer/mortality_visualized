"""mortality URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

import covid.views as covid_views
import wiki.views as wiki_views
import hmd.views as hmd_views

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('regions/', covid_views.get_regions),
    path('cases/', covid_views.get_cases),
    path('deaths/', covid_views.get_deaths),
    path('diseases/', wiki_views.disease_index),
    path('lifetables/', hmd_views.get_life_table),
    path('lifetable_years/', hmd_views.get_lifetable_years),
    path('lifetables_countries/', hmd_views.get_countries),
    # TODO: Deaths
]
