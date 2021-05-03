import psycopg2
import csv
import time
import datetime

id_importu = int(time.strftime("%d%H%M%S"))
teraz = time.strftime("%Y-%m-%d %H:%M:%S")

conn = psycopg2.connect("host=192.168.33.10 dbname=projekt user=postgres")

cur = conn.cursor()

cur.execute("INSERT INTO importy VALUES (%s, %s, %s, %s);", [id_importu, teraz, "inprogress",'1900-01-01 01:01:01'])
conn.commit()

with open('/tmp/zapis2.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader) # Skip the header row.
    for row in reader:
        print(row)
        klucz = row[0]
        rok = row[1]
        nr_ustawy = row[2]
        tytul = row[3]
        link = row[4]
        cur.execute("""INSERT INTO ustawy
                        (index, rok, nr_ustawy, tytul, link, nr_importu)
                    SELECT %s, %s, %s, %s, %s, %s
                    WHERE
                        NOT EXISTS (
                            SELECT index FROM ustawy WHERE index = %s
                        );""", [klucz, rok, nr_ustawy, tytul, link, id_importu, klucz])

        cur.execute("""INSERT INTO wyniki
                        (id_wyniku, ustawa, wynik_tak, wynik_nie, wynik_wstrzymany)
                    SELECT %s, %s, %s, %s, %s
                    WHERE
                        NOT EXISTS (
                            SELECT id_wyniku FROM wyniki WHERE id_wyniku = %s
                        );""", [klucz, klucz, '0', '0', '0', klucz])
        
    cur.execute("UPDATE importy SET status = %s, data_zakonczenia = %s WHERE index = %s;", ["OK",time.strftime("%Y-%m-%d %H:%M:%S"),id_importu])
conn.commit()