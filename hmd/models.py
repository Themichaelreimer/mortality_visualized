from django.db import models
from django.forms import model_to_dict

SEX_CHOICES = [
    ('m', 'm'),
    ('f', 'f'),
    ('a', 'a')
]


class Country(models.Model):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=8)

    def __str__(self):
        return str(self.name)


class CountryAgePopulation(models.Model):
    SEX_CHOICES = [
        ('m','m'),
        ('f','f'),
        ('a','a')
    ]
    country = models.ForeignKey(Country, null=True, on_delete=models.SET_NULL)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default='a')
    age = models.IntegerField()
    population = models.IntegerField()


class CountryAgeDeaths(models.Model):
    country = models.ForeignKey(Country, null=True, on_delete=models.SET_NULL)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default='a')
    age = models.IntegerField()
    population = models.IntegerField()


class CountryBirths(models.Model):
    country = models.ForeignKey(Country, null=True, on_delete=models.SET_NULL)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default='a')
    population = models.IntegerField()


# Populated by COUNTRY/STATS/fltper_1x1.txt or mltper_1x1.txt
class LifeTable(models.Model):
    country = models.ForeignKey(Country, null=True, on_delete=models.SET_NULL)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default='a')
    age = models.IntegerField()
    year = models.IntegerField()
    probability = models.DecimalField(max_digits=10, decimal_places=5)
    cumulative_probability = models.DecimalField(max_digits=10, decimal_places=5)

    def __str__(self):
        return f"({self.age}{self.sex} {self.country}) - {self.probability}"

    def to_dict(self):
        return {self.id: model_to_dict(self)}
