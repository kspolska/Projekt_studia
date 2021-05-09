from django import forms
from .models import *
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
import datetime
import re


class ContactForm(forms.ModelForm):
	user = forms.CharField()
	class Meta:
		#tworzenie daty 
		BIRTH_YEAR_CHOICES = []
		now = datetime.datetime.now()
		for i in range(120) :
			BIRTH_YEAR_CHOICES.append(now.year-i)

		#validacja numeru telefonu
		regex =re.compile("\d(9)")
		model = Dane_osoba

		fields  = [ 'id','imie','nazwisko','user','haslo','data_urodzenia','email','nr_telefonu','pesel','is_active']

		widgets = {'id': forms.HiddenInput(), 'haslo':forms.PasswordInput(), 'data_urodzenia':forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES), 'email':forms.TextInput ,'is_active': forms.HiddenInput(),}



class GlosyForm(forms.ModelForm):
	class Meta:
		model = Glosy
		
		fields = ['ustawa', 'glosujacy']
		widgets = {'glosujacy': forms.HiddenInput(), 'ustawa': forms.HiddenInput()}

class WynikiForm(forms.ModelForm):
	class Meta:
		model=Wyniki
		fields = '__all__'