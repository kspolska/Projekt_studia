from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse
from .forms import *

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


# działające dodawnie do bazy danych
def glosowanie(request, id):
	ustawy=Ustawy.objects.get(index=id)
	form = GlosyForm(request.POST or None)
	if request.method == 'POST':
		form = GlosyForm(request.POST or None)
		print('Printing POST:', request.POST)
		if form.is_valid():
			form.save()
			return redirect ('/StronaGlowna')

	context = {'form':form}

	return render(request, 'oddajglos.html',context )

# aktualizowanie bazy tabeli wyniki
def glosowanie2(request, id):
	ustawy=Wyniki.objects.get(id_wyniku=id)
	form = WynikiForm(instance=ustawy)

	if request.method == 'POST':
		form = WynikiForm(request.POST or None , instance=ustawy)
		print('Printing POST:', request.POST)
		if form.is_valid():
			form.save()
			return redirect ('/StronaGlowna')

	context = {'form':form}

	return render(request, 'oddajglos.html',context )


#próba połączenia powyższych metod
