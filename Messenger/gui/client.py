import socket
import base64
import threading
import os
from time import sleep
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, KeySerializationEncryption
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey, X25519PublicKey
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.fernet import Fernet
import base64

class Client:
	def __init__(self):
		self.s = socket.socket()
		host = socket.gethostname()
		port = 12345
		self.s.connect((host, port))



		self.messages = []


		private_key_bob = X25519PrivateKey.generate()
		public_key_bob = private_key_bob.public_key()

		peer_public_alice_raw = (self.s.recv(2048))
		#print(peer_public_alice_raw)

		self.s.send(public_key_bob.public_bytes(Encoding.Raw, PublicFormat.Raw))

		peer_public_alice = X25519PublicKey.from_public_bytes(peer_public_alice_raw)
		shared_key = private_key_bob.exchange(peer_public_alice)

		
		
		derived_key = HKDF(algorithm = hashes.SHA256(),length = 32,salt = None,info = b'handshake data', backend = default_backend()).derive(shared_key)
		self.f = Fernet(base64.urlsafe_b64encode(derived_key))
		t = threading.Thread(target=self.recvMessages, args=(self.s,))
		t.start()
		
	def sendMessage(self, name,  message):
		message = name + " - " + message
		#t = sign(message, 
		#message + chr(127) + 
		message = message.encode()
		
		encryptedMessage = self.f.encrypt(message)
		self.s.send(encryptedMessage)
		#s.send(message.encode())
		
	def sendCredentials(self, username, password):
		signupCredentials = "signup" + " " + username + " " + password
		encryptedCreds = self.f.encrypt(signupCredentials.encode())
		self.s.send(encryptedCreds)
		
	def sendCredentialsLogin(self, username, password):	
		loginCredentials = "login" + " " + username + " " + password
		encryptedCredsLogin = self.f.encrypt(loginCredentials.encode())
		self.s.send(encryptedCredsLogin)
		
		
	def recvMessages(self, s):
		while True:
			message = self.s.recv(2048)
			if message==b'Hello':
				self.messages.append(message.decode())
				print("Incorrect Username or Password")
				input("")
				return -1
				break
			message = self.f.decrypt(message)
			message = message.decode()
			self.messages.append(message)
			for message in self.messages:
				print(message)
				
		return






	
	def sign(self, message, key):
		h = hmac.HMAC(key, hashes.SHA256(), backend=default_backend())
		h.update(message.encode())
		t = h.finalize()
		return t
		
#cd Documents\Messenger\gui
#cd Documents\Messenger\node		
	
	
