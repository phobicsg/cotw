import requests
import json
import sys 
import random
from datetime import datetime
import csv
import time
import logging


def writeToJSONFile(writeObj, filename,operationMode="w"):
    logging.info("Starting write data to : %s", filename)  
    print("Starting write data to : %s" % filename)
    with open (filename,operationMode) as file:
        file.write(json.dumps(writeObj,indent=2))
        file.close()
    logging.info("Completed writing data to : %s" ,filename)
    print("Completed writing data to : %s" % filename)


def filterListByAttributes(objList,attributes,value,isValue):
    filteredList=[]
    filteredList= list(filter(lambda obj : ((obj[attributes]==value) is isValue), objList))     
    return filteredList



def findObjInListByAttributes(objList, attributes, value):
    object= None
    for obj in objList:
       if attributes in obj.keys():
           if obj[attributes] == value:
               object = obj
               break
    return object

def readCSVFile(filename):
    with open(filename,newline="") as csvFile:
        reader = csv.DictReader(csvFile)
        listOfEntries = list(row for row in reader)
        return listOfEntries


def writeCSVFile(filename,writeObj):
    with open(filename,"w",encoding="utf-8") as csvFile:
        header=writeObj[0].keys()
        writer = csv.DictWriter(csvFile,header)
        writer.writeheader()
        writer.writerows(writeObj)

       
        

def configureLoggingBasic():
  logging.basicConfig(filename="LOGFILE", encoding="utf-8",level=logging.DEBUG, format="%(asctime)s -%(levelname)s- %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p")

configureLoggingBasic()
