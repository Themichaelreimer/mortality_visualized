from django.db import models
from django.utils import timezone


# Create your models here.
class StatisticType(models.Model):
    """ This class represents categories for numerical data """
    OPTIONS = [
        'mortality',
        'frequency',
        'incidence',
        'deaths',
    ]
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'statistic_type'

CATEGORY_TYPES = [
    ('symptom', 'symptom'),
    ('treatment', 'treatment'),
]
class CategoryType(models.Model):
    """ Defines categorical data categories. Eg: Symptoms, risk factors, treatments"""
    name = models.CharField(max_length=255, choices=CATEGORY_TYPES)

    class Meta:
        db_table = 'category_type'


class Citation(models.Model):
    """ Defines a citation. Eg: (Wikipedia, 2021, http://en.wikipedia.org/...) """
    source_name = models.CharField(max_length=255)
    link = models.TextField(default='')
    timestamp = models.DateTimeField(default=timezone.now)

    def to_html(self) -> str:
        """ Returns the html for the citation """
        return f'''
            <a href="{self.link}"> ({self.source_name}, {self.timestamp.strftime('%Y')}) </a>
        '''

    class Meta:
        db_table = 'statistic_citation'


class CategoricalValue(models.Model):
    """ Defines a category as having a value. Eg: (Symptom, 'Cough')"""
    category_type = models.ForeignKey(CategoryType, on_delete=models.CASCADE)
    value = models.CharField(max_length=255, default='')


class Disease(models.Model):
    """
        This class implements a model of a disease. A disease has some identifiers (name, ICD),
        and some categorical and numerical data.
    """
    name = models.CharField(default="", max_length=255, unique=True)
    other_names = models.TextField(default="")
    icd10 = models.CharField(null=True, max_length=64)
    differential_diagnosis = models.ManyToManyField('Disease')  # Diseases a disease could be confused with
    # statistics are a many-to-one relationship implemented via a foreign key on Statistic

    def to_dict(self) -> dict:
        # TODO: Look at how model_to_dict handles many_to_many fields, might be ideal
        return {
        }


class CategoricalTag(models.Model):
    """
    This class represents a categorical data point
    : ('Flu', ('Symptom', 'malaise'), (Wikipedia, 2021))
    """
    categorical_value = models.ForeignKey(CategoricalValue, on_delete=models.CASCADE)
    citation = models.ForeignKey(Citation, on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)


class Statistic(models.Model):
    """
    This class represents a numerical data point.
    Eg: (mortality rate, 0.05, (Wikipedia, 2021))
    """
    statistic_type = models.ForeignKey(StatisticType, on_delete=models.CASCADE)
    citation = models.ForeignKey(Citation, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=5)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)

    class Meta:
        db_table = 'statistic'
