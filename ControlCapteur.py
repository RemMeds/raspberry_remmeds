#!/usr/bin/python
# coding=utf-8

# Les modules necessaires sont importes et mis en place
import RPi.GPIO as GPIO
import os
import time
import datetime
import ReplaceData
import Pill

GPIO.setmode(GPIO.BCM)

# La broche d'entree du capteur est declaree. En outre la resistance de Pull-up est activee.
GPIO_PIN = 21  # Senseur Hall branche sur GPIO 21
GPIO_PIN2 = 20  # Senseur Hall branche sur GPIO 21
GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(GPIO_PIN2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Sensor-Test [Appuyez sur Ctrl + C pour terminer le test]")

# Cette fonction de sortie est executee par detection du signal
def fonctionDeSortie(null):
    print("Signal détecté capteur 1")
    os.system("wall capteur1")

    time = datetime.datetime.now()
    minute = str(time.minute)
    minute = ReplaceData.replace(minute, "num")
    hour = str(time.hour) + ":" + minute

    list = {}
    list["Hour"] = hour
    list["Comp"] = "1"
    list["call"] = ""
    Pill.led(list)



# Cette fonction de sortie est executee par detection du signal
def fonctionDeSortie2(null):
    print("Signal détecté capteur 2")
    os.system("wall capteur2")

    time = datetime.datetime.now()
    minute = str(time.minute)
    minute = ReplaceData.replace(minute, "num")
    hour = str(time.hour) + ":" + minute

    list = {}
    list["Hour"] = hour
    list["Comp"] = "2"
    list["call"] = ""
    Pill.led(list)


# Lors de la detection d'un signal (front descendant du signal) de la fonction de sortie est declenchee
GPIO.add_event_detect(GPIO_PIN, GPIO.RISING, callback=fonctionDeSortie, bouncetime=100)
GPIO.add_event_detect(GPIO_PIN2, GPIO.RISING, callback=fonctionDeSortie2, bouncetime=100)

# Boucle de programme principale
try:
    while True:
        time.sleep(0.1)

# reinitialisation de tous les GPIO en entrees
except KeyboardInterrupt:
    GPIO.cleanup()
