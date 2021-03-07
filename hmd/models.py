from django.db import models

# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=5)

class CountryAgePopulation():
    SEX_CHOICES = [
        ('m','m'),
        ('f','f'),
        ('a','a')
    ]
    country = models.ForeignKey(Country, on_delete=models.SET_NULL)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default='a')
    age = models.IntegerField()
    population = models.IntegerField()


class CountryAgeDeaths():
    SEX_CHOICES = [
        ('m','m'),
        ('f','f'),
        ('a','a')
    ]
    country = models.ForeignKey(Country, on_delete=models.SET_NULL)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default='a')
    age = models.IntegerField()
    population = models.IntegerField()


class CountryBirths():
    SEX_CHOICES = [
        ('m','m'),
        ('f','f'),
        ('a','a')
    ]
    country = models.ForeignKey(Country, on_delete=models.SET_NULL)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default='a')
    population = models.IntegerField()

# Populated by COUNTRY/STATS/fltper_1x1.txt or mltper_1x1.txt
class LifeTable():
    country = models.ForeignKey(Country, on_delete=models.SET_NULL)
    