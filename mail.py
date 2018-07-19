#!/usr/bin/python
# coding=utf-8

# import necessary packages
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import MySQLdb

def mail(message, subject, To):
    # create message object instance
    msg = MIMEMultipart()

    # setup the parameters of the message
    password = "@azerty$"
    msg['From'] = "projet.remmeds@gmail.com" #RemMeds@outlook.fr #remmeds@yahoo.com #projet.remmeds@gmail.com
    msg['To'] = str(To)
    msg['Subject'] = str(subject) # L'objet du mail

    # add in the message body
    msg.attach(MIMEText(message, 'plain'))

    # create server
    server = smtplib.SMTP('smtp.gmail.com: 587') #smtp-mail.outlook.com: 587 #smtp.mail.yahoo.com: 587 #smtp.gmail.com: 465

    server.starttls()

    # Login Credentials for sending the mail
    server.login(msg['From'], password)

    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())

    server.quit()

    print ("successfully sent email to %s:" % (msg['To']))



def infos(list):
    dbLocal = MySQLdb.connect("localhost", "usrRemMeds", "azerty", "remmeds")
    cursor = dbLocal.cursor()

    cursor.execute("select com_name from rm_compartment where com_num = " + str(list["Comp"]))
    drugName = cursor.fetchone()

    cursor.execute("select us_firstname, us_mail from rm_user")
    userData = cursor.fetchone()
    userName = userData[0]
    userMail = userData[1]

    message = "Bonjour "+str(userName)+", \n\n" \
              "Il est "+str(list["Hour"])+" et vous devez prendre le medicament "+str(drugName[0])+" \n" \
              "qui est dans le compartiment "+str(list["Comp"])+" \n"
    #le corps du message

    mail(message, "Rappel", userMail)


def alertMissing(list):
    print(list)
    dbLocal = MySQLdb.connect("localhost", "usrRemMeds", "azerty", "remmeds")
    cursor = dbLocal.cursor()

    cursor.execute("select com_name from rm_compartment where com_num = " + str(list["Comp"]))
    drugName = cursor.fetchone()

    #For the user
    cursor.execute("select us_firstname, us_mail from rm_user")
    userData = cursor.fetchone()
    userName = userData[0]
    userMail = userData[1]

    message = "Bonjour "+str(userName)+", \n\n" \
              "Vous avez oublie de prendre le medicament "+str(drugName[0])+". Il est dans le compartiment "+str(list["Comp"])+"" \
              "Vous deviez le prendre à "+str(list["Hour"])
    #le corps du message pour l'utilisateur.

    mail(message, "Alerte ! Medicament oublie", userMail)

    #For contacts
    cursor.execute("select re_firstname, re_mail from rm_repertory")
    data = cursor.fetchall()
    for row in data:
        reName = row[0]
        reMail = row[1]

        print(reName)
        print(reMail)

        message = "Bonjour "+str(reName)+", \n\n" \
                  ""+str(userName)+" a oublie de prendre le medicament "+str(drugName[0])+" qu'il devait prendre a "+str(list["Hour"])
        #le corps du message pour l'utilisateur.

        mail(message, "Alerte ! Medicament oublie", reMail)


def alertOpenning(list):
    dbLocal = MySQLdb.connect("localhost", "usrRemMeds", "azerty", "remmeds")
    cursor = dbLocal.cursor()

    cursor.execute("select com_name from rm_compartment where com_num = " + str(list["Comp"]))
    drugName = cursor.fetchone()

    #For the user
    cursor.execute("select us_firstname, us_mail from rm_user")
    userData = cursor.fetchone()
    userName = userData[0]
    userMail = userData[1]

    message = "Bonjour "+str(userName)+", \n\n" \
              "Vous avez ouvert le compartiment "+list["Comp"]+" qui contenait du "+str(drugName[0])+". " \
              "Vous ne devriez pas en consommer hors des heures de prises conseillées par le médecin."


    #le corps du message pour l'utilisateur.

    mail(message, "Alerte ! Compartiment ouvert", userMail)

    #For contacts
    cursor.execute("select re_firstname, re_mail from rm_repertory")
    data = cursor.fetchall()
    for row in data:
        reName = row[0]
        reMail = row[1]

        message = "Bonjour "+str(reName)+", \n\n" \
                  ""+str(userName)+" à ouvert le compartiment "+list["Comp"]+" qui contenait du "+str(drugName[0])+" " \
                  "en dehors des heures de prises conseillées par le médecin."
        #le corps du message pour l'utilisateur.

        mail(message, "Alerte ! Compartiment ouvert", reMail)