import Connection
import os
import datetime
import Mail

file = open("/home/pi/Documents/log.txt", "a")
date = datetime.datetime.now()
print(str(date.hour)+":"+str(date.minute))
#data = Connection.checkComp()
#print(data)

compNum = Connection.checkComp()
if(compNum):
    #Mail.infos(compNum)
    pass



file.write("\nlog hour " + str(date.hour)+":"+str(date.minute) +" --> "+str(compNum) + " Mail ")
file.close()




