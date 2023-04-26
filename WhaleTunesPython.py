# File Name: WhaleTunesPython.py
# Author: Seamus Finlayson
# Date: 2023-04-25

#default libraries
from datetime import datetime
from time import sleep
import os

#additional libraries
import pyrebase

#my files
from waveFileClass import waveFileClass
from firebaseApiConfig import firebaseConfig

#startup dialog
print("Running...")

#firebase setup
firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()

#make wave file and give name with time and date
now = datetime.now()
dateTimeString = now.strftime("%Y-%m-%d at %H:%M:%S")

outputFileName = "Whale Recording from " + dateTimeString + ".wav"

outputpath = os.path.join("./Recordings", outputFileName)

#set input file
rawDataFileName = "WhaleData.dat"

waveFileClass(16000, rawDataFileName, outputpath).createFile()
print("Recording saved as: ", outputpath)

# upload file
storage.child(outputFileName).put(outputpath)
print("File uploaded.")

#remove file
# os.remove(name)
# print("File Removed")
# sleep(2)

print("Done.")