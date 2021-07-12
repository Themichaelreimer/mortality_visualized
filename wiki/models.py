from django.db import models

# Create your models here.
"""
    The models in this file are deprecated. From Phase2 and onwards, Diseases should be modeled 
    using disease/models.py. The models there are more general and better fit a
    'multiple values from different sources' model
"""

class Article(models.Model):
    """
        This class represents an article post parsing HTML, but with no other processing yet
    """
    title = models.CharField(default="", max_length=128, unique=True)
    first_sentence = models.TextField(default="")
    text = models.TextField(default="")
    disease = models.ForeignKey('WikiDisease', null=True, default=None, on_delete=models.SET_NULL)


class WikiFrequency(models.Model):
    region_name = models.CharField(default='', max_length=255)
    frequency_int = models.BigIntegerField(null=True)
    frequency_ratio = models.FloatField(null=True)

    def display_value(self):
        val = self.frequency_ratio if self.frequency_ratio else self.frequency_int / 7500000000
        return unit_rule(100*val)

    def __str__(self):
        if self.frequency_int:
            return f"{self.frequency_int}"
        return f"{self.frequency_ratio}"


class WikiDeath(models.Model):
    region_name = models.CharField(default='', max_length=255)
    frequency_int = models.BigIntegerField(null=True)
    frequency_ratio = models.FloatField(null=True)

    def display_value(self):
        val = self.frequency_ratio if self.frequency_ratio else self.frequency_int / 7500000000
        return unit_rule(100*val)

    def __str__(self):
        if self.frequency_int:
            return f"{self.frequency_int}"
        return f"{self.frequency_ratio}"


class WikiCaseFatalityRate(models.Model):
    region_name = models.CharField(default='', max_length=255)
    frequency_int = models.BigIntegerField(null=True)
    frequency_ratio = models.FloatField(null=True)

    def __str__(self):
        if self.frequency_int:
            return f"{self.frequency_int}"
        return f"{self.frequency_ratio}"


class WikiMortalityRate(models.Model):
    region_name = models.CharField(default='', max_length=255)
    frequency_int = models.BigIntegerField(null=True)
    frequency_ratio = models.FloatField(null=True)

    def display_value(self):
        if self.frequency_ratio:
            return f'{self.frequency_ratio*100} %'
        return f'{self.frequency_int * 100 / 7500000000} %'

    def __str__(self):
        if self.frequency_int:
            return f"{self.frequency_int}"
        return f"{self.frequency_ratio}"


class WikiSymptom(models.Model):
    name = models.CharField(default="", max_length=512)

    def __str__(self):
        return self.name.title()


class WikiRiskFactor(models.Model):
    name = models.CharField(default="", max_length=512)

    def __str__(self):
        return self.name.title()


class WikiTreatment(models.Model):
    name = models.CharField(default="", max_length=512)

    def __str__(self):
        return self.name.title()


class WikiPrevention(models.Model):
    name = models.CharField(default="", max_length=512)

    def __str__(self):
        return self.name.title()


class WikiDiagnosticMethod(models.Model):
    name = models.CharField(default="", max_length=512)

    def __str__(self):
        return self.name.title()


class WikiMedication(models.Model):
    name = models.CharField(default="", max_length=512)

    def __str__(self):
        return self.name.title()


class WikiSpecialty(models.Model):
    name = models.CharField(default="", max_length=512)

    def __str__(self):
        return self.name.title()


class WikiCause(models.Model):
    name = models.CharField(default="", max_length=512)

    def __str__(self):
        return self.name.title()


class WikiDisease(models.Model):
    """
        This class represents the 'endpoint' in the wikipedia parsing pipeline. Entries in this table 
        are considered complete.
        
        I expect almost all the many to many's to have at most one entry, but it was
        designed this way to handle potentially conflicting information. It IS Wikipedia
        after all. And then I might be able to extend this model for pubmed too
    """
    name = models.CharField(default="", max_length=255, unique=True)
    other_names = models.TextField(default="")
    icd10 = models.CharField(null=True, max_length=64)
    specialty = models.ManyToManyField(WikiSpecialty)
    frequency = models.ForeignKey(WikiFrequency, null=True, on_delete=models.SET_NULL)
    mortality_rate = models.ForeignKey(WikiCaseFatalityRate, null=True, on_delete=models.SET_NULL)
    case_fatality_rate = models.ForeignKey(WikiMortalityRate, null=True, on_delete=models.SET_NULL)
    deaths = models.ForeignKey(WikiDeath, null=True, on_delete=models.SET_NULL)
    symptoms = models.ManyToManyField(WikiSymptom)
    risk_factors = models.ManyToManyField(WikiRiskFactor)
    treatments = models.ManyToManyField(WikiTreatment)
    preventions = models.ManyToManyField(WikiPrevention)
    diagnostic_methods = models.ManyToManyField(WikiDiagnosticMethod)
    medications = models.ManyToManyField(WikiMedication)
    causes = models.ManyToManyField(WikiCause)
    #duration? usual onset? types?
    # TODO: Differential Diagnosis should be scrapable

    def __str__(self):
        return self.name

    def to_dict(self):

        specialty = self.specialty.all().first()
        frequency = self.frequency
        deaths = self.deaths

        if self.mortality_rate:
            mortality_rate = self.mortality_rate.display_value()
        elif deaths and deaths.frequency_int and frequency and frequency.frequency_int and frequency.frequency_int is not 0:
            mortality_rate = deaths.frequency_int / frequency.frequency_int
            mortality_rate = unit_rule(100 * mortality_rate)
        else:
            mortality_rate = 'Unknown'

        return {
            'id': self.id,
            'name': self.name,
            'icd10': self.icd10,
            'specialty': specialty.name if specialty else 'Unknown',
            'frequency': frequency.display_value() if frequency else 'Unknown',
            'deaths': deaths.display_value() if deaths else 'Unknown',
            'mortality_rate': mortality_rate
        }

    def print(self):
        print("======================================================")
        print(self.name)
        print(self.specialty)
        print(self.frequency)
        print(self.mortality_rate)
        print(self.case_fatality_rate)
        print(self.deaths)
        print(self.symptoms)
        print(self.risk_factors)
        print(self.treatments)
        print(self.preventions)
        print(self.diagnostic_methods)
        print(self.medications)
        print(self.causes)
        print("=====================================================")


def unit_rule(val) -> str:
    if val == 0:
        return "0.0000 %"
    if val < 1E-8:
        return f"{round(val*1E9,4)} n%"
    if val < 1E-5:
        return f"{round(val*1E6,4)} µ%"
    if val < 1E-2:
        return f"{round(val*1E3,4)} m%"
    return f"{round(val,4)} %"


