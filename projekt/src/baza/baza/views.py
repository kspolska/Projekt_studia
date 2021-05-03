from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse
from .forms import *
from django.db import connection

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
	id_uzytkownika = str(1)
	#Numer ustawy na ktora oddany jest glos
	nr_ustawy=str(Ustawy.objects.get(index=id))
	ustawa=Ustawy.objects.get(index=id)
	#Sprawdzenie w bazie czy user glosowal
	check =0
	query_isdone = "SELECT COUNT(*) FROM glosy WHERE glosujacy = {0} and ustawa = {1}".format(id_uzytkownika, nr_ustawy)
	with connection.cursor() as cursor:
		cursor.execute(query_isdone)
		results = cursor.fetchall()
		check=results[0][0]
	if(results[0][0] > 0):
		print("Brak mozliwosci glosowania")


	#Dodanie do requesta znanych wczesniej wartosci
	data = request.POST.copy()
	data['ustawa'] = nr_ustawy
	data['glosujacy'] = id_uzytkownika

	#Nowy formularz z pełnymi danymi
	form = GlosyForm(data)

	if request.method == 'POST':
		print('Printing POST:', request.POST)

		#Aktualizacje tabeli wyniki
		if "Za" in str(request.POST):
			query = "UPDATE wyniki set wynik_tak = wynik_tak + 1 where ustawa = "+ str(nr_ustawy)
			with connection.cursor() as cursor:
				cursor.execute(query)
			print("Za!")
		if "Przeciw" in str(request.POST):
			query = "UPDATE wyniki set wynik_nie = wynik_nie + 1 where ustawa = "+ str(nr_ustawy)
			with connection.cursor() as cursor:
				cursor.execute(query)
			print("Przeciw!")
		if "Wstrzymuje" in str(request.POST):
			print("Wstrzymuje!")
			query = "UPDATE wyniki set wynik_wstrzymany = wynik_wstrzymany + 1 where ustawa = "+ str(nr_ustawy)
			with connection.cursor() as cursor:
				cursor.execute(query)

		if form.is_valid():
			instance = form.save()
			return redirect ('/StronaGlowna')

	context = {'form':form , 'ustawa':nr_ustawy, 'dane':ustawa, 'check':check  }

	return render(request, 'oddajglos.html', context)

def Wyniki_glosowania(request, id):
	ust=Ustawy.objects.get(index=id)
	wynik=Wyniki.objects.get(ustawa=ust)
	
	return render(request, "Wyniki_glosowania.html", {'wyniki':wynik , 'ust':ust} )