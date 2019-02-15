import socket, threading, time

#TODO make input of this key (=PIN CODE)
shutdown = False
join = False

def receving (name, sock):
	while not shutdown:
		try:
			while True:
				data, addr = sock.recvfrom(1024)

				decrypt = ""
				k = False
				for i in data.decode("utf-8"):
					if i == ":":
						k = True
						decrypt += i
					elif k == False or i == " ":
						decrypt += i
					else:
						decrypt += chr(ord(i)^key)
				print(decrypt)

				time.sleep(0.2)
		except:
			pass
host = socket.gethostbyname(socket.gethostname()) #if this doesn't work, paste your IPv4-address (from ipconfig in cmd/bash)
#print(host)
port = 0

server = ("192.168.1.23", 9090) #client must know, where is chat server 

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0) #need this to circumvent some errors

alias = input("Enter your name: ")

needPass = True
while needPass: #equivalent to authentification
        key = input("Enter your secret key, from 1000 to 9999:") 
        if len(key) != 4:
                continue
        try:        
                key =int(key)
                needPass = False
        except: #if it wasn't number
                continue
                

rT = threading.Thread(target = receving, args = ("RecvThread", s)) #multithreading to enable good recieving of messages
rT.start()

while shutdown == False:
	if join == False:
		s.sendto(("[User Action] [" + alias + "] join chat ").encode("utf-8"),server)
		join = True 
	else:
		try:
			message = input()

			crypt = ""
			for i in message:
				crypt += chr(ord(i)^key) #XOR encryption
			message = crypt

			if message != "":
				s.sendto(("[" + alias + "] :: "+ message).encode("utf-8"), server) #can't send without encoding string in bytes
			
			time.sleep(0.2) #better to use it to limit sending
		except: #Ctrl+C and errors at client app
			s.sendto(("[User Action] [" + alias + "] left chat ").encode("utf-8"), server)
			shutdown = True

rT.join()
s.close()
