import MySQLdb
import csv
import os

dbDebian = MySQLdb.connect("localhost", "usrRemMeds", "azerty", "remmedsTest")
cursorDebian = dbDebian.cursor()

# For User
cursorDebian.execute("select * from rm_user where us_id = 2 ;")
# Fetch all row.
data = cursorDebian.fetchall()
print("retrieve data")
print(data)


#-------------------------------------------------------
print("create and open doc")
file = open("fichier.csv", "wb")


print("write in file")
writer = csv.writer(file)

print("write data in file")
writer.writerow(data[0])

file.close()

print("delete csv")
#os.remove("fichier.csv")


print("open doc")
file = open("fichier.csv", "rb")

print("use the csv to fuck")
reader = csv.DictReader(file)

print(reader)

for row in reader:
    print(row)

