from tkinter import *
from client import Client
from time import sleep

class Application(Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.client = Client()
		self.username = ""
		self.password = ""
		self.password2 = ""
		self.master = master
		self.pack()
		self.currentIndex = None
		self.create_menu()
		
	def create_menu(self):
		self.menu = Frame(self)
		self.title = Label(self.menu, text = 'Menu')
		self.menu.pack()
		self.title.pack()
		
		#create a register button
		self.registerButton = Button(self.menu)
		self.registerButton["text"] = "Click Here if you are a New User"
		self.registerButton["command"] = self.create_register
		self.registerButton.pack()
		
		#create a login button
		self.loginButton = Button(self.menu)
		self.loginButton["text"] = "Click Here if you are an Existing User"
		self.loginButton["command"] = self.create_login
		self.loginButton.pack()
		
		
		
		
	def menuDestroy(self):
		self.menu.destroy()
		
	def create_register(self):
		self.menuDestroy()
		self.registerPage = Frame(self)
		self.title = Label(self.registerPage, text = 'Sign Up')
		self.registerPage.pack()
		self.title.pack()
		#self.titleUsername = Label(self.registerPage, text = 'Username\nPassword\nRe-enter Password')
		#self.titleUsername.pack(side = LEFT)
		self.usernameEntry = Entry(self.registerPage)
		self.usernameEntry.pack()
		self.passwordEntry = Entry(self.registerPage)
		self.passwordEntry.pack()
		self.passwordEntry2 = Entry(self.registerPage)
		self.passwordEntry2.pack()
		self.usernameEntryButton = Button(self.registerPage)
		self.usernameEntryButton["text"] = "Enter"
		self.usernameEntryButton["command"] = self.setUsername
		self.usernameEntryButton.pack(side = BOTTOM)
	
	def create_login(self):
		self.menuDestroy()
		self.loginPage = Frame(self)
		self.title = Label(self.loginPage, text = 'Log In')
		self.loginPage.pack()
		self.title.pack()
		#self.titleUsername = Label(self.loginPage, text = 'Username\nPassword)
		#self.titleUsername.pack(side = LEFT)
		self.usernameEntry = Entry(self.loginPage)
		self.usernameEntry.pack()
		self.passwordEntry = Entry(self.loginPage)
		self.passwordEntry.pack()
		self.usernameEntryButton = Button(self.loginPage)
		self.usernameEntryButton["text"] = "Enter"
		self.usernameEntryButton["command"] = self.setLogin
		self.usernameEntryButton.pack(side = BOTTOM)
	
		
	def setUsername(self):
		self.username = self.usernameEntry.get()
		self.password = self.passwordEntry.get()
		self.password2 = self.passwordEntry2.get()
		if (self.username != "" and self.password != "" and self.password2 != "") and (self.password == self.password2):
			self.registerDestroy()
			# print(self.username)
			# print(self.password)
			# print(self.password2)
			self.client.sendCredentials(self.username, self.password)
			
	def setLogin(self):
		self.username = self.usernameEntry.get()
		self.password = self.passwordEntry.get()
		if (self.username != "" and self.password != ""):
			self.loginDestroy()
			# print(self.username)
			# print(self.password)
			self.client.sendCredentialsLogin(self.username, self.password)
			
	def	sendMessage(self):
		self.client.sendMessage(self.username, self.sendMessageEntry.get())
		self.sendMessageEntry.delete(0, END)
		
		
	def registerDestroy(self):
		self.registerPage.destroy()
		self.createAppPage()
		
	def loginDestroy(self):
		self.loginPage.destroy()
		self.createAppPage()
		
	def incorrectCreds(self):
		self.appPage.destroy()
		self.incorrectPage = Frame(self)
		self.incorrectPage = Message(root, text = 'Invalid username or password') 
		self.incorrectPage.config(bg='red', width = 100)
		self.incorrectPage.pack()
		sleep(5)
		break
		
	def createAppPage(self):
		self.appPage = Frame(self)
		self.title = Label(self.appPage, text = 'Message Box')
		self.title.pack(side = TOP)
		#scrollbar = Scrollbar(self) 
		#scrollbar.pack( side = RIGHT, fill = Y ) 
		self.appPage.pack()
		scrollbar = Scrollbar(self.appPage) 
		scrollbar.pack( side = RIGHT, fill = Y )
		self.mylist = Listbox(self.appPage, yscrollcommand = scrollbar.set, width = 200)
		self.mylist.pack(fill = BOTH, expand = 1) 
		self.MessageBox = Frame(self.appPage)
		self.sendMessageEntry = Entry(self.MessageBox)
		self.sendMessageEntry.pack(side = LEFT)
		self.sendMessageEntryButton = Button(self.MessageBox)
		self.sendMessageEntryButton["text"] = "Enter"
		self.sendMessageEntryButton["command"] = self.sendMessage
		self.sendMessageEntryButton.pack(side = LEFT) 
		self.MessageBox.pack(side = BOTTOM, fill = BOTH, expand = True)

		scrollbar.config( command = self.mylist.yview ) 
		self.checkMessages()
	
	def checkMessages(self):
		if "Hello" in self.client.messages:
			self.incorrectCreds()
		mesLength = len(self.client.messages)
		print(self.client.messages)
		if (self.currentIndex == None):
			self.currentIndex = 0
		
		while (self.currentIndex < mesLength):
			self.mylist.insert(END, self.client.messages[self.currentIndex])
			self.currentIndex+=1
		
		self.after(1000, self.checkMessages)
		
		
		
	
	#use Text
	
		
"""
root = Tk() 
w = Canvas(root, width=40, height=60) 
w.title('Message Box')
w.pack(side=TOP) 
canvas_height=20
canvas_width=200
scrollbar = Scrollbar(root) 
scrollbar.pack( side = RIGHT, fill = Y ) 


T = Text(root, height=2, width=30) 
T.pack() 
T.insert(END, 'texthere') 
"""




"""
messageBox.mainloop()
mainloop() 
"""

root = Tk()
app = Application(master = root)
app.mainloop()

#cd documents\messenger\gui
#cd documents\messenger\threading

