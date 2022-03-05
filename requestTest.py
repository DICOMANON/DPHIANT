
import requests
import json
import random
import uuid
import names
from pymongo import MongoClient

def anonymizePatientInfo(originalPHI):
    # aliasPatientName is randomly generated based on original PatientSex
    # aliaspatientID is a new UUID
    # aliasPatientBirthDate is binned down to its year

    aliasPatientName = ""
    aliasPatientID = str(uuid.uuid4())
    aliasPatientBirthDate = originalPHI["PatientBirthDate"][:4] + "0000"

    if(originalPHI["PatientSex"].strip() == "O"):
        aliasPatientName = names.get_full_name()
    elif(originalPHI["PatientSex"].strip() == "F"):
        aliasPatientName = names.get_full_name(gender="female")
    else:
        aliasPatientName = names.get_full_name(gender="male")

    originalPHI["aliasPatientName"] = aliasPatientName
    originalPHI["aliasPatientID"] = aliasPatientID
    originalPHI["aliasPatientBirthDate"] = aliasPatientBirthDate
    
    return originalPHI

def saveToDatabase(PHI, client:MongoClient, db, collection):
    collection.insert_one(PHI)

def checkIfPatientExists(originalPHI, client:MongoClient, db, collection):
    document = list(collection.find(originalPHI))
    # print(list(document))
    if(len(document) == 0):
        return False
    else:
        return True

def getPatientInfo(PHI, client:MongoClient, db, collection):
    document = list(collection.find(PHI))
    patientRow = document[0]

    aliasPHI = {
        "PatientName":patientRow["aliasPatientName"],
        "PatientID":patientRow["aliasPatientID"],
        "PatientBirthDate":patientRow["aliasPatientBirthDate"],
        "PatientSex":patientRow["PatientSex"]
    }

    return aliasPHI



client = MongoClient(
    host = 'mongodb://localhost:27017/', # <-- IP and port go here
    serverSelectionTimeoutMS = 3000, # 3 second timeout
    username="root",
    password="example",
)
db = client["PHICrossTable"]
collection = db["PatientHealthInformation"]

orthancApi = requests.Session()
# orthancApi.headers.update({"Authorization": self.authorizationToken})

'''
    "0010-0010" - PatientName
    "0010-0020" - PatientID
    "0010-0030" - PatientBirthDate
    "0010-0040" - PatientSex
'''

#List of Personal Health Information Tags to retrieve
getTags = ['0010-0010', '0010-0020', '0010-0030', '0010-0040']
tagNames = ["PatientName", "PatientID", "PatientBirthDate", "PatientSex"]
originalPHI = {}
instanceId = "b2f4e23c-9d5b3bfe-81474211-0e6af1a9-c976169e"
for tag, tagName in zip(getTags, tagNames):
    url = "http://localhost:8044/instances/" + instanceId + "/content/" + tag
    page = orthancApi.get(url, auth=('demo', 'demo'))
    originalPHI[tagName] = page.text

# print(originalPHI)

patientExists = checkIfPatientExists(originalPHI, client, db, collection)

if(patientExists):
    print(getPatientInfo(originalPHI, client, db, collection))
else:
    newPHI = anonymizePatientInfo(originalPHI)
    saveToDatabase(newPHI, client, db, collection)
