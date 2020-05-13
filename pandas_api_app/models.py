from django.db import models
from django_pandas.managers import DataFrameManager
from django.contrib.postgres.fields import JSONField
# Create your models here.
class Covid(models.Model):
    observationdate = models.CharField(max_length=300)
    state = models.CharField(max_length=300)
    country = models.CharField(max_length=300)
    lastupdate = models.CharField(max_length=300)
    confirmed = models.FloatField(max_length=300)
    death = models.FloatField(max_length=300)
    recovered = models.FloatField(max_length=300)
    objects = DataFrameManager()

class Titanic(models.Model):
    survived = models.IntegerField() 
    pclass   = models.IntegerField()        
    name     = models.CharField(max_length=200)  
    sex      = models.CharField(max_length=200)
    age      = models.FloatField() 
    sibsp    = models.FloatField() 
    parch    = models.FloatField()
    ticket   = models.CharField(max_length=200)
    fare     = models.FloatField()
    cabin    = models.CharField(max_length=200)
    embarked = models.CharField(max_length=200)
    objects = DataFrameManager()

class TitanicJson(models.Model):
    data_json = JSONField()

class CovidJson(models.Model):
    data_json = JSONField()