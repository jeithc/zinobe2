import requests
import sqlite3
from sqlite3 import Error



def list_countries():
    """me conecto al api de regiones para traer los datos """
    url = "https://restcountries-v1.p.rapidapi.com/all"

    headers = {
        'x-rapidapi-host': "restcountries-v1.p.rapidapi.com",
        'x-rapidapi-key': "c330b5449dmshb77195a45bb8017p1d0f40jsn6f22cdb2611a"
    }
    response =requests.request("GET", url, headers=headers)
    region_data= response.json()
    return region_data


def country_region(region):
    """me conecto al api de países  para traer los datos de países por regiones"""
    url = "https://restcountries.eu/rest/v2/region/"
    response =requests.request("GET", url+region)
    region_data= response.json()
    return region_data


def sql_connection():
    try:
        con = sqlite3.connect('db_data.db')
        return con
    except Error:
        print(Error)



