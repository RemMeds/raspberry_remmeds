#!/usr/bin/python
# coding=utf-8


import MySQLdb
import datetime
import requests
import replace_data
import socket #test internet connection
import datetime

#list = map(key, value)
def addhisto(data):
    print("HISTORIQUE")
    dbLocal = MySQLdb.connect("localhost", "usrRemMeds", "azerty", "remmeds")
    cursorLocal = dbLocal.cursor()

    date = datetime.datetime.now()
    print(data)
    print("--------------")
    day = replace_data.replace(str(date.day), "num")
    month = replace_data.replace(str(date.month), "num")
    date = str(day) + "-" + str(month) + "-" + str(date.year)

    cursorLocal.execute("select com_name from rm_compartment where com_num = " + str(data["Comp"]))
    drugName = cursorLocal.fetchone()
    drugName = drugName[0]

    cursorLocal.execute("insert into rm_historic (us_id, hi_drugname, hi_hours, hi_day,"
                        "hi_takenrespected, hi_num_comp, hi_time_slot)"
                        "values ('" + str(selectUserID()) + "','" + drugName + "','" + str(data["Hour"]) + "',"
                        "'" + str(date) + "','" + str(data["hi_takenrespected"]) + "','" + str(data["Comp"]) + "',"
                        "'" + str(data["TimeSlot"]) + "');")
    dbLocal.commit()

    print("Local OK")
    print("--------------")

    #Check si on est connecte a internet
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("www.google.com", 80))
        print("connecte")
        connect = 1
    except socket.gaierror:
        print("Pas connecte")
        connect = 0

    #Si on est bien connecte
    if(connect):
        #pour chaque historique.
        cursorLocal.execute("select * from rm_historic;")
        #Fetch all row.
        data = cursorLocal.fetchall()

        #For each line in historic
        for row in data:
            #Envoyer les donnees a l'API.
            print("http://212.73.217.202:15020/historic/add_historic/"+str(row[1])+"&"+str(row[2])+"&"+str(row[3])+"&"
                          ""+str(row[4])+"&"+str(row[5])+"&"+str(row[6])+"&"+str(row[7])+"")
            requests.post("http://212.73.217.202:15020/historic/add_historic/"+str(row[1])+"&"+str(row[2])+"&"+str(row[3])+"&"
                          ""+str(row[4])+"&"+str(row[5])+"&"+str(row[6])+"&"+str(row[7])+"")


        #Supprimer les donnees historique de la bdd locale pour eviter les doublons.
        cursorLocal.execute("DELETE FROM rm_historic;")
        dbLocal.commit()

    dbLocal.close()


def sameData(data, map):
    dbLocal = MySQLdb.connect("localhost", "usrRemMeds", "azerty", "remmeds")
    cursorLocal = dbLocal.cursor()

    #print(data)
    #print(map['ID'])
    for i in data:
        #print(data[i])
        slt = replace_data.replace(i, map['table'])

        #print("select "+str(slt)+" from  "+map['table']+" where "+map['cdt']+" = " + str(map['ID'])+";")

        cursorLocal.execute("select "+str(slt)+" from  "+map['table']+" where "+map['cdt']+" = " + str(map['ID']))
        # Fetch row.
        dt = cursorLocal.fetchone()

        #print(dt[0])

        newData = data[i]

        if (newData == None):
            newData = ""

        #print(newData)

        if(newData != dt[0]):
            #print("KO")

            #print("update "+map['table']+" set "+slt+" = '"+str(newData)+"' where "+map['cdt']+" = " + str(map['ID'])+";")

            cursorLocal.execute("update "+map['table']+" set "+slt+" = '"+str(newData)+"' where "+map['cdt']+" = " + str(map['ID'])+";")
            dbLocal.commit()



def checkIfExists(id, table, name):
    db = MySQLdb.connect("localhost", "usrRemMeds", "azerty", "remmeds")
    cursor = db.cursor()

    #print("checkIfExists")

    cursor.execute("select * from " + table + " where " + name + " = " + str(id))
    data = cursor.fetchone()

    #print(data)
    #print("\n\n")

    if(data):
        #print("False")
        return False
    else:
        #print("True")
        return True


def synchroBDD(userID):
    dbLocal = MySQLdb.connect("localhost", "usrRemMeds", "azerty", "remmeds")
    cursorLocal = dbLocal.cursor()

    userID = str(userID)

    #-------------------------------------------------------------------------------------------------------------
    #For User

    # Fetch all row from user.
    r = requests.get("http://212.73.217.202:15020/raspberry/get_user/" + str(userID))
    result = r.json()
    data = result["user"][0]
    #print(data)
    #print(data["user_id"])
    #print("\n")

    if(checkIfExists(data["user_id"], "rm_user", "us_id")):
        liste = []
        for i in data:
            #print (i)
            if(i != None):
                liste.append(str(i))
            else:
                liste.append("")
        #print("\n\n")
        #print(data[0])
        #print("\n\n")
        #print(liste)

        cursorLocal.execute("insert into rm_user (us_id, us_lastname, us_firstname, us_mail, us_prefbreakfast,"
                            "us_preflunch, us_prefdinner, us_prefbedtime)"
                            "values ('"+str(data["user_id"])+"','"+str(data["lastname"])+"','"+str(data["firstname"])+"','"+str(data["mail"])+"',"
                            "'"+str(data["pref_breakfast"])+"','"+str(data["pref_lunch"])+"','"+str(data["pref_dinner"])+"','"+str(data["pref_bedtime"])+"');")
        dbLocal.commit()

        liste = []
    else:
        map = {}
        map['ID'] = userID
        map['table'] = "rm_user"
        map['cdt'] = "us_id"

        sameData(data, map)

    # -------------------------------------------------------------------------------------------------------------
    # For compartment
    # Fetch all compartment from user.
    r = requests.get("http://212.73.217.202:15020/compartment/list_com/" + str(userID))
    result = r.json()
    data = result["compartment"]
    #print(data)

    liste = []
    for row in data:
        #print(row)
        #print(row["compartment_id"])
        #print("\n")
        if (checkIfExists(row["compartment_id"], "rm_compartment", "com_id")):
            for i in row:
                if(row[i] != None):
                    #print(i)
                    #print(row[i])
                    liste.append(row[i])
                else:
                    liste.append("")
            #print("\n\n")
            #print(row)
            #print("\n\n")
            #print(liste)
            #print("\n\n\n\n")

            cursorLocal.execute("""insert into rm_compartment (us_id, com_id, com_durationnumb, com_days, com_check_perso_hour,
                                com_note, com_name, com_frequency, com_num, com_list_pref, com_hour, com_durationtext)
                                values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""", liste)
            dbLocal.commit()

            liste = []

        else:
            map = {}
            map['ID'] = row["compartment_id"]
            map['table'] = "rm_compartment"
            map['cdt'] = "com_id"

            sameData(row, map)


    # -------------------------------------------------------------------------------------------------------------
    #For Repertory
    # Fetch all contact from user.

    r = requests.get("http://212.73.217.202:15020/raspberry/list_contact/" + str(userID))
    result = r.json()
    data = result["contact"]
    #print(data)

    #print("\n\n")

    liste = []
    for row in data:
        #print(row)
        #print(row["contact_id"])
        #print("\n")
        if (checkIfExists(row["contact_id"], "rm_repertory", "re_id")):
            for i in row:
                if(row[i] != None):
                    #print(i)
                    #print(row[i])
                    liste.append(row[i])
                else:
                    liste.append("")
            #print("\n\n")
            #print(row)
            #print("\n\n")
            liste.append(userID)
            #print(liste)
            #print("\n\n\n\n")


            cursorLocal.execute("""insert into rm_repertory (re_chxSMS, re_firstname, re_lastname, re_id, re_note,
                               re_phonenumber, re_mail, re_chxMail, us_id)
                               values (%s, %s, %s, %s, %s, %s, %s, %s, %s);""", liste)
            dbLocal.commit()

            liste = []
        else:
            map = {}
            map['ID'] = row["contact_id"]
            map['table'] = "rm_repertory"
            map['cdt'] = "re_id"

            sameData(row, map)
    # -------------------------------------------------------------------------------------------------------------

    return "Synchro";

def resetBDD():
    dbLocal = MySQLdb.connect("localhost", "usrRemMeds", "azerty", "remmedsTest")
    cursor = dbLocal.cursor()
    cursor.execute("DELETE FROM rm_comp_preset;")
    cursor.execute("DELETE FROM rm_compartment;")
    cursor.execute("DELETE FROM rm_connect;")
    cursor.execute("DELETE FROM rm_historic;")
    cursor.execute("DELETE FROM rm_repertory;")
    cursor.execute("DELETE FROM rm_user;")
    dbLocal.commit()
    dbLocal.close()
    return "RESET";


def checkComp():
    #print("CheckComp")
    #print("------------------------------------------")

    map = {}
    result = False
    for numComp in range(1,9):
        dbLocal = MySQLdb.connect("localhost", "usrRemMeds", "azerty", "remmeds")
        cursor = dbLocal.cursor()
        """
        print("------------------------------------------")
        print("Numero du compartiment")
        print(numComp)
        """

        #Récupérer le jour de la semaine.
        day = replace_data.days(str(datetime.datetime.today().weekday()))

        #Récuéprer tous les jours ou l'utilisateur devra prendre le médicament du compartiement i
        cursor.execute("select com_days from rm_compartment where com_num = " + str(numComp))
        comDays = cursor.fetchone()
        """
        print("Tous les jours de la semaine")
        print(comDays)
        print("Du compartiment")
        print(numComp)
        """
        if(comDays): #Or '0' ?
            comDays = comDays[0]
            #print("ELIF")
            #print(comDays)
            if(comDays == "0" or comDays == ""):
                #print("It must be True")
                result = True
            else:
                list = comDays.split(",")
                for i in list:
                    if(str(i) == day):
                        #print("OK")
                        result = True
        else:
            result = True

        if(result):
            #print("result = true")
            result = False
            time = datetime.datetime.now()
            minute = str(time.minute)
            hour = str(time.hour)

            minute = replace_data.replace(minute, "num")
            hour = replace_data.replace(hour, "num")
            date = hour + ":" + minute

            #Heure perso
            cursor.execute("select com_hour from rm_compartment where com_num = " + str(numComp))
            comHour = cursor.fetchone()
            #print(comHour)
            if(comHour):
                #print("if")
                comHour = comHour[0]

                if(date == comHour):
                    map["Hour"] = date
                    map["Comp"] = numComp
                    map["TimeSlot"] = "Perso"
                    print(map)
                    return map #C'est pour le moment qu'a condition que l'utilisateur doit prendre qu'un seul médicament
                                # Il ne peut en prendre deux à la même heure a la même minute. #TODO gérer cela

            #Heure Petit dej / dej / diner / couché
            cursor.execute("select com_list_pref from rm_compartment where com_num = " + str(numComp))
            comListPref = cursor.fetchone()
            comListPref = comListPref[0]
            list = comListPref.split(",")
            pref = ""
            for i in list:
                if(i == "Breakfast"):
                    pref = "us_prefbreakfast"
                    map["TimeSlot"] = str(i)
                elif(i == "Lunch"):
                    pref = "us_preflunch"
                    map["TimeSlot"] = str(i)
                elif(i == "Dinner"):
                    pref = "us_prefdinner"
                    map["TimeSlot"] = str(i)
                else:
                    pref = "us_prefbedtime"
                    map["TimeSlot"] = str(i)

                cursor.execute("select "+str(pref)+" from rm_user")
                comHour = cursor.fetchone()
                comHour = comHour[0]

                if(date == comHour):
                    map["Hour"] = date
                    map["Comp"] = numComp
                    print(map)
                    return map #C'est pour le moment qu'a condition que l'utilisateur doit prendre qu'un seul médicament
                                # Il ne peut en prendre deux à la même heure a la même minute. #TODO gérer cela



def selectUserID():
    db = MySQLdb.connect("localhost", "usrRemMeds", "azerty", "remmeds")
    cursor = db.cursor()

    #print("checkIfExists")

    cursor.execute("select us_id from rm_user")
    data = cursor.fetchone()
    user = data[0]
    print(user)
    return user


#print(resetBDD())

#print(synchroBDD(1))


"""

liste1 = {}

liste1["us_id"] = 1
liste1["Hour"] = "11:00"
liste1["hi_takenrespected"] = 1
liste1["hi_day"] = "15-04-2018"
liste1["Comp"] = 2
liste1["TimeSlot"] = "Perso"


print(addhisto(liste1))
"""

