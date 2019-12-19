#
# ----------------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <jairomer@protonmail.com> wrote this file.  As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return.   Jaime Romero Marín
# ----------------------------------------------------------------------------------
#!../bin/pypy3

import xlrd as x
from sys import argv
import requests
from bs4 import BeautifulSoup
import json
import time
import threading

"""
    Generator.
    Read excel file and generate an URL string on
    each call.

"""
def get_next_url_from_excel( excel_file_path ):
    wb = x.open_workbook( excel_file_path )
    sheet = wb.sheet_by_index(0)
    rows = sheet.nrows
    # <ID> <link> <title> <score> <genre> <poster>
    for i in range(1,rows):
        url = sheet.cell_value(i, 1)
        yield url


"""
    Receives a string containing an URL.
    Return a JSON formatted movie representation.

"""
def parse_page_to_json( url ):
    data = {}
    try:
        page = requests.get( url )
        # Initialize the page using beautiful soup.
        soup = BeautifulSoup( page.content, 'html.parser')
        film_json = soup.find ('script', type='application/ld+json')
        data = json.loads( film_json.text )
        #print (data)
    except Exception as ex:
        print(ex)
        return

    #print( data['name'] )
    #print( data['director'] )
    #print( data['datePublished'] )
    #print( data['genre'] )
    #print( data['keywords'] )
    #print( data['description'] )
    #print( data['actor'])

    json_film = {}
    title       = data['name']
    if 'director' in data:
        if type( data['director'] ) is list :
            directors   = [ i['name'] for i in data['director'] ]
        else:
            directors   = data['director']['name']

    if 'datePublished' in data:
        date        = data['datePublished']

    if 'genre' in data:
        genre       = data['genre']

    if 'keywords' in data:
        keywords    = data['keywords']
        json_film['keywords']    = keywords

    if 'description' in data:
        description = data['description']

    if 'actor' in data:
        if type( data['actor'] ) is list:
            actors  = [ i['name'] for i in data['actor'] ]
        else:
            actors  = data['actor']['name']

    json_film['title']       = title
    if 'director' in data:
        json_film['directors']   = directors

    if 'datePublished' in data:
        json_film['release']     = date
        json_film['day']         = date.split('-')[2]
        json_film['month']       = date.split('-')[1]
        json_film['year']        = date.split('-')[0]

    if 'genre' in data:
        json_film['genres']      = genre

    if 'description' in data:
        json_film['description'] = description

    if 'actor' in data:
        json_film['actors']      = actors

    return json.dumps(json_film)
    #return json_film
'''
    Insert into ElasticSearch a new
    film encoded as a json.
'''
def put_film_into_ES( film_json ):
    print (film_json)
#    film_json["Content-Type"] = "application/json"
    r = requests.post( 'http://localhost:9200/film_db/film/', data = film_json, headers={"content-type":"application/json" }, timeout=120)
    print()
    print(r.json())
    print()
    #assert ( r['_shards']['successful'] == 1 )

def download_thread( url ):
    jsn = parse_page_to_json( url )
    print(jsn)
    put_film_into_ES(jsn)


def main ():
    script, excel_file = argv
    # while we have URLs to parse:
    #   1. Get the next URL.
    #   2. Feed the URL to the parser.
    #   3. Get the parsed JSON and push it into ES.

    recovery = open("processed_urls", "rb")
    processed_urls = recovery.readlines()
    recovery.close()

    recovery = open("processed_urls", "ab")
    processed_urls = [ x.strip() for x in processed_urls ]
    #print(processed_urls)

    worker_list = []
    for url in get_next_url_from_excel(excel_file) :
        print(url)
        if bytearray(url.strip(), 'utf-8') in processed_urls:
            print("processed!")
            continue
        else:
            copy = url + "\n"
            recovery.write(bytearray(copy, 'utf-8'))
        time.sleep(0.1)
        thread = threading.Thread(target=download_thread, args=(url,))
        thread.start()
        worker_list.append( thread )

    for worker in worker_list:
        worker.join()

    # Tests
    # j = parse_page_to_json( "https://www.imdb.com/title/tt0133093/?ref_=fn_al_tt_1" )
    # j = parse_page_to_json( "https://www.imdb.com/title/tt0113243/?ref_=fn_al_tt_1" )
    # j = parse_page_to_json( "https://www.imdb.com/title/tt0137523/?ref_=fn_al_tt_1" )
    # put_film_into_ES(j)

main()
