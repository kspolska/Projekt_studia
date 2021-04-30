from django.db import models

class Ustawy(models.Model):

	index=models.IntegerField(primary_key=True)
	rok=models.IntegerField(null=True)
	nr_ustawy=models.IntegerField(null=True)
	tytul=models.TextField(null=True)
	link=models.TextField(null=True)
	nr_importu=models.IntegerField(null=True)

	class Meta:
		db_table="ustawy"
 
class Dane_osoba(models.Model):
	id_osoby=models.IntegerField(primary_key=True)
	imie=models.CharField(max_length=30, null=True)
	nazwisko=models.CharField(max_length=50, null=True)
	haslo=models.CharField(max_length=50, null=True)
	data_urodzenia=models.DateField(null=True)
	email=models.CharField(max_length=70, null=True)
	nr_telefonu=models.IntegerField()
	plec=models.BooleanField(null=True)
	PESEL=models.TextField(null=True)
	class Meta:
		db_table="dane_osoba"

class Glosy(models.Model):	
	id_glosu=models.IntegerField(primary_key=True)
	ustawa=models.ForeignKey(Ustawy, null=True, on_delete=models.SET_NULL)
	glosujacy=models.ForeignKey(Dane_osoba, null=True, on_delete=models.SET_NULL)
	class Meta:
		db_table="glosy"

class Wyniki(models.Model):
	id_wyniku=models.IntegerField(primary_key=True)
	ustawa=models.ForeignKey(Ustawy, null=True, on_delete=models.SET_NULL)
	wynik_tak=models.IntegerField(null=True)
	wynik_nie=models.IntegerField(null=True)
	wynik_wstrzymany=models.IntegerField(null=True)
	class Meta:
		db_table="wyniki"

