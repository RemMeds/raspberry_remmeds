#!/usr/bin/python
# coding=utf-8

import MySQLdb
import requests

dbLocal = MySQLdb.connect("localhost", "usrRemMeds", "azerty", "remmeds")
cursorLocal = dbLocal.cursor()

# pour chaque historique.
cursorLocal.execute("select * from rm_historic;")
# Fetch all row.
data = cursorLocal.fetchall()

# For each line in historic
for row in data:

    print("http://212.73.217.202:15020/historic/add_historic/" + str(row[1]) + "&" + str(row[2]) + "&" + str(row[3]) + "&"
          "" + str(row[4]) + "&" + str(row[5]) + "&" + str(row[6]) + "&" + str(row[7]) + "")

    requests.post("http://212.73.217.202:15020/historic/add_historic/" + str(row[1]) + "&" + str(row[2]) + "&" + str(row[3]) + "&"
                  "" + str(row[4]) + "&" + str(row[5]) + "&" + str(row[6]) + "&" + str(row[7]) + "")

dbLocal.close()