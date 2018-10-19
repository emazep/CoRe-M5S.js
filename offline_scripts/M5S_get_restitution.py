#!/usr/bin/env python3

__author__ = "Emanuele Zeppieri"
__copyright__ = """

    Copyright 2017-2018 Emanuele Zeppieri

    Licensed under the MIT License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       https://opensource.org/licenses/MIT

    This software is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""
__license__ = "MIT"
__status__ = "Beta"
__version__ = "0.0.1"

import argparse
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qsl
from string import Template
import json
import sys
import logging

#logging.basicConfig(level=logging.DEBUG)

HTML_PARSER = 'lxml'
UA = UserAgent()

PEOPLEDIR_URL    = 'http://www.tirendiconto.it/trasparenza/'
PERSON_URL_TEMPL = PEOPLEDIR_URL + 'rendicontazione.php?mese=${mese}&user=${user}&tipo=${tipo}'
person_url_templ = Template(PERSON_URL_TEMPL)

PAGE_NA_TEXT = 'Rendicontazione del mese selezionato in elaborazione'
RECEIPT_TEXT = 'upload/bonifici'

STIPENDIO_FORFAIT            = 5000
RIMBORSO_FORFAIT             = 7000
TOTALE_PERCEPITO_FORFAIT     = STIPENDIO_FORFAIT + RIMBORSO_FORFAIT
STIPENDIO_RESTITUITO_FORFAIT = 2000
RIMBORSO_RESTITUITO_FORFAIT  = 3000
TOTALE_RESTITUITO_FORFAIT    = STIPENDIO_RESTITUITO_FORFAIT + RIMBORSO_RESTITUITO_FORFAIT 

MONTHS = range(3, 66)

def td2float(text):
    return float( text.rstrip(' €').replace('.','').replace(',','.') )

parser = argparse.ArgumentParser(description='Scarica gli importi percepiti e restituiti dai parlamentari del M5S dal sito "Ti Rendi Conto?!?!?!?", e li stampa serializzati in JSON')
group = parser.add_mutually_exclusive_group()
group.add_argument(
    '--users', metavar='User', type=int, nargs='+',
    help = 'Lista degli id (numerici interi) dei parlamentari del M5S di cui scaricare i dati. Per ottenere gli id, lanciare questo script senza alcun parametro.'
)
group.add_argument( '--all', action='store_true', help = 'Scarica i dati di tutti i parlamentari del M5S.' )
args = parser.parse_args()

people_dir_page = requests.get( PEOPLEDIR_URL, headers = {'User-Agent': UA.random} )
people_dir_soup = BeautifulSoup(people_dir_page.text, HTML_PARSER)
people_table = people_dir_soup.findAll('table')[0]

persons = {}

for row in people_table.findAll('tr'):
    for table_cell in row.findAll('td'):
        person = {}
        table_cell_a_tag = table_cell.a
        person['fullname'] = table_cell_a_tag['title']
        person_href = table_cell_a_tag['href'].split("'")[1]
        person['data'] = dict( parse_qsl( urlparse(person_href).query ) )
        persons[ person['data']['user'] ] = person

if not (args.users or args.all):
    for user in sorted(persons, key=int):
        print( user, '\t', persons[user]['fullname'] )
    sys.exit(0)
    
user_results = {}

requested_users = persons.keys() if args.all else map(str, args.users) & persons.keys()

for user in sorted( requested_users, key=int ):
        
    person_data = persons[user]['data']
    person_url_partial_templ = Template( person_url_templ.safe_substitute( user=person_data['user'], tipo=person_data['tipo'] ) )
    
    user_results[user] = {}
    
    for month in MONTHS:
        person_url = person_url_partial_templ.substitute(mese = 4 if month==3 else month)
        
        person_page = requests.get( person_url, {'User-Agent': UA.random} )
        
        person_page_text = person_page.text
        
        if PAGE_NA_TEXT in person_page_text:
            # The previous month was the last one available, so stop looping over months.
            break
        
        person_soup = BeautifulSoup(person_page_text, HTML_PARSER)
        
        stipendio_forfait = STIPENDIO_FORFAIT
        rimborso_forfait  = RIMBORSO_FORFAIT
        totale_restituito_forfait = TOTALE_RESTITUITO_FORFAIT
        stipendio_restituito_forfait = STIPENDIO_RESTITUITO_FORFAIT
        rimborso_restituito_forfait = RIMBORSO_RESTITUITO_FORFAIT
        
        if month == 3:
            stipendio_forfait /= 2
            rimborso_forfait  /= 2
            totale_restituito_forfait /= 2
            stipendio_restituito_forfait /= 2
            rimborso_restituito_forfait /= 2

        try:
            table_totale, table_stipendio, table_rimborso = person_soup.findAll('table')[1:4]

            if month in (3, 4, 5):
                # Different data on the site, special case.
                totale_restituito = td2float( table_stipendio.findAll('tr')[5].findAll('td')[1].text )
                                
                if month == 3:
                    totale_restituito /= 3
                elif month == 4:
                    totale_restituito *= 2/3
                
                user_results[user][month] = {
                    'totale_restituito'   : totale_restituito,
                    'stipendio'           : stipendio_forfait,
                    'stipendio_restituito': totale_restituito * STIPENDIO_FORFAIT / TOTALE_PERCEPITO_FORFAIT,
                    'rimborso'            : rimborso_forfait,
                    'rimborso_restituito' : totale_restituito * RIMBORSO_FORFAIT / TOTALE_PERCEPITO_FORFAIT
                }
            else :
                td_ricevuta, td_importo_tot_restituito = table_totale.find('tr').findAll('td')
                
                '''
                if RECEIPT_TEXT not in td_ricevuta.a['href']:
                    # No receipt here: skip this month
                    continue
                '''
                
                totale_restituito = td2float(td_importo_tot_restituito.text)
                
                trs_stipendio = table_stipendio.findAll('tr')
                stipendio = td2float( trs_stipendio[1].findAll('td')[1].text )
                stipendio_restituito = td2float( trs_stipendio[4].findAll('td')[1].text )
                
                trs_rimborso = table_rimborso.findAll('tr')
                rimborso = td2float( trs_rimborso[1].findAll('td')[1].text )
                try:
                    tr_rimborso = trs_rimborso[6]
                except IndexError:
                    tr_rimborso = trs_rimborso[4]
                rimborso_restituito = td2float( tr_rimborso.findAll('td')[1].text )
                
                user_results[user][month] = {
                    'totale_restituito'   : totale_restituito,
                    'stipendio'           : stipendio,
                    'stipendio_restituito': stipendio_restituito,
                    'rimborso'            : rimborso,
                    'rimborso_restituito' : rimborso_restituito
                }
            
            user_results[user][month]['presuntivo'] = False
        except:
            # log error
            print('User:' , '\t', user , file=sys.stderr)
            print('Month:', '\t', month, file=sys.stderr)
            
            # Save anyway default values and go on
            user_results[user][month] = {
                'totale_restituito'   : totale_restituito_forfait,
                'stipendio'           : stipendio_forfait,
                'stipendio_restituito': stipendio_restituito_forfait,
                'rimborso'            : rimborso_forfait,
                'rimborso_restituito' : rimborso_restituito_forfait,
                'presuntivo'          : True
            }
        
print( json.dumps(user_results, indent=4) )

'''
Current users list
1 108 7 11 12 14 116 17 19 121 23 124 29 126 45 47 48 129 130 54 55 56 57 133 62 63 135 66 67 138 72 143 145 84 87 88 91 92 156 97 98 104 105
'''
        