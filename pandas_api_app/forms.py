from django import forms
from .models import *
class TitanicForm(forms.ModelForm):
    class Meta:
        model = Titanic
        fields = '__all__'
