import datetime
import random

from django.core.management.base import BaseCommand

from pandas_api_app.models import Covid, Titanic
from pandas_api_app.views import *
import pandas as pd
import os
import json

class Command(BaseCommand):
    def handle(self, *args, **options):
        # import ipdb; ipdb.set_trace()
        titanicjson = TitanicJsonView()
        data_dict = titanicjson.titanicdata()
        record = []   
        for each in data_dict:

            titanic_record = TitanicJson(data_json = json.dumps(data_dict))
            # self.stdout.write(self.style.SUCCESS(type(titanic_record)))
            record.append(titanic_record)
        # self.stdout.write(self.style.SUCCESS(student_record))        
        TitanicJson.objects.bulk_create(record)
        self.stdout.write(self.style.SUCCESS('data populated sucessfully'))