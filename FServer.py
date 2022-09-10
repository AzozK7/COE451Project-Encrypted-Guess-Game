
######################################
# Name : Abdulaziz Alamri
# Student ID : s201842560
# SHA256 : acda20201a05e2bd6ac1a66f743eb861a49b30d9f7c51890fc21fcf4cf5dfa84
######################################

# Imported Libraries

import base64
import random
import socket
import time
from Cryptodome.Cipher import AES								# Module for AES Encryption and Decryption	
from Cryptodome.Util.Padding import pad,unpad

#	Connection initialization

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)			# initialize Socket for the connection
s.bind(("192.168.8.163",9000))										# Bind ip and port for the server to use
s.listen(5)

print ("Waiting for client ...")								# waiting for the client to connect to the server

(c,a) = s.accept()												# when a client tries to connect, His/Her IP address and Port will be printed in the server terminal
print ("Received connection from", a)						

# Functions
##################################################################################################################

def AEScipherENC(key,PlainText,IVrecievedDECODED):							# AES encrypton Function
	dataTOENC = str.encode(PlainText)										# Encode the plaintext
	cipher = AES.new(key, AES.MODE_CBC, IVrecievedDECODED)					# Create new AES cipher object
	CipherText = cipher.encrypt(pad(dataTOENC,AES.block_size))				# Generate the ciphertext from the plaintext
	print("[+] Plain Text (Before) ==> ",PlainText) 
	print("[+] Cipher Text (After) ==> ",base64.b64encode(CipherText)) 							# Print the corrosponding Ciphertext
	return CipherText														# Return the Cipher Text

def AEScipherDECr(key,CT,IVrecievedDECODED):								# AES decryption Function
	cipher = AES.new(key, AES.MODE_CBC, IVrecievedDECODED)					# Create new AES cipher object
	PlainText = (unpad(cipher.decrypt(CT),AES.block_size)).decode("utf-8")	# Get the plaintext from the ciphertext
	print("[+] Cipher Text (Before) ==> ",base64.b64encode(CT))   
	print("[+] Plain Text (After) ==> ",PlainText)   											# Print the corrosponding Plaintext
	return PlainText			

##################################################################################################################

def Play(IVrecievedDECODED):														# The Play function will be launched when the client chooses to play
	
	random_number = random.randint(1, 100)						# A number choosen randomly 

	print("Random Number is", random_number)					# Print the number in the server terminal
	running = 1													# Set variable "running" to 1 to use in a loop
	while running:												# This Loop is active when the client is playing

		c.send(AEScipherENC(key,"Choose a number between 1 and 100",IVrecievedDECODED))	# Send instructions to the client

		guess=c.recv(10000)	  						# Recieve guess from the client
		guessDecoded = AEScipherDECr(key,guess,IVrecievedDECODED)
		guessNUM=int(guessDecoded)

		print("Client == ",guessDecoded)								# convert the recieved string into an integer and then print it in the server terminal 

		if guessNUM < random_number:							
			c.send(AEScipherENC(key,"Go Higher!",IVrecievedDECODED))						# If the cleint guessed lower than the random number, then message "Go Higher!" will be sent

		if guessNUM > random_number:
			c.send(AEScipherENC(key,"Go Lower!",IVrecievedDECODED))	   					# If the cleint guessed higher than the random number, then message "Go Lower!" will be sent

		if guessNUM == random_number:
			print("User Guessed the Random Number!")
			c.send(AEScipherENC(key,"\n*** Correct! ***\nHeading Back to the Main Menu...",IVrecievedDECODED))	

			AskUser(IVrecievedDECODED)											# If the cleint guessed the random number correctly, then a message will be sent to the client and game will get back to the main menu											

def AskUser(IVinitial):
	c.send(AEScipherENC(key,"""Enter Your Choice :\n###########################\n1. Play the Guess Game! \n2. Exit.\n###########################\n """,IVinitial)) 

	UserChoice = c.recv(10000)  						# Recieve the clients choice of game
	UserChoiceDECODED = AEScipherDECr(key,UserChoice,IVinitial)
	print("Client : ",UserChoiceDECODED)

	UserChoiceNUM = int(UserChoiceDECODED)								# conver the recieved the client choice from string to integer

	if UserChoiceNUM == 1:
		print("User Choose to Play!")
		c.send(AEScipherENC(key,"You Chose to Play the Guess Game!",IVinitial))		# If the client chose to play, then the game will start and gets directed to the "Play" Function
		
		IVrecievedENCODED=c.recv(10000).decode()
		IVrecievedDECODED=base64.b64decode(IVrecievedENCODED)

		print("\nNew IV == ",IVrecievedENCODED)
		Play(IVrecievedDECODED)

	elif UserChoiceNUM == 2:
		print("User Choose to Exit!\nTerminating session...")	# If the client chose to Exit, then the game will be terminated and the connection will be closed

		time.sleep(2)											# this is Line used to create some reality in the game. the game will wait 2 seconds then both the game and conection will closed
		c.close()												# Close the connection
		exit()													# Close the Program

	else:
		c.send(AEScipherENC(key,"Wrong Choice! Please Try Again",IVinitial))		# If the user chose anything other the two choices, then a warning message will be sent
		AskUser(IVinitial)												# Return to the main menu after a wrong choice

	AskUser(IVinitialDECODED)													# Return to the main menu after a round ended


keyHEX= "acda20201a05e2bd6ac1a66f743eb861a49b30d9f7c51890fc21fcf4cf5dfa84"
key = bytearray.fromhex(keyHEX)
print("key == ",key)

IVinitial =c.recv(10000).decode()
print("Initial IV : ",IVinitial)
IVinitialDECODED=base64.b64decode(IVinitial)

hello=c.recv(10000) 									# Recieve Message #1 from the client
print(AEScipherDECr(key,hello,IVinitialDECODED))										# Print client's Message

c.send(AEScipherENC(key,"Greetings!",IVinitialDECODED))									# Send "Greetings!" Message to the client

AskUser(IVinitialDECODED)