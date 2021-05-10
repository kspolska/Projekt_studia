from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse
from .forms import *
from django.db import connection
from django.contrib.auth import	authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from random import seed
from random import randint


def Start(request):
	if request.method == 'POST':
		
		username = request.POST.get('user')
		password = request.POST.get('haslo')
		
		user = authenticate(request	, username=username, password=password)
	
		if user is not None:
			login(request, user)
			osoba=Dane_osoba.objects.get(user=username)			
			if(str(osoba.is_active)=="False"):
				return redirect('weryfikacja')
			return redirect('home_page')
		else:
			messages.info(request, ' Nazwa urzydkownika lub haslo nie poprawne!')
	context ={}
	return render(request, "Start.html", context)


def wyloguj(request):
	logout(request)
	return redirect('home')

@login_required(login_url='home')
def StronaGlowna(request):
	return render(request, "StronaGlowna.html")

def zakladanie_konta(request):
	
	#Przypisanie formularza do zmiennej form
	form=ContactForm()

	if request.method == 'POST':

		kopia_request = request.POST.copy()

		# Walidacja nazwy usera
		username=kopia_request['user']
		query_user = "SELECT  dane_osoba.user FROM dane_osoba where dane_osoba.user = '{0}'".format(username)
		with connection.cursor() as cursor:
			cursor.execute(query_user)
			results_user = cursor.fetchall()
		if(len(results_user) > 0):
			error_message ="Podany user już istnieje"
			return blad(request, error_message)



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

		#hashowanie hasła
		kopia_request['haslo'] = make_password(haslo)
		

		# przygotowywanie daty urodzenia do wstawienia go w formularz
		data_urodzenia_month = kopia_request['data_urodzenia_month']
		data_urodzenia_day = kopia_request['data_urodzenia_day']
		data_urodzenia_year = kopia_request['data_urodzenia_year']

		#walidacja adresu email
		email = kopia_request['email']

		#zbadanie czy podae email istnieje już w bazie danych
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

		#zbadanie czy podae nr telefonu istnieje już w bazie danych
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

		#zbadanie czy podae PESEL istnieje już w bazie danych
		query_pesel = "SELECT  dane_osoba.pesel FROM dane_osoba where dane_osoba.pesel = '{0}'".format(pesel)
		with connection.cursor() as cursor:
			cursor.execute(query_pesel)
			results_pesel = cursor.fetchall()
		if(len(results_pesel) > 0):
			error_message ="Podany nr PESSEL jest już w użyciu, jeśli jesteś jego posiadaczem, skontatkuj się z administratorem sieci za pośrednictwem maila na adres : pomoc@twojref.pl"
			return blad(request, error_message)
		now = datetime.datetime.now()

		#walidatory daty
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
		
		# Zbadanie czy data urodzenia jest zgodna z PESEL
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


		#Walidacja liczby kontorlnej w PESEL
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
		
		if not ((10-kontrolna)%10 == int(pesel[10])):
			error_message ="PESEL jest niezgodny z datą urodzenia !"
			return blad(request, error_message)

		#dodanie flagi o tym że user jest nie aktywny
		kopia_request['is_active']=False
		
		#stworzenie usera w tabeli auth_user
		user = User.objects.create_user(username, first_name=imie, last_name=nazwisko, email=email, password=haslo)
		user_id = User.objects.get(username=username).pk
		
		#Nadanie tego samego id co w tabeli auth_user co w tabeli dane_osoba
		kopia_request['id'] = user_id

		#oprzypisanie zwalidowanych danych do requestu
		request.POST=kopia_request
		
		form=ContactForm(data = request.POST)

		#zapisanie danych do tabeli dane_osoba
		if form.is_valid():
			form.save()

			return Utworzono(request)

	return render(request, "zakladanie_konta.html",{"data":form})


def blad(request, er):
	return render(request, "blad.html",{'error':er})

def Weryfikacja_potwierdzenie(request, code):
	form=Dane_osoba.objects.get(id=request.user.id)	
	print('udalosie')
	if request.method == 'POST':
			klucz = request.POST.get('klucz')
			key=code
			print(klucz)
			print(code)
			if(klucz == key):
				form.is_active=True
				if form.is_valid():
					form.save()
					return redirect('home_page')
	return render(request, "weryfikacja.html", {'form1':form})


@login_required(login_url='home')
def Weryfikacja(request):
	
	form=Dane_osoba.objects.get(id=request.user.id)	
	
	if (str(form.is_active)=="False"):
		seed(randint(1000,9999))
		key=randint(1000,9999) 
		port = 465
		smtp_serwer ="smtp.gmail.com"
		nadawca = "TwojeReferendum.pl@gmail.com"
		odbiorca = form.email
		haslo ="qsisjvtjgarerfcs"

		wiadomosc = MIMEMultipart("alternative")
		wiadomosc["Subject"] = "Potwierdz swoj adres email w portalu TwojeReferendum"
		wiadomosc["From"] = "TwojeReferendum@gmail.com"
		wiadomosc["To"] = form.email


		text = "Klucz weryfikacyjny to :" + str(key)
		
		part1 = MIMEText(text, "plain")
		
		
		wiadomosc.attach(part1)

		
		ssl_pol = ssl.create_default_context()
		with smtplib.SMTP_SSL(smtp_serwer, port, context=ssl_pol) as serwer:
			serwer.login(nadawca, haslo)
			serwer.sendmail(nadawca, odbiorca, wiadomosc.as_string())
		print('wyslany')
		return Weryfikacja_potwierdzenie(request,key)

		
	return render(request, "weryfikacja.html", {'form1':form})

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
def glosowanie(request, id):

	# przypisanie usera który będzie głosował
	id_uzytkownika = request.user.id
	#Numer ustawy na ktora oddany jest glos
	nr_ustawy=str(Ustawy.objects.get(index=id))
	ustawa=Ustawy.objects.get(index=id)

	#Walidacja czy osoba jest pełnoletnia
	osoba=Dane_osoba.objects.get(id=request.user.id)
	wiek =int(str(osoba.data_urodzenia)[0]+str(osoba.data_urodzenia)[1]+str(osoba.data_urodzenia)[2]+str(osoba.data_urodzenia)[3]+str(osoba.data_urodzenia)[5]+str(osoba.data_urodzenia)[6]+str(osoba.data_urodzenia)[8]+str(osoba.data_urodzenia)[9])
	data_dzis =datetime.datetime.now()
	data_chek=int(str(data_dzis)[0]+str(data_dzis)[1]+str(data_dzis)[2]+str(data_dzis)[3]+str(data_dzis)[5]+str(data_dzis)[6]+str(data_dzis)[8]+str(data_dzis)[9])
	wiek = data_chek-wiek

	#Sprawdzenie w bazie czy user glosowal
	#Możliwość głosowania jest uruchamiana po stronie przeglądarki.
	check =0
	query_isdone = "SELECT COUNT(*) FROM glosy WHERE glosujacy = {0} and ustawa = {1}".format(id_uzytkownika, nr_ustawy)
	with connection.cursor() as cursor:
		cursor.execute(query_isdone)
		results = cursor.fetchall()
		check=results[0][0]
	#Dodanie do requesta znanych wczesniej wartosci
	data = request.POST.copy()
	data['ustawa'] = nr_ustawy
	data['glosujacy'] = id_uzytkownika

	#Nowy formularz z pełnymi danymi
	form = GlosyForm(data)

	if request.method == 'POST':
		

		#Aktualizacje tabeli wyniki
		if "Za" in str(request.POST):
			query = "UPDATE wyniki set wynik_tak = wynik_tak + 1 where ustawa = "+ str(nr_ustawy)
			with connection.cursor() as cursor:
				cursor.execute(query)
		if "Przeciw" in str(request.POST):
			query = "UPDATE wyniki set wynik_nie = wynik_nie + 1 where ustawa = "+ str(nr_ustawy)
			with connection.cursor() as cursor:
				cursor.execute(query)
		if "Wstrzymuje" in str(request.POST):
			query = "UPDATE wyniki set wynik_wstrzymany = wynik_wstrzymany + 1 where ustawa = "+ str(nr_ustawy)
			with connection.cursor() as cursor:
				cursor.execute(query)
		# dodanie rekordu do tabeli głosy
		if form.is_valid():
			instance = form.save()
			return redirect ('/StronaGlowna')

	context = {'form':form , 'ustawa':nr_ustawy, 'dane':ustawa, 'check':check,'wiek':wiek, 'osoba':osoba  }

	return render(request, 'oddajglos.html', context)

@login_required(login_url='home')
def Wyniki_glosowania(request, id):
	ust=Ustawy.objects.get(index=id)
	wynik=Wyniki.objects.get(ustawa=ust)
	
	return render(request, "Wyniki_glosowania.html", {'wyniki':wynik , 'ust':ust } )