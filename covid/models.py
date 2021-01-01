from django.db import models

class Region(models.model):
    name = models.CharField(length=128, default="")
    parent = models.ForeignKey("self", null=True, on_delete=models.PROTECT)

class Cases(models.model):
    region = models.ForeignKey(Region, null=False, on_delete=models.PROTECT)
    date = models.DateTimeField()
    cumulative = models.IntegerField(default=0)

class Deaths(models.model):
    region = models.ForeignKey(Region, null=False, on_delete=models.PROTECT)
    date = models.DateTimeField()
    value = models.IntegerField(default=0)
