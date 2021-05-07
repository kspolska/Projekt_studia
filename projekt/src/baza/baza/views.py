from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse
from .forms import *
from django.db import connection
from django.contrib.auth import	authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages

from django.contrib.auth.decorators import login_required


def Start(request):
	print('test1')
	if request.method == 'POST':
		
		username = request.POST.get('user')
		password = request.POST.get('haslo')
		password = make_password(password)
		print('username',username)
		print('password',password)
		user = authenticate(request	, username=username, password=password)
		print('user',user)
		if user is not None:
			login(request, user)
			return redirect('StronaGlowna')
		else:
			messages.info(request, ' Nazwa urzydkownika lub haslo nie poprawne!')
	context ={}
	return render(request, "Start.html", context)


@login_required(login_url='home')
def StronaGlowna(request):
	return render(request, "StronaGlowna.html")

def zakladanie_konta(request):
	form=ContactForm()
	if request.method == 'POST':
		kopia_request = request.POST.copy()
		csrfmiddlewaretoken = kopia_request['csrfmiddlewaretoken']




		imie = kopia_request['imie']
		nazwisko = kopia_request['nazwisko']

		# Walidacja Hasła
		haslo = kopia_request['haslo']
		if ( len(haslo)<8):
			error_message ="Podany haslo jest za krótkie, pamiętaj o tym aby używać silnych haseł. To takie które zawierają małe i duże litery, znaki specjalne i cyfry!"
			return blad(request, error_message)
		moc_hasla=0	
		if (re.search("[a-z]",haslo)):
			moc_hasla+=1
		if (re.search("[A-Z]",haslo)):
			moc_hasla+=1
		if (re.search("[0-1]",haslo)):
			moc_hasla+=1
		if ((re.search("[!@#$%^&*()]",haslo))):
			moc_hasla+=1

		if(moc_hasla<3):
			error_message ="Haslo jest za słabe, pamiętaj o tym aby używać silnych haseł - to takie które zawierają małe i duże litery, znaki specjalne i cyfry!"
			return blad(request, error_message)

		kopia_request['haslo'] = make_password(haslo)

		print(haslo)
		#spradzanie hasla
		print(check_password(haslo,kopia_request['haslo']))  # returns True
		print(kopia_request['haslo'])

		# Walidacja nazwy usera
		user=kopia_request['user']

		query_user = "SELECT  dane_osoba.user FROM dane_osoba where dane_osoba.user = '{0}'".format(user)
		with connection.cursor() as cursor:
			cursor.execute(query_user)
			results_user = cursor.fetchall()
		if(len(results_user) > 0):
			error_message ="Podany user już istnieje"
			return blad(request, error_message)

		# przygotowywanie daty urodzenia do wstawienia go w formularz
		data_urodzenia_month = kopia_request['data_urodzenia_month']
		data_urodzenia_day = kopia_request['data_urodzenia_day']
		data_urodzenia_year = kopia_request['data_urodzenia_year']

		#walidacja adresu email
		email = kopia_request['email']

		query_email = "SELECT  dane_osoba.email FROM dane_osoba where dane_osoba.email = '{0}'".format(email)
		with connection.cursor() as cursor:
			cursor.execute(query_email)
			results_email = cursor.fetchall()
		if(len(results_email) > 0):
			error_message ="Podany email jest już w użyciu, użyj innego adresu"
			return blad(request, error_message)

		#Walidacja numer telefonu
		nr_telefonu = kopia_request['nr_telefonu']
		if ( len(nr_telefonu)<9):
			error_message ="Podany nr telefonu jest za krótki!"
			return blad(request, error_message)
		
		valid = re.compile('[0-9]{9}')
		if not(valid.match(nr_telefonu)):
			error_message ="Podany nr telefonu zawiera niedozwolony znak!"
			return blad(request, error_message)

		
		query_nr_telefonu = "SELECT  dane_osoba.nr_telefonu FROM dane_osoba where dane_osoba.nr_telefonu = '{0}'".format(nr_telefonu)
		with connection.cursor() as cursor:
			cursor.execute(query_nr_telefonu)
			results_nr_telefonu = cursor.fetchall()
		if(len(results_nr_telefonu) > 0):
			error_message ="Podany nr_telefonu jest już w użyciu, użyj innego numeru"
			return blad(request, error_message)

		#Walidacja adresu pessel 
		pesel = kopia_request['pesel']

		valid = re.compile('[0-9]{11}')
		if not(valid.match(pesel)):
			error_message ="Podany nr PESEL zawiera niedozwolony znak!"
			return blad(request, error_message)
		if ( len(pesel)<11):
			error_message ="Podany nr PESSEL jest za krótki!"
			return blad(request, error_message)
		
		query_pesel = "SELECT  dane_osoba.pesel FROM dane_osoba where dane_osoba.pesel = '{0}'".format(pesel)
		with connection.cursor() as cursor:
			cursor.execute(query_pesel)
			results_pesel = cursor.fetchall()
		if(len(results_pesel) > 0):
			error_message ="Podany nr PESSEL jest już w użyciu, jeśli jesteś jego posiadaczem, skontatkuj się z administratorem sieci za pośrednictwem maila na adres : pomoc@twojref.pl"
			return blad(request, error_message)
		now = datetime.datetime.now()
		valid_day=re.compile('[1-2][0-9]|[0][1-9]|[3][0-1]')

		valid_month=re.compile('[0][1-9]|[1][0-2]')		
		valid_month_nowe=re.compile('[2][1-9]|[3][0-2]')

		valid_year=re.compile('[0-9][0-9]')
		valid_year_nowe=re.compile('[0-1][0-9]|[2][0-1]')
		day_check = str(pesel[4])+str(pesel[5])
		month_check = str(pesel[2])+str(pesel[3])
		year_check=str(pesel[0])+str(pesel[1])

		#walidacja dnia
		if not (valid_day.match(day_check)):
			error_message ="Niepoprawny adres PESEL!"
			return blad(request, error_message)
		#walidacja miesiąca
		if not ((valid_month.match(month_check)) or ( valid_month_nowe.match(month_check) and valid_year_nowe.match(year_check) ) ):

			error_message ="Niepoprawny adres PESEL!"
			return blad(request, error_message)

		# poniżej dalsza część pesel po ustaleniu jaka jest data dla formularza
		#obliczanie daty od formularza

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
		# koniec daty do formularza
		if not(day_check==str((data_uro[8])+str(data_uro[9]))):
			error_message ="PESEL jest niezgodny z datą urodzenia!"
			return blad(request, error_message)
		if not(year_check==str((data_uro[2])+str(data_uro[3]))):
			error_message ="PESEL jest niezgodny z datą urodzenia!"
			return blad(request, error_message)	
		mantch_for_check_pesel=(int(data_uro[5])*10)+int(data_uro[6])+20
		if not(month_check==str((data_uro[5])+str(data_uro[6])) or (month_check!=mantch_for_check_pesel)): 
			error_message ="PESEL jest niezgodny z datą urodzenia!"
			return blad(request, error_message)


		#Walidacja liczby kontorlnej
		kontrolna = (int(pesel[0])*1)%10	
		kontrolna = kontrolna +(int(pesel[1])*3)%10
		kontrolna = kontrolna +(int(pesel[2])*7)%10
		kontrolna = kontrolna +(int(pesel[3])*9)%10
		kontrolna = kontrolna +(int(pesel[4])*1)%10
		kontrolna = kontrolna +(int(pesel[5])*3)%10
		kontrolna = kontrolna +(int(pesel[6])*7)%10
		kontrolna = kontrolna +(int(pesel[7])*9)%10
		kontrolna = kontrolna +(int(pesel[8])*1)%10
		kontrolna = kontrolna +(int(pesel[9])*3)%10
		kontrolna = kontrolna%10
		print('10-kontrolna', (10-kontrolna))
		print('int(pesel[10])', int(pesel[10]))
		print('(10-kontrolna == int(pesel[10]))%10', (10-kontrolna == int(pesel[10]))%10)
		if not ((10-kontrolna)%10 == int(pesel[10])):
			print(kontrolna)
			error_message ="PESEL jest niezgodny z datą urodzenia4 !"
			return blad(request, error_message)

		request.POST=kopia_request


		form=ContactForm(data = request.POST)

		print(form.errors)
		if form.is_valid():
			form.save()
			print("user zapisany")
			return Utworzono(request)

	return render(request, "zakladanie_konta.html",{"data":form})


def blad(request, er):
	return render(request, "blad.html",{'error':er})


def Utworzono(request):
	return render(request, "utworzono.html")

@login_required(login_url='home')
def Statystyki(request):
	return render(request, "Statystyki.html")

@login_required(login_url='home')
def Roczniki(request):
	return render(request, "Roczniki.html")

@login_required(login_url='home')
def Regulamin(request):
	return render(request, "Regulamin.html")

@login_required(login_url='home')
def Projekt(request):
	return render(request, "Projekt.html")

@login_required(login_url='home')
def Omnie(request):
	return render(request, "Omnie.html")

@login_required(login_url='home')
def Kontakt(request):
	return render(request, "Kontakt.html")

@login_required(login_url='home')
def rocznik(request , lata):
	results=Ustawy.objects.all()
	return render(request, 'Ustawy_roczniki.html', {"data":results , "rokcznik":lata})

@login_required(login_url='home')
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

@login_required(login_url='home')
def Wyniki_glosowania(request, id):
	ust=Ustawy.objects.get(index=id)
	wynik=Wyniki.objects.get(ustawa=ust)
	
	return render(request, "Wyniki_glosowania.html", {'wyniki':wynik , 'ust':ust} )