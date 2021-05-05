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
	form=ContactForm()
	if request.method == 'POST':
		kopia_request = request.POST.copy()
		csrfmiddlewaretoken = kopia_request['csrfmiddlewaretoken']





		imie = kopia_request['imie']
		nazwisko = kopia_request['nazwisko']
		haslo = kopia_request['haslo']
		data_urodzenia_month = kopia_request['data_urodzenia_month']
		data_urodzenia_day = kopia_request['data_urodzenia_day']
		data_urodzenia_year = kopia_request['data_urodzenia_year']
		email = kopia_request['email']
		nr_telefonu = kopia_request['nr_telefonu']
		PESEL = kopia_request['PESEL']
		if(len(str(data_urodzenia_month))==1 and len(str(data_urodzenia_day))==1):
			data_uro = str(data_urodzenia_year)+'-0'+str(data_urodzenia_month)+'-0'+str(data_urodzenia_day)
		if (len(str(data_urodzenia_month))==1 and len(str(data_urodzenia_day))>1):
			data_uro = str(data_urodzenia_year)+'-0'+str(data_urodzenia_month)+'-'+str(data_urodzenia_day)
		if(len(str(data_urodzenia_month))>1 and len(str(data_urodzenia_day))==1):
			data_uro = str(data_urodzenia_year)+'-'+str(data_urodzenia_month)+'-0'+str(data_urodzenia_day)
		if(len(str(data_urodzenia_month))>1 and len(str(data_urodzenia_day))>1):
			data_uro = str(data_urodzenia_year)+'-'+str(data_urodzenia_month)+'-'+str(data_urodzenia_day)
		kopia_request.pop('data_urodzenia_month')
		kopia_request.pop('data_urodzenia_day')
		kopia_request.pop('data_urodzenia_year')
		kopia_request['data_urodzenia']=data_uro

		request.POST=kopia_request
		print(request.POST)

		form=ContactForm(data = request.POST)

		print(form.errors)
		if form.is_valid():
			form.save()
			print("user zapisany")
	return render(request, "zakladanie_konta.html",{"data":form})

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