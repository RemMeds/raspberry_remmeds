import os

def conf_wifi(ssid, mdp):

    wpa = open("/etc/wpa_supplicant/wpa_supplicant.conf", "a")

    wifi = "\n\nnetwork={\n\tssid="+ssid+"\n\tpsk="+mdp+"\n\tkey_mgmt=WPA-PSK\n}"

    wpa.write(wifi)

    os.system("service networking restart")
