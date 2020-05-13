import datetime
import random

from django.core.management.base import BaseCommand

from pandas_api_app.models import Covid
from pandas_api_app.views import *
import pandas as pd
import kaggle
import pandas as pd
# !kaggle datasets download -d sudalairajkumar/novel-corona-virus-2019-dataset
# !unzip \*.zip
import kaggle

kaggle.api.authenticate()

kaggle.api.dataset_download_files('sudalairajkumar/novel-corona-virus-2019-dataset', unzip=True)
df = pd.read_csv(r'covid_19_data.csv')
df = df.rename(columns={'ObservationDate' : 'observationdate', 'Province/State' : 'state', 'Country/Region': 'country', 'Last Update' : 'lastupdate','Confirmed' : 'confirmed','Deaths':'death','Recovered':'recovered'})
df = df.drop(columns=['SNo'])

class Command(BaseCommand):
    def handle(self, *args, **options):
        record = []
        for column, row in df.iterrows():
            # student_record.(dict(row))
            covid_record = Covid(**dict(row))
            self.stdout.write(self.style.SUCCESS(type(covid_record)))
            # student_record.append(dict(row))
            record.append(covid_record)
        # self.stdout.write(self.style.SUCCESS(student_record))        
        Covid.objects.bulk_create(record)
        self.stdout.write(self.style.SUCCESS('data populated sucessfully'))
        