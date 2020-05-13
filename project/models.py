from django.db import models
from django.contrib.auth.models import User
# Create your models here.
project_status_choices = ((1, 'Open'),(2, 'In progress'),(3, 'verified'),(4, 'To verify'),(5, 'closed'))
class BaseContent(models.Model):
    active= models.IntegerField(default = 2)
    created= models.DateTimeField(auto_now_add=True)
    modified= models.DateField(auto_now=True)

class Activity(BaseContent):
    start_date = models.DateField()
    end_date = models.DateField()
    project_status = models.IntegerField(null= True, choices=project_status_choices)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank = True, null=True)

class MileStone(BaseContent):
    project = models.ForeignKey('Activity', on_delete=models.DO_NOTHING ,blank =True,null =True)
    start = models.DateField()
    end = models.DateField()

class ProjectWeightage(BaseContent):
    weightage = models.FloatField()
