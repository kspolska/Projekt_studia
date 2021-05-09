from django.db import models
from django.contrib.auth.models import User

class Ustawy(models.Model):

	index=models.IntegerField(primary_key=True)
	rok=models.IntegerField(null=True)
	nr_ustawy=models.IntegerField(null=True)
	tytul=models.TextField(null=True)
	link=models.TextField(null=True)
	nr_importu=models.IntegerField(null=True)

	def __str__(self):
		return str(self.index)

	class Meta:
		db_table="ustawy"



class Dane_osoba(models.Model):
	id=models.OneToOneField(User, on_delete=models.CASCADE, db_column='id_osoby', primary_key=True)
	imie=models.CharField(max_length=30, null=True)
	nazwisko=models.CharField(max_length=50, null=True)
	user=models.CharField(max_length=50, null=True)
	haslo=models.CharField(max_length=250, null=True)
	data_urodzenia=models.DateField(null=True)
	email=models.CharField(max_length=70, null=True)
	nr_telefonu=models.CharField(max_length=9, null=True)
	pesel=models.CharField(max_length=11, null=True)
	is_active=models.BooleanField(null=True)
	
	def __str__(self):
		return str(self.ustawa.index) 
	class Meta:
		db_table="dane_osoba"


class Glosy(models.Model):	
	id_glosu=models.AutoField(primary_key=True)
	ustawa=models.ForeignKey(Ustawy, null=True, on_delete=models.SET_NULL, db_column='ustawa')
	glosujacy=models.ForeignKey(Dane_osoba, null=True, on_delete=models.SET_NULL, db_column='glosujacy')

	def __str__(self):
		return str(self.ustawa.index) 
	class Meta:
		db_table="glosy"

class Wyniki(models.Model):
	id_wyniku=models.IntegerField(primary_key=True)
	ustawa=models.ForeignKey(Ustawy, null=True, on_delete=models.SET_NULL, db_column='ustawa')
	wynik_tak=models.IntegerField(null=True)
	wynik_nie=models.IntegerField(null=True)
	wynik_wstrzymany=models.IntegerField(null=True)
	class Meta:
		db_table="wyniki"

