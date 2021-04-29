from django.shortcuts import render
from .models import Ustawy
from .models import Dane_osoba
from django.http import HttpResponse

from .forms import Dane_osoba

import numpy as numpy

def home_view(request):
	 return HttpResponse("Hello!") 

def Start(request):
	return render(request, "Start.html")

def StronaGlowna(request):
	return render(request, "StronaGlowna.html")

def zakladanie_konta(request):
	results=Dane_osoba.objects.all()
	return render(request, "zakladanie_konta.html",{"data":results})

def Statystyki(request):
	return render(request, "Statystyki.html")

def Roczniki(request):
	return render(request, "Roczniki.html")

def Regulamin(request):
	return render(request, "Regulamin.html")

def Projekt(request):
	return render(request, "Projekt.html")

def Omnie(request):
	return render(request, "Omnie.html")

def Kontakt(request):
	return render(request, "Kontakt.html")
def base(request):
	form = Dane_osoba()
	return render(request, "base.html",{"form":form})

def post_new(request):
    form = Dane_osoba()
    return render(request, 'base.html', {'form': form})
def rocznik(request , lata):
	#lata = [ '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020','2021']
	results=Ustawy.objects.all()
	#dane_z_bazy = Ustawy.objects.all(numpy.unique(rok = lata))
	return render(request, 'Ustawy_roczniki.html', {"data":results , "rokcznik":lata})
#def main_base(request):
#	return render(request, "main_base.html")

#def main_base_page(request):
#	return render(request, "main_base_page.html")