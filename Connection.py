import MySQLdb
import datetime


# Connexion locale
def conLocal():
    dbLocal = MySQLdb.connect("localhost", "usrRemMeds", "azerty", "remmeds")
    cursor = dbLocal.cursor()

    return "testLocal"


def conDebian():
    dbDebian = MySQLdb.connect("http://212.73.217.202:10080/", "root", "azerty", "remmeds_users")
    cursor = dbDebian.cursor()

    return "testDebian";


def addToBDD(cursorDebian, userID, cursorLocal, dbLocal, table):
    cursorDebian.execute("select * from "+table+" where us_id = "+userID+" ;")
    # Fetch all row.
    data = cursorDebian.fetchall()
    #Add to local bdd
    print(data)
    for row in data:
        cursorLocal.execute("insert into "+table+"  values "+row+";")
        dbLocal.commit()

def synchroBDD(userID):
    dbDebian = MySQLdb.connect("localhost", "usrRemMeds", "azerty", "remmedsTest")
    cursorDebian = dbDebian.cursor()
    dbLocal = MySQLdb.connect("localhost", "usrRemMeds", "azerty", "remmeds")
    cursorLocal = dbLocal.cursor()

    userID = str(userID)

    #-------------------------------------------------------------------------------------------------------------
    #For User
    cursorDebian.execute("select * from rm_user where us_id = " + userID)
    # Fetch all row.
    data = cursorDebian.fetchall()
    #Add to local bdd

    liste = []
    for i in data[0]:
        print (i)
        if(i != None):
            liste.append(str(i))
        else:
            liste.append("")
    print("\n\n")
    print(data[0])
    print("\n\n")
    print(liste)

    cursorLocal.execute("""insert into rm_user (us_id, us_lastname, us_firstname, us_mail, us_mdp, us_prefbreakfast,
                        us_preflunch, us_prefdinner, us_prefbedtime)
                        values (%s, %s, %s, %s, %s, %s, %s, %s, %s);""", liste)
    dbLocal.commit()

    # -------------------------------------------------------------------------------------------------------------
    #For compartment
    cursorDebian.execute("select * from rm_compartment where us_id = " + userID)
    # Fetch all row.
    data = cursorDebian.fetchall()
    #Add to local bdd
    print(data)

    liste = []
    for row in data:
        for i in row:
            if(i != None):
                print(i)
                liste.append(i)
            else:
                liste.append("")
        print("\n\n")
        print(row)
        print("\n\n")
        print(liste)
        print("\n\n\n\n")

        cursorLocal.execute("""insert into rm_compartment (com_id, us_id, com_num, com_name, com_note, com_durationnumb,
                            com_durationtext, com_personalized, com_freqyencyeveryint, com_frequencyeverystr,
                            com_days)
                            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""", liste)
        dbLocal.commit()

        liste = []

    # -------------------------------------------------------------------------------------------------------------
    #For comp_preset
    cursorDebian.execute("select * from rm_compartment where us_id = " + userID)
    # Fetch all row.
    data = cursorDebian.fetchall()

    #For each compartment
    for x in data:
        id = x[0]
        cursorDebian.execute("select * from rm_comp_preset where com_id = " + str(id))
        # Fetch all row.
        dt = cursorDebian.fetchall()
        # Add to local bdd
        print(dt)

        liste = []
        for row in dt:
            for i in row:
                if (i != None):
                    print(i)
                    liste.append(i)
                else:
                    liste.append("")
            print("\n\n")
            print(row)
            print("\n\n")
            print(liste)
            print("\n\n\n\n")

            cursorLocal.execute("""insert into rm_comp_preset (cpe_id, com_id, cpe_meal, cpe_hour, cpe_mealWhen)
                                values (%s, %s, %s, %s, %s);""", liste)
            dbLocal.commit()

            liste = []

    # -------------------------------------------------------------------------------------------------------------
    #For Repertory
    cursorDebian.execute("select * from rm_repertory where us_id = " + userID)
    # Fetch all row.
    data = cursorDebian.fetchall()
    #Add to local bdd
    print(data)

    liste = []
    for row in data:
        for i in row:
            if(i != None):
                print(i)
                liste.append(i)
            else:
                liste.append("")
        print("\n\n")
        print(row)
        print("\n\n")
        print(liste)
        print("\n\n\n\n")

        cursorLocal.execute("""insert into rm_repertory (re_id, us_id, re_lastname, re_firstname, re_phonenumber,
                           re_mail, re_chxSMS, re_chxMail, re_note)
                           values (%s, %s, %s, %s, %s, %s, %s, %s, %s);""", liste)
        dbLocal.commit()

        liste = []
    # -------------------------------------------------------------------------------------------------------------
    #For Historic
    cursorDebian.execute("select * from rm_historic where us_id = " + userID)
    # Fetch all row.
    data = cursorDebian.fetchall()
    #Add to local bdd
    print(data)

    liste = []
    for row in data:
        for i in row:
            if(i != None):
                print(i)
                liste.append(i)
            else:
                liste.append("")
        print("\n\n")
        print(row)
        print("\n\n")
        print(liste)
        print("\n\n\n\n")

        cursorLocal.execute("""insert into rm_historic (hi_id, us_id, hi_drugname, hi_hours, 
                            hi_day, hi_takenrespected)
                           values (%s, %s, %s, %s, %s, %s);""", liste)
        dbLocal.commit()

        liste = []
    # -------------------------------------------------------------------------------------------------------------
    #For Connect
    cursorDebian.execute("select * from rm_connect where us_id = " + userID)
    # Fetch all row.
    data = cursorDebian.fetchall()
    #Add to local bdd
    print(data)

    liste = []
    for row in data:
        for i in row:
            if(i != None):
                print(i)
                liste.append(i)
            else:
                liste.append("")
        print("\n\n")
        print(row)
        print("\n\n")
        print(liste)
        print("\n\n\n\n")

        cursorLocal.execute("""insert into rm_connect (con_id, us_id, con_ssid, con_mdp)
                           values (%s, %s, %s, %s);""", liste)
        dbLocal.commit()

        liste = []
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

print(synchroBDD(555))


