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
    print(response.content)
    
def getReverseGeocoding(area,countryCode, lang):
    url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&language=%s&key=%s" % (area,lang, API_KEY)
    print(url)
    response = requests.get(url)
    result=response.json()
    print(result)
    if result["status"] == "ZERO_RESULTS":
        return "No Results Found for %s. Consider Search by GPS Coordinates" % area
    else:
        placeDetails = result["results"]
        if len(placeDetails)==1:
            geoInfoObj = placeDetails[0]
            addressComponentList=geoInfoObj["address_components"]
            placeTypesList= geoInfoObj["types"]
            if "political" or "locality" or "sublocality" in placeTypesList:
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
                                return translatedName
                    else:
                        return "Result return is not in the right country. Verify location by GPS"
            else:
                return "no suitable match is found. Verify Location by GPS"
   
#listofentries = readCSVFile("Input/NPL-ne-translations.csv")
#print(len(listofentries))

print(getReverseGeocoding("Gairigaun","NP", "ne"))