from helperfunctions import *
from credentials import API_KEY
import requests
import json
import sys 
import random
from datetime import datetime
import csv
import time
from translatorApp import *



def getGeocoding(lat,long,lang):
    url = "https://maps.googleapis.com/maps/api/geocode/json?latlng=%f,%f&language=%s&key=%s" % (lat, long,lang, API_KEY)
    print(url)
    response = requests.get(url)
    print(response)
    print(response.json())
    
def getReverseGeocoding(area,country,countryCode, lang):
    area = area +","+country
    url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&language=%s&key=%s" % (area,lang, API_KEY)
    print(url)
    try:

        response = requests.get(url)
        result=response.json()
        print(result)
        if result["status"] == "ZERO_RESULTS":
            print("No Results Found for %s. Consider Search by GPS Coordinates" % area)
            return "",""
        else:
            placeDetails = result["results"]       
            geoInfoObj = placeDetails[0]
            addressComponentList=geoInfoObj["address_components"]
            placeTypesList= geoInfoObj["types"]
            if "political" in placeTypesList or "locality" in placeTypesList or "sublocality" in placeTypesList:
                countryType=["country","political"]
                country=findObjInListByAttributes(addressComponentList,"types",countryType)
                if country is not None:
                    countryShortName = country["short_name"]
                    if countryCode == countryShortName:
                        for addresses in addressComponentList:
                            addressType=addresses["types"]
                            if addressType==placeTypesList:
                                translatedName=addresses["long_name"]
                                print("Translated Name for %s is : %s" % (area, translatedName))
                                latLng=geoInfoObj["geometry"]["location"]
                                latLngList = [latLng["lat"], latLng["lng"]]
                                print(latLngList)
                                return translatedName ,latLngList
                    else:
                        print("Result return is not in the right country. Verify location by GPS")
                        return "",""
                else:
                    print("Country not found. Likely disputed territory")
                    return "",""
            else:
                print("no suitable match is found. Verify Location by GPS")
                return "",""        

    except:
        e = sys.exc_info()
        print(e)
        return "",""
    


def populatingTranslation(listOfEntries,country,baseLangCode,translatedLangCode, countryCode):
    translatedList=[]
    for place in listOfEntries:
        english_name = place[baseLangCode]
        translatedName, latlng =getReverseGeocoding(english_name,country,countryCode,translatedLangCode)
        place[translatedLangCode]=translatedName
        place["latlng"]=latlng
        translatedList.append(place)
    return translatedList


def extractingListByRange(listOfEntries, start,end):
    extractedList=[]
    for i in range(start,end):
        extractedList.append(listOfEntries[i])
    return extractedList

def gettingTranslationByCountryAndLanguage(countrycode3, country, languageCode, outputFileName):
    if isSupportedLanguageOnGoogle(languageCode):
        listOfPlaces=getKeysForTargetLanguage(countrycode3,languageCode)
        if len(listOfPlaces) < 2000: 
            translatedList=populatingTranslation(listOfPlaces,country,"en",languageCode,getCountryCodeISO3166(country))
            writeCSVFile(outputFileName,translatedList)
        else:
            print("There are a total of %d entries found. Consider slicing up the records and run your query for optimum time" % len(listOfPlaces))
    else:
        print("Requested Translated Language %s is not supported on Google Platform" % languageCode)


def getListOfGoogleCompatibleTranslations():
    listOfPlaces=readJSONFile(PLACES_TO_TRANSLATE)
    newlist=[]
    for place in listOfPlaces:
        supportedlang=[]
        languages = place["languages"]
        for lang in languages:
           if isGoogleMapSupportedLang(lang):
               supportedlang.append(lang)
        if len(supportedlang)!=0:
            place["languages"] = supportedlang
            newlist.append(place)
    return newlist


