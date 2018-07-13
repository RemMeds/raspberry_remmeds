#!/usr/bin/python
# coding=utf-8

import Connection
import os
import datetime
import Mail
import Pill
import ReplaceData

file = open("/remmeds/log.txt", "a")
date = datetime.datetime.now()
#print(str(date.hour)+":"+str(date.minute))
#print(data)





compNum = Connection.checkComp()
print(compNum)

if(compNum):
    Mail.infos(compNum)
    #Allumer la led pendant une heure (si la led existe)                     #Executer un script python qui tourne en boucle.
    compNum["call"] = "Main"
    #print(compNum)
    Pill.led(compNum)

minute = str(date.minute)

minute = ReplaceData.replace(minute, "num")

file.write("\nlog hour " + str(date.hour)+":"+minute +" --> "+str(compNum) + " Mail ")




#Synchro des bdd
userID = Connection.selectUserID() #Vérifier si il y'a un user en récupérant son id
if(userID): #si la variable contient un id
    #print(userID)
    Connection.synchroBDD(userID) #La synchro se lance.
    file.write("\nUserID -> "+str(userID)) #Log

file.close()

