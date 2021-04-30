CREATE TABLE "ustawy" (
	"index" serial NOT NULL,
	"rok" DATE NOT NULL,
	"nr_ustawy" integer NOT NULL,
	"tytul" TEXT NOT NULL,
	"link" TEXT NOT NULL,
	"nr_importu" integer NOT NULL,
	CONSTRAINT "ustawy_pk" PRIMARY KEY ("index")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "dane_osoba" (
	"id_osoby" serial NOT NULL,
	"imie" VARCHAR(30) NOT NULL,
	"nazwisko" VARCHAR(50) NOT NULL,
	"Has�o" VARCHAR(50) NOT NULL,
	"data_urodzenia" DATE NOT NULL,
	"e-mail" VARCHAR(70) NOT NULL,
	"nr_telefonu" integer NOT NULL,
	"plec" BOOLEAN NOT NULL,
	"PESEL" TEXT NOT NULL UNIQUE,
	CONSTRAINT "dane_osoba_pk" PRIMARY KEY ("id_osoby")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "glosy" (
	"id_glosu" serial NOT NULL,
	"ustawa" integer NOT NULL,
	"glosujacy" integer NOT NULL,
	"glos_tak" BOOLEAN NOT NULL,
	"glos_nie" BOOLEAN NOT NULL,
	"glos_wstrzymany" BOOLEAN NOT NULL,
	CONSTRAINT "glosy_pk" PRIMARY KEY ("id_glosu")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "importy" (
	"index" serial NOT NULL,
	"data_startu" DATE NOT NULL,
	"status" VARCHAR(16) NOT NULL,
	"data_zakonczenia" DATE NOT NULL,
	CONSTRAINT "importy_pk" PRIMARY KEY ("index")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "wyniki" (
	"id_wyniku" serial NOT NULL,
	"ustawa" integer NOT NULL UNIQUE,
	"wynik_tak" integer NOT NULL,
	"wynik_nie" integer NOT NULL,
	"wynik_wstrzymany" integer NOT NULL,
	CONSTRAINT "wyniki_pk" PRIMARY KEY ("id_wyniku")
) WITH (
  OIDS=FALSE
);



ALTER TABLE "ustawy" ADD CONSTRAINT "ustawy_fk0" FOREIGN KEY ("nr_importu") REFERENCES "importy"("index");


ALTER TABLE "glosy" ADD CONSTRAINT "glosy_fk0" FOREIGN KEY ("ustawa") REFERENCES "ustawy"("index");
ALTER TABLE "glosy" ADD CONSTRAINT "glosy_fk1" FOREIGN KEY ("glosujacy") REFERENCES "dane_osoba"("id_osoby");


ALTER TABLE "wyniki" ADD CONSTRAINT "wyniki_fk0" FOREIGN KEY ("ustawa") REFERENCES "ustawy"("index");
