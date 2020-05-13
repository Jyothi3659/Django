import datetime
import random

from django.core.management.base import BaseCommand

from pandas_api_app.models import Covid, Titanic
from pandas_api_app.views import *
import pandas as pd
import os
import numpy as np

# import ipdb; ipdb.set_trace()
custom_command_path = os.path.dirname(__file__)
# PROJECT_ROOT = os.path.abspath(os.path.dirname(settings_dir))
# python_file_path = os.getcwd()
# python_file_path = os.path.abspath('titanic_data.py')
base_url = '/'.join(custom_command_path.split('/')[:-2])
media_url = '/media/train.csv'
final_url = base_url + media_url
df_titanic = pd.read_csv(final_url)
del df_titanic['PassengerId']
df_titanic = df_titanic.rename(columns = {'Survived':'survived','Pclass':'pclass','Name':'name','Sex':'sex','Age':'age','SibSp':'sibsp','Parch':'parch','Ticket':'ticket','Fare':'fare','Cabin':'cabin','Embarked':'embarked'})
df_titanic = df_titanic.replace(np.nan,0)
class Command(BaseCommand):
    def handle(self, *args, **options):
        record = []
        for column, row in df_titanic.iterrows():
            # student_record.(dict(row))
            titanic_record = Titanic(**dict(row))
            self.stdout.write(self.style.SUCCESS(type(titanic_record)))
            # student_record.append(dict(row))
            record.append(titanic_record)
        # self.stdout.write(self.style.SUCCESS(student_record))        
        Titanic.objects.bulk_create(record)
        self.stdout.write(self.style.SUCCESS('data populated sucselfessfully'))
        