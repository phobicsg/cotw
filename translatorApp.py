from helperfunctions import *
import requests
import json
import sys 
import random
from datetime import datetime
import csv
import time
import credentials
from constants import *


def getLanguages(country):
    response=requests.get("https://translator-api-qa.taethni.com/api/languages/country/NPL")
    print(response.json())



def getCountryCodeISO3166(name):
    countrycodes=readJSONFile(COUNTRYCODE3166)
    code=findObjInListByAttributes(countrycodes,"Name",name)
    if code is not None:
        return code["Code"]
    else:
        return "not found"


def getKeysForTargetLanguage(countryCode3, languageCode):
     url="https://translator-api-qa.taethni.com/api/Keys/%s/%s" % (countryCode3, languageCode)
     response= requests.get(url)
     listOfEntries=response.json() 
     return convertKeysForTargetLanguageIntoCSVHeaderFormat(listOfEntries, languageCode)

def convertKeysForTargetLanguageIntoCSVHeaderFormat(listOfEntries,languageCode):
    newlist=[]
    for places in listOfEntries:
        places["en"]= places.pop("enValue")
        places[languageCode] = places["translation"] if places["translation"] is not None else ""
        places.pop("language")
        places.pop("translation")
        newlist.append(places)
    return newlist

def isSupportedLanguageOnGoogle(langCode):
    langCode=langCode.lower() 
    response=requests.get("https://translator-api-qa.taethni.com/api/Languages/google-supported")
    languages = response.json()["languages"]
    Obj=findObjInListByAttributes(languages,"code",langCode)
    if Obj is None:
        return False
    else:
        return True


def isGoogleMapSupportedLang(langCode):
    langCode=langCode.lower()
    supported_languages=readCSVFile(GOOGLEMAP_SUPPORTED_LANG)
    obj=findObjInListByAttributes(supported_languages,"LanguageCode",langCode)
    if obj is None:
        return False
    else:
        return True