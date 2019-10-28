 
#!/usr/bin/env python
 
import socket

def recivir(clientsocket):
	while 1:
		data = clientsocket.recv(1024)
		print(data.decode('utf-8'))
		if not data:break


serversocket    =   socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serversocket.bind(('127.0.0.1', 5151))

serversocket.listen(1)

clientsocket, clientaddress = serversocket.accept()
print('Conexion desde: ', clientaddress)
recivir(clientsocket)
clientsocket.close()
