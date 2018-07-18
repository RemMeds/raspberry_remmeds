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


#Synchro des bdd
userID = Connection.selectUserID() #Vérifier si il y'a un user en récupérant son id
if(userID): #si la variable contient un id
    #print(userID)
    Connection.synchroBDD(userID) #La synchro se lance.
    file.write("\nUserID -> "+str(userID)) #Log




compNum = Connection.checkComp()
print(compNum)

if(compNum):
    Mail.infos(compNum) #TODO Retirer le commentaire
    compNum["call"] = "Main"
    print("APPEL LED")
    Pill.led(compNum)
minute = str(date.minute)

minute = ReplaceData.replace(minute, "num")

file.write("\nlog hour " + str(date.hour)+":"+minute +" --> "+str(compNum) + " Mail ")





file.close()

