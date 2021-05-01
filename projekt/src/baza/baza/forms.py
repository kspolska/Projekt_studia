from django import forms
from .models import *
from django.forms import ModelForm




class ContactForm(forms.ModelForm):
	class Meta:
		model = Dane_osoba
		fields  =  '__all__'


class GlosyForm(forms.ModelForm):
	class Meta:
		model=Glosy
		fields = '__all__'