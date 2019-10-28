import socket

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('192.168.137.123',5151))
while 1:
	data = input('>')
	clientsocket.send(bytes(data, "utf-8"))

clientsocket.close()