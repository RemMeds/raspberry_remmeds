#!/usr/bin/python
# coding=utf-8

# Les modules necessaires sont importes et mis en place
import RPi.GPIO as GPIO
import time
import connection
import replace_data
import mail
import MySQLdb
import os


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
    pin = replace_data.comToPin(str(comp))
    pin = int(pin)

    #active led light for 30 minutes
    GPIO.setup(pin, GPIO.OUT)
    #led on
    GPIO.output(pin, GPIO.LOW)
    time.sleep(30)  #1800 Timer 30 minutes In seconds

    #Once half an hour has passed, check the condition of the pine
    state = GPIO.input(pin)
    #if led is on
    if(state == 0):
        mail.alertMissing(map)
        map["hi_takenrespected"] = "0"
        connection.addhisto(map)
    #led off
    ledOff(map)


def ledOff(map):
    print("LEDOFF")
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    comp = map["Comp"]
    pin = replace_data.comToPin(str(comp))
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
        pin = replace_data.comToPin(str(comp))
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
            connection.addhisto(map)

        else:
            print('Mail')
            mail.alertOpenning(map)
            map["hi_takenrespected"] = "0"
            map["TimeSlot"] = "Erreur d ouverture"

            print("map ->")
            print(map)
            print("--------------")
            connection.addhisto(map)
