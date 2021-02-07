from django.db import models

# Create your models here.


class Article(models.Model):
    """
        This class represents an article post parsing HTML, but with no other processing yet
    """
    title = models.CharField(default="", max_length=128, unique=True)
    text = models.TextField(default="")
    infobox = models.ForeignKey('Infobox', null=True, default=None, on_delete=models.SET_NULL)

class Infobox(models.Model):
    """
        This class is a container for the info in an infobox. I expect these to be insanely valuable, so they get their own class
    """

    specialty = models.CharField(default="", max_length=255)
    symptoms = models.CharField(default="", max_length=255)
    usual_onset = models.CharField(default="", max_length=255)
    duration = models.CharField(default="", max_length=255)
    types = models.CharField(default="", max_length=255)
    risk_factors = models.CharField(default="", max_length=255)
    complications = models.CharField(default="", max_length=255)
    diagnostic_method = models.CharField(default="", max_length=255)
    prevention = models.CharField(default="", max_length=255)
    treatment = models.CharField(default="", max_length=255)
    medication = models.CharField(default="", max_length=255)
    prognosis = models.CharField(default="", max_length=255)
    frequency = models.CharField(default="", max_length=255)
    deaths = models.CharField(default="", max_length=255)
    icd_code = models.CharField(max_length=32)

class WikiFrequency(models.Model):
    region_name = models.CharField(max_length=255, unique=True)
    frequency = models.IntegerField()

class WikiDeath(models.Model):
    region_name = models.CharField(max_length=255, unique=True)
    frequency = models.IntegerField()

class WikiSymptom(models.Model):
    name = models.CharField(default="", max_length=255, unique=True)

class WikiRiskFactor(models.Model):
    name = models.CharField(default="", max_length=255, unique=True)

class WikiTreatment(models.Model):
    name = models.CharField(default="", max_length=255, unique=True)

class WikiPrevention(models.Model):
    name = models.CharField(default="", max_length=255, unique=True)

class WikiDiagnosticMethod(models.Model):
    name = models.CharField(default="", max_length=255, unique=True)

class WikiMedication(models.Model):
    name = models.CharField(default="", max_length=255, unique=True)


class WikiDisease(models.Model):
    """
        This class represents the 'endpoint' in the wikipedia parsing pipeline. Entries in this table are considered complete
    """
    name = models.CharField(default="", max_length=255, unique=True)
    frequency = models.ManyToManyField(WikiFrequency)
    deaths = models.ManyToManyField(WikiDeath)
    symptoms = models.ManyToManyField(WikiSymptom)
    risk_factors = models.ManyToManyField(WikiRiskFactor)
    treatments = models.ManyToManyField(WikiTreatment)
    preventions = models.ManyToManyField(WikiPrevention)
    diagnostic_methods = models.ManyToManyField(WikiDiagnosticMethod)
    medications = models.ManyToManyField(WikiMedication)


