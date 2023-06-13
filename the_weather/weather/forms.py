from django.forms import ModelForm, TextInput
from .models import City,Alert
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
#pythonfrom .models import Alert

class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {'name' : TextInput(attrs={'class' : 'input', 'placeholder' : 'city Name'})}

        
class UserRegister(UserCreationForm):

    class Meta:
        model=User
        fields=['username','first_name','last_name','email']


class AlertForm(forms.ModelForm):
    class Meta:
        model = Alert
        fields = ['alert_name', 'city_names', 'condition', 'threshold']
        widgets = {
            'alert_name': forms.Select(attrs={'class': 'form-control'}),
            'city_names': forms.Select(attrs={'class': 'form-control'}),
            'condition': forms.Select(attrs={'class': 'form-control'}),
            'threshold': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter threshold value'}),
        }