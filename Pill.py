#!/usr/bin/python
# coding=utf-8

# Les modules necessaires sont importes et mis en place
import RPi.GPIO as GPIO
import time
import Connection
import ReplaceData
import Mail
import MySQLdb
import os

"""
Déclaration de la variable d'environnement
"""


"""
Etat d'une pin 
state = GPIO.input(pin)

sources : https://www.raspberrypi.org/forums/viewtopic.php?t=38753
"""

def ledOn(map):
    print(map)
    print("LEDON")
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    #hour = map["Hour"]
    comp = map["Comp"]
    pin = ReplaceData.comToPin(str(comp))
    pin = int(pin)

    #active led light for 30 minutes
    GPIO.setup(pin, GPIO.OUT)
    #print("LED on")
    GPIO.output(pin, GPIO.LOW)
    time.sleep(30)  #1800 Timer 30 minutes In seconds

    #Une fois la demi heure passé, on vérifie l'état de la pin.
    state = GPIO.input(pin)
    if(state == 0):
        Mail.alertMissing(map) #TODO Retirer le commentaire.
        map["hi_takenrespected"] = "0"
        Connection.addhisto(map)


    ledOff(map)


def ledOff(map):
    print("LEDOFF")
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    comp = map["Comp"]
    pin = ReplaceData.comToPin(str(comp))
    pin = int(pin)

    GPIO.setup(pin, GPIO.OUT)
    #print("LED off")
    GPIO.output(pin, GPIO.HIGH)


def led(map):
    #print(map)
    print("LED")
    if(map["call"] == "Main"):
        ledOn(map)

    else:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        comp = map["Comp"]
        pin = ReplaceData.comToPin(str(comp))
        pin = int(pin)

        GPIO.setup(pin, GPIO.OUT)

        state = GPIO.input(pin)
        print(state)
        if(state == 0):
            ledOff(map)
            map["hi_takenrespected"] = "1"
            print('TRUE')
            #retrieve timeslot
            dbLocal = MySQLdb.connect("localhost", "usrRemMeds", "azerty", "remmeds")
            cursorLocal = dbLocal.cursor()

            now = str(map["Hour"])
            hour = now[0] + now[1]
            minute = int(now[3] + now[4]) - 30
            if (minute < 0):
                hour = int(hour) - 1
                minute = 60 + minute
                after = str(hour) + ":" + str(minute)
            else:
                after = str(hour) + ":" + str(minute)

            cursorLocal.execute(
                "select * from rm_compartment where com_hour between '" + str(after) + "' and '" + str(now) + "';")
            data = cursorLocal.fetchall()

            if (data):
                map["TimeSlot"] = "Perso"
            else:
                cursorLocal.execute(
                    "select * from rm_user where us_prefbreakfast between '" + str(after) + "' and '" + str(now) + "'")
                data = cursorLocal.fetchone()
                if (data):
                    map["TimeSlot"] = "Breakfast"
                else:
                    cursorLocal.execute(
                        "select * from rm_user where us_preflunch between '" + str(after) + "' and '" + str(now) + "'")
                    data = cursorLocal.fetchone()
                    if (data):
                        map["TimeSlot"] = "Lunch"
                    else:
                        cursorLocal.execute(
                            "select * from rm_user where us_prefdinner between '" + str(after) + "' and '" + str(
                                now) + "'")
                        data = cursorLocal.fetchone()
                        if (data):
                            map["TimeSlot"] = "Dinner"
                        else:
                            cursorLocal.execute(
                                "select * from rm_user where us_prefbedtime between '" + str(after) + "' and '" + str(
                                    now) + "'")
                            data = cursorLocal.fetchone()
                            map["TimeSlot"] = "Bedtime"
            #end retrieve timeslot
            #Add to rm_historic
            Connection.addhisto(map)

        else:
            print('Mail')
            Mail.alertOpenning(map)  #TODO Retirer le commentaire.
            map["hi_takenrespected"] = "0"
            map["TimeSlot"] = "Erreur d ouverture"

            print("map ->")
            print(map)
            print("--------------")
            Connection.addhisto(map)



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