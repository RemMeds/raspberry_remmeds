import datetime

date = datetime.datetime.now()
print(str(date.hour)+":"+str(date.minute)+"->"+str(date.day)+"->"+str(date.month)+"->"+str(date.year))

time = datetime.time()
print(time)

jour = date.today()
print(jour)