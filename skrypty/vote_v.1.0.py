from bs4 import BeautifulSoup

import requests
import csv
import time


#zapis do csv, sciezka do pliku
csv_file = open('/tmp/zapis2.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['klucz','rok','nr_ustawy', 'tytul', 'link'])
#rok od ktorego zaczyna skanowanie
x = 2013
#rok konca skanowania
while x<=2021 :
  
  source = requests.get('https://isap.sejm.gov.pl/isap.nsf/ByYear.xsp?type=WDU&year='+str(x)).text
  soup = BeautifulSoup(source, 'lxml')

  for links in soup.find_all('a', class_='doc-details-link'):
      indeks_do_bazy = links.text
      indeks_do_bazy = indeks_do_bazy.split(' ')[3]
      adres = links['href'].split('?')[1]
      pelen_adres = f'https://isap.sejm.gov.pl/isap.nsf/DocDetails.xsp?{adres}'
      kopia_do_pdf = adres.split('=')[1]
      #Connect and sleep for 1 second
      try:
        new_source = requests.get(pelen_adres).text
        time.sleep(1)
      except requests.exceptions.ConnectionError:
        print("Connection refused")

      soup_link = BeautifulSoup(new_source, 'lxml')
      tytul = soup_link.find('h2').text

      for pdf in soup_link.find_all('div', class_='row') : 
          for ten in pdf.find_all(class_='icon-after doc-link'):
          
              test = ten['href'].split('/')[4]
              if test == 'O':
                  test = ten['href'].split('/')[5] 
                  link_do_pdf = f'https://isap.sejm.gov.pl/isap.nsf/download.xsp/{kopia_do_pdf}/O/{test}'
                  klucz = (x - 2000) * 10000 + int(indeks_do_bazy)
                  csv_writer.writerow([klucz, x, indeks_do_bazy, tytul, link_do_pdf])
  #skanowanie kolejnego roku     
  x+=1    
csv_file.close()
