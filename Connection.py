import MySQLdb
import datetime
import requests
import ReplaceDataApi
import socket #test internet connection
import datetime

#list = map(key, value)
def addhisto(data, userID):
    dbLocal = MySQLdb.connect("localhost", "usrRemMeds", "azerty", "remmeds")
    cursorLocal = dbLocal.cursor()

    cursorLocal.execute("insert into rm_historic (us_id, hi_drugname, hi_hours, hi_day,"
                        "hi_takenrespected)"
                        "values ('" + str(data["us_id"]) + "','" + str(data["hi_drugname"]) + "','" + str(data["hi_hours"]) + "',"
                        "'" + str(data["hi_day"]) + "','" + str(data["hi_takenrespected"]) + "');")
    dbLocal.commit()

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
            #print(row[1])
            requests.post("http://212.73.217.202:15020/raspberry/add_historic/"+str(row[1])+"&"+str(row[2])+"&"+str(row[3])+"&"
                          ""+str(row[4])+"&"+str(row[5])+"")


        #Supprimer les donnees historique de la bdd locale pour eviter les doublons.
        cursorLocal.execute("DELETE FROM rm_historic;")
        dbLocal.commit()

        #Lancer une nouvelle synchronisation
        synchroBDD(userID)
    dbLocal.close()


def sameData(data, map):
    dbLocal = MySQLdb.connect("localhost", "usrRemMeds", "azerty", "remmeds")
    cursorLocal = dbLocal.cursor()

    #print(data)
    #print(map['ID'])
    for i in data:
        #print(data[i])
        slt = ReplaceDataApi.replace(i, map['table'])

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


def checkHour(numComp):
    date = datetime.datetime.now()
    hour = str(date.hour) # + ":" + str(date.minute)
    dbLocal = MySQLdb.connect("localhost", "usrRemMeds", "azerty", "remmeds")
    cursor = dbLocal.cursor()

    numComp = str(numComp)
    cursor.execute("select com_id from rm_compartment where com_num = " + numComp)

    idComp = cursor.fetchone()

    idComp = str(idComp[0])

    cursor.execute("select cpe_hour from rm_comp_preset where com_id = " + idComp)


    result = cursor.fetchall()
    bool = False

    for row in result:
        row = row[0]
        print(row)
        if(row == hour):
            bool = True
            break

    if(bool):
        return True
    else:
        return False



def checkComp():
    map = {}
    for numComp in range(1,9):
        dbLocal = MySQLdb.connect("localhost", "usrRemMeds", "azerty", "remmeds")
        cursor = dbLocal.cursor()

        cursor.execute("select com_hour from rm_compartment where com_num = " + str(numComp))
        comHour = cursor.fetchone()
        comHour = comHour[0]

        time = datetime.datetime.now()
        date = str(time.hour) + ":" + str(ReplaceDataApi.replace(str(time.minute), "num"))

        if(date == comHour):
            map["Hour"] = date
            map["Comp"] = numComp
            return map






#print(resetBDD())

#print(synchroBDD(1))



"""
liste1 = {}

liste1["us_id"] = 1
liste1["hi_drugname"] = "doli"
liste1["hi_hours"] = "11:00"
liste1["hi_takenrespected"] = 1
liste1["hi_day"] = "lundi"


print(addhisto(liste1, 1))
"""

checkComp()