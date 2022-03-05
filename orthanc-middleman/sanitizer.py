from multiprocessing import Pool, Queue, Process
import json
import threading
import requests
import uuid
import names
import random
import datetime
from pymongo import MongoClient


class Sanitizer:

    def __init__(self, workerCount, authorizationToken):
        self.workerCount = workerCount
        self.workers = []
        self.workersShouldStop = False
        self.instancesToProcess = Queue()
        self.authorizationToken = authorizationToken

    def start(self):
        print("Starting {w} python workers for Sanitizer".format(
            w=self.workerCount))

        for i in range(0, self.workerCount):
            self.workers.append(
                Process(target=worker, group=None, args=(str(i), self, )))
            self.workers[i].start()

    def stop(self):
        print("Stopping {w} python workers for Sanitizer".format(
            w=self.workerCount))
        workersShouldStop = True

        # push one dummy message for each worker to wake them up
        for i in range(0, self.workerCount):
            self.instancesToProcess.put(None)

        for i in range(0, self.workerCount):
            self.workers[i].join()

    def push(self, instanceId: str):
        print("pushing instance " + instanceId)
        self.instancesToProcess.put(instanceId)

    def retryInstanceLater(self, instanceId: str, delay: float):
        t = threading.Timer(delay, function=self.push, args=(instanceId, ))
        t.start()

    def modifyInstance(self, instanceId: str):
        print("processing instance " + instanceId)

        # Initialize MongoDB client
        client = MongoClient(
            host = 'mongodb://mongo:27017', # <-- IP and port go here
            serverSelectionTimeoutMS = 3000, # 3 second timeout
            username="root",
            password="example",
        )
        db = client["PHICrossTable"]
        collection = db["PatientHealthInformation"]

        # we are not in the Orthanc main process so we can't use the orthanc python module,
        # we have to use requests to access Orthanc from the external API
        orthancApi = requests.Session()
        orthancApi.headers.update({"Authorization": self.authorizationToken})
        
        #List of Personal Health Information Tags to retrieve
        getTags = ['0010-0010', '0010-0020', '0010-0030', '0010-0040']
        tagNames = ["PatientName", "PatientID", "PatientBirthDate", "PatientSex"]
        originalPHI = {}
        for tag, tagName in zip(getTags, tagNames):
            url = "http://localhost:8042/instances/" + instanceId + "/content/" + tag
            page = orthancApi.get(url, auth=('demo', 'demo'))
            originalPHI[tagName] = page.text

        print("Original PHI:", originalPHI)
        

        patientExists = self.checkIfPatientExists(originalPHI, client, db, collection)
        print("PatientExists: ", patientExists)

        newPHI = []
        modifyBody = {}

        if(patientExists):
            newPHI = self.getPatientInfo(originalPHI, client, db, collection)
            modifyBody = {
                "Replace": {
                    "InstitutionName": "DPHIANT",
                    "PatientName": newPHI["PatientName"],
                    "PatientID": newPHI["PatientID"],
                    "PatientBirthDate": newPHI["PatientBirthDate"],
                    "PatientSex": newPHI["PatientSex"]
                },
                "Keep": ["SOPInstanceUID"],
                "Force": True  # because we want to replace/keep the SOPInstanceUID
            }
        else:
            newPHI = self.anonymizePatientInfo(originalPHI)
            self.saveToDatabase(newPHI, client, db, collection)
            modifyBody = {
                "Replace": {
                    "InstitutionName": "DPHIANT",
                    "PatientName": newPHI["aliasPatientName"],
                    "PatientID": newPHI["aliasPatientID"],
                    "PatientBirthDate": newPHI["aliasPatientBirthDate"],
                    "PatientSex": newPHI["PatientSex"]
                },
                "Keep": ["SOPInstanceUID"],
                "Force": True  # because we want to replace/keep the SOPInstanceUID
            }


        try:
            # print(json.dumps(modifyBody))
            modifyRequest = orthancApi.post(url="http://localhost:8042/instances/" + instanceId + "/modify",
                                            data=json.dumps(modifyBody))

            if modifyRequest.status_code != 200:
                print("Could not modify instance: " +
                      instanceId + ", it won't be retried !")
                return

            modifiedDicom = modifyRequest.content

            sendToPacsRequest = orthancApi.post(
                url="http://localhost:8042/modalities/pacs/store-straight", data=modifiedDicom)

            if sendToPacsRequest.status_code == 200:
                print("instance sent to PACS, deleting from middleman")
                deleteRequest = orthancApi.delete(
                    url="http://localhost:8042/instances/" + instanceId)

                if deleteRequest.status_code == 200:
                    return
            else:
                print("instance failed to send to PACS, will retry later")

            self.retryInstanceLater(instanceId, 10.0)

        except Exception as e:
            print("could not process instance: {i}: {e}, will retry later".format(
                i=instanceId, e=e))
            self.retryInstanceLater(instanceId, 10.0)

    def generateRandomPatientInfo(self):
        name = ""
        genderList = ["M", "F", "O"]
        randomGender = random.choices(genderList)[0]
        
        if(randomGender == "O"):
            name = names.get_full_name()
        elif(randomGender == "F"):
            name = names.get_full_name(gender="female")
        else:
            name = names.get_full_name(gender="male")

        yearRange = random.randint(1970, 2000)
        monthRange = random.randint(1,12)
        dayRange = random.randint(1,31)
        dicomDate = None

        while(dicomDate == None):
            try:
                dicomDate = datetime.datetime(yearRange, monthRange, dayRange).strftime("%Y%m%d")
            except:
                dayRange = random.randint(1,31)
        
        return [name, dicomDate, randomGender]

    def anonymizePatientInfo(self, originalPHI):
        # aliasPatientName is randomly generated based on original PatientSex
        # aliaspatientID is a new UUID
        # aliasPatientBirthDate is binned down to its year

        aliasPatientName = ""
        aliasPatientID = str(uuid.uuid4())
        aliasPatientBirthDate = originalPHI["PatientBirthDate"][:4] + "0101"

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

    def saveToDatabase(self, PHI, client:MongoClient, db, collection):
        collection.insert_one(PHI)

    def checkIfPatientExists(self, originalPHI, client:MongoClient, db, collection):
        document = list(collection.find(originalPHI))
        print("Checking if patient exists")
        print(originalPHI)
        print(list(document))
        if(len(document) == 0):
            return False
        else:
            return True

    def getPatientInfo(self, PHI, client:MongoClient, db, collection):
        document = list(collection.find(PHI))
        patientRow = document[0]

        aliasPHI = {
            "PatientName":patientRow["aliasPatientName"],
            "PatientID":patientRow["aliasPatientID"],
            "PatientBirthDate":patientRow["aliasPatientBirthDate"],
            "PatientSex":patientRow["PatientSex"]
        }

        return aliasPHI



def worker(workerName: str, sanitizer: Sanitizer):
    print("Starting python worker " + workerName)

    while not sanitizer.workersShouldStop:
        instanceId = sanitizer.instancesToProcess.get()

        if sanitizer.workersShouldStop:
            break

        sanitizer.modifyInstance(instanceId)

    print("Exiting python worker " + workerName)
