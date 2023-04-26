#default libraries
from datetime import datetime
from picamera import PiCamera
from time import sleep
import os

#additional libraries
import pyrebase

#my files
from waveFileClass import waveFileClass
from firebaseApiConfig import firebaseConfig

#startup dialog
print("running...")

firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()

#make file
outputFileName = "WhaleSoundsTest.wav"
rawDataFileName = "WhaleData.dat"
waveFileClass(16000, rawDataFileName, outputFileName).createFile()

#upload file
# print("pushed")
# now = datetime.now()
# dt = now.strftime("%d%m%Y%H:%M:%S")
# name = dt+".jpg"
# camera.capture(name)
# print(name+" saved")
storage.child(outputFileName).put(outputFileName)
# print("Image sent")
# os.remove(name)
# print("File Removed")
# sleep(2)

print("done")