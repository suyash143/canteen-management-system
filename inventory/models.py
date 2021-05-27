from django.db import models


class Supplies(models.Model):
    name=models.CharField(max_length=500,null=True,blank=True)
    stock=models.FloatField(null=True,blank=True)
    minimum=models.FloatField(null=True,blank=True)
    created = models.DateTimeField(null=True)
