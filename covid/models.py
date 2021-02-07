from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=128, default="")
    #parent = models.ForeignKey("self", null=True, on_delete=models.PROTECT)

    def __str__(self):
        if self.parent:
            return f"{self.name},{self.parent.name}"
        return f"{self.name}"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'parent': self.parent.name if self.parent else None
        }

'''
class Cases(models.Model):
    region = models.ForeignKey(Region, null=False, on_delete=models.PROTECT)
    date = models.DateTimeField()
    cumulative = models.IntegerField(default=0)

    def to_dict(self):
        return {
            'date': self.date,
            'cumulative': self.cumulative
        }


class Deaths(models.Model):
    region = models.ForeignKey(Region, null=False, on_delete=models.PROTECT)
    date = models.DateTimeField()
    cumulative = models.IntegerField(default=0)

'''