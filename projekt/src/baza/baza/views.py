from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse
from .forms import Dane_osoba
from .forms import GlosyForm

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

def rocznik(request , lata):
	results=Ustawy.objects.all()
	return render(request, 'Ustawy_roczniki.html', {"data":results , "rokcznik":lata})

def glosowanie(request):
	form = GlosyForm()
	print('TEST!!!!!!!!!!:')
	#if request.method == 'POST':
	print('Printing POST:', request.POST)
	form = GlosyForm(request.POST)
	if form.is_valid():
		print('Udalo sie!!!!!!!!!!:')
		form.save()
		return redirect ('/')
	context = {'form1':form}
	return render(request, 'oddajglos.html',context)
