from django.db import models

# Create your models here.


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

    def __str__(self):
        if self.frequency_int:
            return f"{self.frequency_int}"
        return f"{self.frequency_ratio}"


class WikiDeath(models.Model):
    region_name = models.CharField(default='', max_length=255)
    frequency_int = models.BigIntegerField(null=True)
    frequency_ratio = models.FloatField(null=True)

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

    def __str__(self):
        if self.frequency_int:
            return f"{self.frequency_int}"
        return f"{self.frequency_ratio}"


class WikiSymptom(models.Model):
    name = models.CharField(default="", max_length=255, unique=True)

    def __str__(self):
        return self.name


class WikiRiskFactor(models.Model):
    name = models.CharField(default="", max_length=255, unique=True)

    def __str__(self):
        return self.name


class WikiTreatment(models.Model):
    name = models.CharField(default="", max_length=255, unique=True)

    def __str__(self):
        return self.name


class WikiPrevention(models.Model):
    name = models.CharField(default="", max_length=255, unique=True)

    def __str__(self):
        return self.name


class WikiDiagnosticMethod(models.Model):
    name = models.CharField(default="", max_length=255, unique=True)

    def __str__(self):
        return self.name


class WikiMedication(models.Model):
    name = models.CharField(default="", max_length=255, unique=True)

    def __str__(self):
        return self.name


class WikiSpecialty(models.Model):
    name = models.CharField(default="", max_length=255, unique=True)

    def __str__(self):
        return self.name


class WikiCause(models.Model):
    name = models.CharField(default="", max_length=255, unique=True)

    def __str__(self):
        return self.name


class WikiDisease(models.Model):
    """
        This class represents the 'endpoint' in the wikipedia parsing pipeline. Entries in this table 		are considered complete.
        
        I expect almost all the many to many's to have at most one entry, but it was
        designed this way to handle potentially conflicting information. It IS Wikipedia
        after all. And then I might be able to extend this model for pubmed too
    """
    name = models.CharField(default="", max_length=255, unique=True)
    other_names = models.TextField(default="")
    specialty = models.ManyToManyField(WikiSpecialty)
    frequency = models.ManyToManyField(WikiFrequency)
    mortality_rate = models.ManyToManyField(WikiCaseFatalityRate)
    case_fatality_rate = models.ManyToManyField(WikiMortalityRate)
    deaths = models.ManyToManyField(WikiDeath)
    symptoms = models.ManyToManyField(WikiSymptom)
    risk_factors = models.ManyToManyField(WikiRiskFactor)
    treatments = models.ManyToManyField(WikiTreatment)
    preventions = models.ManyToManyField(WikiPrevention)
    diagnostic_methods = models.ManyToManyField(WikiDiagnosticMethod)
    medications = models.ManyToManyField(WikiMedication)
    causes = models.ManyToManyField(WikiCause)
    #duration? usual onset? types?

    def print(self):
        print("======================================================")
        print(self.name)
        print(self.specialty)
        print(self.frequency.all())
        print(self.mortality_rate.all())
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


