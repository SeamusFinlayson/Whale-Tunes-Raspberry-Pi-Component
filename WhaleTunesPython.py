from datetime import datetime
from picamera import PiCamera
from time import sleep
import os

import pyrebase

#startup dialog
print("running...")

#firebase setup
firebaseConfig = {
    #add information here, do not push to github, it is sensitive
}
firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()

#make file
myfile = open("myfile","w")
myfile.close

#upload file
# print("pushed")
# now = datetime.now()
# dt = now.strftime("%d%m%Y%H:%M:%S")
# name = dt+".jpg"
# camera.capture(name)
# print(name+" saved")
name = "pyTest.wav"
storage.child(name).put("66038001.wav")
# print("Image sent")
# os.remove(name)
# print("File Removed")
# sleep(2)

print("done")