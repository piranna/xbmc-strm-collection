from socket import *

serverHostName = '192.168.0.106'
serverPort = 30000
pw = "abc123#?"

clientsocket = socket(AF_INET, SOCK_STREAM)
clientsocket.connect((serverHostName, serverPort))
clientsocket.send(pw)
