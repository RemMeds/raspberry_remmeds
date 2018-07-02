import os

"""
# Ouverture du fichier contanant le texte
file = open("conf.txt", "r")
conf = file.read()

print(conf)

file.close()"""

with open("conf.txt", "r") as file :
    conf = file.read()

print (conf)

file.close()

#os.remove("File Path") #pour supprimer un fichier