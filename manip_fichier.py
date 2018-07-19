import conf_wifi

with open("/remmeds/synchro_phone.json", "r") as file:
    conf = file.readlines()

ssid = conf[0]
mdp = conf[1]
userID = conf[2]
file.close()
conf_wifi.conf_wifi(ssid, mdp)