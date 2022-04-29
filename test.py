import os

dicomDirectory = os.path.dirname(os.path.realpath(__file__)) + "\dicomFiles"

for filename in os.listdir(dicomDirectory):
    print(dicomDirectory + "\\" + filename)

print(os.path.dirname(os.path.realpath(__file__)) + "/dicomFiles/source.dcm", "rb")