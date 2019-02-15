import socket, time

host = socket.gethostbyname(socket.gethostname()) #system characteristic
port = 9090
clients = []
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
quit = False
print("[Server Started IP: " + host + "]") #this address you need to paste in server ins client.py

while not quit:
	try:
		data, addr = s.recvfrom(1024)
		if addr not in clients:
			clients.append(addr)

		itsatime = time.strftime("%Y-%m-%d, %H:%M:%S", time.localtime())
		print("["+addr[0]+"]-["+str(addr[1])+"]-["+itsatime+"]/",end="")
		print(data.decode("utf-8")) #bytes -> string (= message)

		for client in clients:
			if addr != client:
				s.sendto(data, client) #send either in utf-8
	except:	
		print("\n[Server Stopped]")
		quit = True
		
s.close()
