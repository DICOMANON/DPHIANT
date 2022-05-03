import os
import requests
import time
import pprint

'''
    This program is meant to process a folder of DICOM files
    with the use of the DPHIANT pipeline and anonymize them all.
    
    AUTOMATED PIPELINE PROCESS:
    - Automatically builds pipeline using docker compose
    - Automatically uploads DICOM files from a folder to be anonymized into dphiant-modality Orthanc instance
    - Automatically pushes uploaded files from dphiant-modality to dphiant-middleman Orthanc instance
    - Anonymized files are viewable in dphiant-pacs Orthanc instance
    - Cross reference table viewable via Mongo Express web interface

    DPHIANT Modality: (http://localhost:8044)

    DPHIANT Middleman: (http://localhost:8043)
    - Nothing to view here

    DPHIANT PACS: (http://localhost:8042)

    Mongo Express: (http://localhost:8081/db/PHICrossTable/PatientHealthInformation)

'''

# Source directory for DICOM files that need to be anonymized. (Relative to project root)
dicomDirectory = os.path.dirname(os.path.realpath(__file__)) + "\dicomFiles"

os.system("docker-compose up --build -d")

start = time.time()

for filename in os.listdir(dicomDirectory):
    print("uploading file to modality:", dicomDirectory + "\\" + filename)
    modality = requests.Session()
    modality.auth = ("demo", "demo")
    with open(dicomDirectory + "\\" + filename, "rb") as f:
        instanceId = modality.post("http://localhost:8044/instances", f.read()).json()["ID"]
    print("InstanceID: " + str(instanceId))

    print("sending from modality to middleman")

    pacs = requests.Session()
    pacs.auth = ("demo", "demo")
    instanceTagsOnPacsRequest = pacs.get("http://localhost:8042/instances/" + instanceId + "/tags?simplify", timeout=1)

    modality.post("http://localhost:8044/modalities/middleman/store", instanceId)

end = time.time()

print("Pipeline process time :", end-start)

