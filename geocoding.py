from helperfunctions import *
from credentials import API_KEY
import requests
import json
import sys 
import random
from datetime import datetime
import csv
import time
import credentials



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

def populatingTranslation(listOfEntries,country,baseLangCode,translatedLangCode, countryCode):
    translatedList=[]
    for place in listOfEntries:
        english_name = place[baseLangCode]
        translatedName, latlng =getReverseGeocoding(english_name,country,countryCode,translatedLangCode)
        place[translatedLangCode]=translatedName
        place["laglng"]=latlng
        translatedList.append(place)
    return translatedList


def extractingListByRange(listOfEntries, start,end):
    extractedList=[]
    for i in range(start,end):
        extractedList.append(listOfEntries[i])
    return extractedList




extractedDataForTranslation=extractingListByRange(readCSVFile("Input/NPL-ne-translations.csv"),0,5000)
translatedList= populatingTranslation(extractedDataForTranslation,"Nepal","en","ne","NP")
writeCSVFile("Output.csv",translatedList)
