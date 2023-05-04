# File Name: WhaleTunesPython.py
# Author: Seamus Finlayson
# Created: 2023-04-25

#default libraries
from datetime import datetime
import time
import os
import sys

#additional libraries
import pyrebase
import serial

#my files
from waveFileClass import waveFileClass
from firebaseApiConfig import firebaseConfig

#startup dialog
print("Running...")

#setup serial
ser = serial.Serial("/dev/ttyS0", 115200)
print("Using serial: ", ser.name)

#firebase setup
firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()

#state machine setup
WAITING_STATE = 0
COLLECTING_DATA_STATE = 1
UPLOADING_DATA_STATE = 2
state = WAITING_STATE

#uart code symbols
ESCAPE_CHAR = "ffff"
SOF_CHAR = "ffee"
EOF_CHAR = "fffe" #end of file character

fileName = "error getting name"

while True:
    
    #detect exit key -- not implemented
    if False:
        pass
    else:
        
        #select state
        if state == WAITING_STATE:
            
            #indicate state change
            print("\nWaiting for hydrophone...")
            
            
            #check for escape character
            byte_array = ser.read(2)
            if byte_array.hex() == ESCAPE_CHAR:
                
                #check for start of file character
                byte_array = ser.read(2)
                if byte_array.hex() == SOF_CHAR:
                    
                    #go to next state
                    print("Start character received.")
                    state = COLLECTING_DATA_STATE
                    
                else:
                    print("ERROR unexpected uart code word: ", byte_array.hex())
                    print("Expected ", SOF_CHAR)
                    sys.exit(1)
            else:
                print("ERROR unexpected uart code word: ", byte_array.hex())
                print("Expected ", ESCAPE_CHAR)
                sys.exit(1)
            
        elif state == COLLECTING_DATA_STATE:
            
            #indicate state change
            print("\nCollecting data from hydrophone...")
            
            #get date and time for file name
            now = datetime.now()
            dateTimeString = now.strftime("%Y-%m-%d at %H:%M:%S")
            
            #set file name
            fileName = "Recording from " + dateTimeString
            print("File name is: ", fileName)
            
            audioDataFileName = fileName + ".dat"
            audioDataPath = os.path.join("./Hydrophone_Data", audioDataFileName)
            
            #write samples to audio file until escape character
            with open(audioDataPath, 'wb') as f:
                
                #get samples in loop
                quit = False
                while not quit:
                    
                    #get data
                    byte_array = ser.read(2)
                    #binary_data = bytes([data[0], data[1]) #data is already bytes data type
                    
                    #check for escape character
                    if byte_array.hex() == ESCAPE_CHAR:
                        byte_array = ser.read(2)
                        
                        if byte_array.hex() == ESCAPE_CHAR:
                            #escape char value was sent, write it to file
                            intData = int.from_bytes(byte_array, "big", signed="True")
                            bytesData = bytearray(intData.to_bytes(2, "little", signed=True))
                            f.write(bytesData)
                            
                        elif byte_array.hex() == EOF_CHAR:
                            #end of file was sent, go to next state
                            quit = True
                            print("End of data character received.")
                            
                        else:
                            print("ERROR bad data received")
                            sys.exit(1)
                            
                    else:
                        #write data to file
                        #print(time.time(), " data is: ", data) #debug only
                        intData = int.from_bytes(byte_array, "big", signed="True")
                        bytesData = bytearray(intData.to_bytes(2, "little", signed=True))
                        f.write(bytesData)
            
            #next state
            state = UPLOADING_DATA_STATE  
        
        elif state == UPLOADING_DATA_STATE:
            
            #indicate state change
            print("\nUploading data to firebase...")
            
            #
            #audioDataFileName = "WhaleData.dat" #testing only
            waveFileName = fileName + ".wav"
            waveFilePath = os.path.join("./Recordings", waveFileName)

            waveFileClass(16000, audioDataPath, waveFilePath).createFile()
            print("Recording saved as: ", waveFilePath)

            # upload file
            storage.child(waveFileName).put(waveFilePath) #disable while debugging other components
            print("File uploaded.")

            #remove file
            # os.remove(name)
            # print("File Removed")
            
            state = WAITING_STATE