#from flask import Flask, request
import Adafruit_DHT
import serial
import time 
import string
import pynmea2  
import requests
import datetime
sensor = Adafruit_DHT.DHT11
pin = 24
file =  open('filea.txt','w+')
while True:
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    # Gps code is here-------------
    # ser=serial.Serial("/dev/ttyAMA0", baudrate=9600,timeout = 5)
    # dataout =pynmea2.NMEAStreamReader() 
    # newdata=ser.readline()
    #if '$GPRMC' in str(newdata):
        #print(newdata.decode('utf-8'))

            #newmsg=pynmea2.parse(newdata.decode('utf-8'))  
            #lat=newmsg.latitude 
            #lng=newmsg.longitude 
            #gps = "Latitude=" + str(lat) + "and Longitude=" +str(lng)
    # gps code end here---------------------

    gps = '9.57 , 77.67'
    now = datetime.datetime.now()
    timestamp = datetime.datetime.timestamp(now)*1000    
    
    url = 'http://172.20.122.101:8000/hwd/update'
    
    try:
        file1 = open("secret_key.txt",'r')
        a = [] # Store hardware credential---------
        b = [] # store data in file----------------
        for each in file1:
            a.append(each)
        for each2 in file:
            b.append(each2)
        # code to push data from file to blockchain---------
        if(len(b) != 0):
            br = [] #store data(temp humidity and gps)
            while(len(b)!= 0):
                br.append({b[0]}) 
                b.remove(b[0])
                time.sleep(1)
            myobj = {'hardware_id': str(a[0]).replace('\n',''),
                    'hardware_secret_key' : str(a[1]).replace('\n',''),
                    "data": br
                }
            x = requests.post(url, json = myobj)
            print(x.text)    
        # take data from gps and sensor and if there is internet connectivity will upload it to blockchain.----------
        ar = []
        for i in range(1):
            gps = '9.57 , 77.67'
            now = datetime.datetime.now()
            timestamp = datetime.datetime.timestamp(now)*1000    
            humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
            ar.append({"timestamp":timestamp, "temperature":temperature , "humidity":humidity ,"gps":gps })
            time.sleep(2)
        myobj = {'hardware_id': str(a[0]).replace('\n',''),
                    'hardware_secret_key' : str(a[1]).replace('\n',''),
                    "data": ar
                }
        x = requests.post(url, json = myobj)
        print(x.text)
        print(myobj)        


    # Code to save data on file in case not able to post data on blockchain-------------------------------       
    except:
       file.write("timestamp"+":"+ str(timestamp) + ", "+"temperature"+":"+ str(temperature) +", "+ "humidity"+":" +str(humidity) + "," + "gps"+":"+str(gps) + "\n")            
       print("no")

    # This code print the exception in whole program------------------------   
    # except Exception as e:
    #     print(e)   