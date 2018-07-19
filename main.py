#!/usr/bin/python
# coding=utf-8

import connection
import os
import datetime
import mail
import pill
import replace_data

file = open("/remmeds/log.txt", "a")
date = datetime.datetime.now()
#print(str(date.hour)+":"+str(date.minute))
#print(data)


#Synchro des bdd
userID = connection.selectUserID() #Vérifier si il y'a un user en récupérant son id
if(userID): #si la variable contient un id
    #print(userID)
    connection.synchroBDD(userID) #La synchro se lance.
    file.write("\nUserID -> "+str(userID)) #Log




compNum = connection.checkComp()
print(compNum)

if(compNum):
    mail.infos(compNum)
    compNum["call"] = "Main"
    print("APPEL LED")
    pill.led(compNum)
minute = str(date.minute)

minute = replace_data.replace(minute, "num")

file.write("\nlog hour " + str(date.hour)+":"+minute +" --> "+str(compNum) + " Mail ")





file.close()

