#!/usr/bin/python
# coding=utf-8

# Les modules necessaires sont importes et mis en place
import RPi.GPIO as GPIO
import time
import Connection
import ReplaceData
import Mail

import os
"""
Déclaration de la variable d'environnement
"""
#Variable global
params = {}


"""
Etat d'une pin 
state = GPIO.input(pin)

sources : https://www.raspberrypi.org/forums/viewtopic.php?t=38753
"""

def ledOn(map):

    print("LEDON")
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    #hour = map["Hour"]
    comp = map["Comp"]
    pin = ReplaceData.comToPin(str(comp))
    pin = int(pin)

    #active led light for an hour
    GPIO.setup(pin, GPIO.OUT)
    #print("LED on")
    GPIO.output(pin, GPIO.LOW)
    time.sleep(10)  #1800 Timer 30 minutes In seconds
    #Une fois la demi heure passé, on vérifie l'état de la  ariable params.
    if(params[str(map["Comp"])] == True):
        Mail.alertMissing(map)

    ###########
    #print(map)
    ledOff(map)
    ###########
    """
    if (params[str(map["Comp"])]):
        print("Mail Alerte Missing + led off")
        Mail.alertMissing(map)
        ledOff(map)
    """

def ledOff(map):
    print("LEDOFF")
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    print(params)
    comp = map["Comp"]
    pin = ReplaceData.comToPin(str(comp))
    pin = int(pin)
    params[str(map["Comp"])] = False
    print(params)

    GPIO.setup(pin, GPIO.OUT)
    #print("LED off")
    GPIO.output(pin, GPIO.HIGH)


def led(map):
    #print(map)
    print("LED")
    if(map["call"] == "Main"):
        #print(str(map["Comp"]))
        params[str(map["Comp"])] = True
        ledOn(map)

    else:
        #print("check")
        if(params[map["Comp"]]):
            #print("ledOff(map)")
            pass
        else:
            #print("Mail.alertOpenning(map)")
            pass



def check(numCom):
    #Récupérer l'heure + le jour
    if(Connection.checkHour(numCom)):
        print("Add to Historique")
    else:
        Mail.alertOpenning(numCom)



"""
list = {}
list["Hour"] = "20:26"
list["Comp"] = "1"
list["call"] = "Main"

params[list["Comp"]] = True


ledOn(list)
"""

"""
#LEDOFF
list = {}
list["Comp"] = "1"
ledOff(list)


list["Comp"] = "2"
ledOff(list)
"""