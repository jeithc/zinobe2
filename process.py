from connection import list_countries, country_region, sql_connection
from hashlib import sha1
import pandas as pd
import time

def run_process():
    try:
        list_regions = regions()
        countries_regions, language_countries= countries(list_regions)
        print(list_regions)
        print(countries_regions)
        print(language_countries)
        data, data_time = table_dataframe(list_regions,countries_regions,language_countries)
        create_sqlite(data)
        create_json(data)
        return 'ok'
    except Exception as e:
        error = 'Error al ejecutar comandos: {}'.format(e)
        print (error)
        return error
        
    

def regions():
    #sacamos todas las regiones del primer api
    all_regions = list_countries()
    #guardamos en una list
    regions=[region['region'] for region in all_regions]
    #eliminamos las duplicadas
    regions = list(dict.fromkeys(regions))
    #en el api viene una region vaciá. la sacamos de la lista
    regions = list(filter(None, regions))
    return regions


def countries(list_regions):
    countries_regions=[]
    language_countries=[]
    #buscamos un país por region y su idioma
    for region in list_regions:
        all_countries = country_region(region)
        countries_regions.append(all_countries[0]['name'])
        language_countries.append(encrypt(all_countries[0]['languages'][0]['name']))
    return countries_regions, language_countries


def encrypt(string):
    """encriptamos el idioma"""
    string= sha1(string.encode('utf-8')).hexdigest()
    return string


def table_dataframe(regions, countries, languages):
    for i in range(len(regions)):
        begin_time=time.time()        
        d = {
            'region': regions[i],
            'country': countries[i],
            'language': languages[i],
            'time':time.time() - begin_time
        } 
        if i == 0:
            data = pd.DataFrame(data=d, index=[i])
            print(data)
        else:
            data2 = pd.DataFrame(data=d,index=[i])
            data = pd.concat([data, data2])
    print(data)
    # sacamos la medicion de tiempo 
    data_time = {
        'min':data['time'].min(),
        'max':data['time'].max(),
        'mean':data['time'].mean(),
        'sum':data['time'].sum()
    }
    print(data_time['min'],data_time['max'],data_time['mean'],data_time['sum'])

    return data, data_time


def create_sqlite(data):
    con = sql_connection()
    data.to_sql('regions', con, if_exists='replace', index=False)
    con.close()


def create_json(data):
    data.to_json (r'data.json')
    

