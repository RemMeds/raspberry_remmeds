import socket

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("www.google.com", 80))
    print("connecte")
except socket.gaierror:
    print("Pas connecte")