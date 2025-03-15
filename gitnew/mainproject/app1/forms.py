from django import forms
from.models import *
class normal_form(forms.Form):
    doctorname = models.CharField(max_length=30)
    phoneno = models.IntegerField()
    department = models.CharField(max_length=40)
    image = models.ImageField()

class model_form(forms.ModelForm):
    class Meta:
        model=add_doctor
        fields='__all__'


class normal_form2(forms.Form):
    treatmentname = models.CharField(max_length=30)
    about = models.CharField(max_length=200)
    logo = models.ImageField()


class model_form2(forms.ModelForm):
    class Meta:
        model=add_treatment
        fields='__all__'