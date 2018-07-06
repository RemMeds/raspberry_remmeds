import MySQLdb
import datetime
import requests


def addhisto(cursorDebian, userID, cursorLocal, dbLocal, table):
    cursorDebian.execute("select * from "+table+" where us_id = "+userID+" ;")
    # Fetch all row.
    data = cursorDebian.fetchall()
    #Add to local bdd
    print(data)
    for row in data:
        cursorLocal.execute("insert into "+table+"  values "+row+";")
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
    print(data)
    print(data["user_id"])
    print("\n")

    #if(checkIfExists(data["user_id"], "rm_user", "us_id")):
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

    data = str(data["user_id"])+","+str(data["lastname"])+","+str(data["firstname"])+","+str(data["mail"])+"," \
                ""+str(data["pref_breakfast"])+","+str(data["pref_lunch"])+","+str(data["pref_dinner"])+","+str(data["pref_bedtime"])+");"
    print(data)

    cursorLocal.execute("""insert into rm_user (us_id, us_lastname, us_firstname, us_mail, us_prefbreakfast,
                        us_preflunch, us_prefdinner, us_prefbedtime)
                        values (%s, %s, %s, %s, %s, %s, %s, %s);""", data)
    dbLocal.commit()

    # -------------------------------------------------------------------------------------------------------------


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


#print(resetBDD())

print(synchroBDD(18))


