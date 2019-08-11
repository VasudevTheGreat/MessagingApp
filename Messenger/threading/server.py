import threading
import socket
import base64
import hashlib
import codecs
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, KeySerializationEncryption
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey, X25519PublicKey
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.fernet import Fernet
import requests
import os

private_key_alice = X25519PrivateKey.generate()
public_key_alice = private_key_alice.public_key()

global credResult
credResult = 0

clientCounter = 0
clients = {}
conns = []
addrs = []
threads = []
derived_keys = []

s = socket.socket()
host = socket.gethostname() 
port = 12345
s.bind((host,port))

s.listen(5)

m = hashlib.sha256()
'''
s2 = socket.socket()
host2 = socket.gethostname()
s2.connect((host2,port))
'''
def acceptConns():
	global clientCounter
	print("Accepting Connections")
	while True:
		client = {}
		c, addr = s.accept()
		print("New client has been found %s %s" % (c, addr))
		client['conn'] = c
		client['addr'] = addr
		print("Sending pub key")
		c.send(public_key_alice.public_bytes(Encoding.Raw, PublicFormat.Raw)) #sends public key
		print("Waiting for their pub key")
		peer_public_bob_raw = (c.recv(2048))
		peer_public_bob = X25519PublicKey.from_public_bytes(peer_public_bob_raw)
		shared_key = private_key_alice.exchange(peer_public_bob)
		derived_key = HKDF(algorithm = hashes.SHA256(),length = 32,salt = None,info = b'handshake data',backend = default_backend()).derive(shared_key)
		client['key'] = derived_key
		print(client)
		
		
		
		f = Fernet(base64.urlsafe_b64encode(derived_key))
		connectedMessage = f.encrypt('Connected'.encode())
		c.send(connectedMessage) #need to encrypt this message as well
		conns.append(c)
		addrs.append(c)
		clients[clientCounter] = client
		clientCounter+=1
		
		t = threading.Thread(target=handleClient,kwargs=(client))
		threads.append(t)
		
		t.start()
		
		#print(message)
	return

#t = threading.Thread(target=acceptConns)
#t.start()

def handleClient(conn, addr, key):
	f = Fernet(base64.urlsafe_b64encode(key))
	#message = c.recv(2048)
	while True:
		
		message = conn.recv(2048)
		print(message)
		

		#message = base64.urlsafe_b64decode(message)
		decrypted = f.decrypt(message).decode()
		
		print(decrypted)
		if (decrypted[:6] == "signup"):
			splitCredentials = decrypted.split(" ")
			username = splitCredentials[1]
			password = splitCredentials[2]
			
			salt = codecs.encode(os.urandom(16), 'hex')			
			m.update(base64.b64encode(bytes(password, 'utf-8')) + salt)			
			hashed_password = m.hexdigest()

			
			
			URL = "http://localhost:3000/register"
			data = {'username':username, 'hashed_password':hashed_password, 'salt':salt}
			print("sending creds for register")
			r = requests.post(url = URL, data = data)
			
			
		elif (decrypted[:5] == "login"):
			splitCredentials = decrypted.split(" ")
			username = splitCredentials[1]
			password = splitCredentials[2]
			
			

			
			
			URL = "http://localhost:3000/login"
			data = {'username':username}
			print("sending creds for login")
			r = requests.post(url = URL, data = data)
			response = r.json()
			print(response)
			
			
			# hashed_password = bytes.fromhex(response["hashed_password"])
			# salt = bytes.fromhex(response["salt"][:32])
			
			hashed_password_2 = response["hashed_password"] #hashed password from the database
			salt_2 = response["salt"][:32] #salt from the database
			print(salt_2)
			
			m.update(base64.b64encode(bytes(password, 'utf-8')) + salt_2.encode()) #hashing the user entered password using salt from database
			client_hashed_password = m.hexdigest()
			
			print(hashed_password_2)
			print(client_hashed_password)
			
			if client_hashed_password == hashed_password_2:
				print("Same")
				credResult = 1
			else:
				conn.send("Hello".encode())
		

		else:
			for id,client in clients.items():
				fr = Fernet(base64.urlsafe_b64encode(client['key']))
				
				print((fr.encrypt(decrypted.encode())))
				client['conn'].send((fr.encrypt(decrypted.encode())))
				
		
	return

acceptConns()

#cd documents\messenger\threading
