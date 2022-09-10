
######################################
# Name : Abdulaziz Alamri
# Student ID : s201842560
# SHA256 : acda20201a05e2bd6ac1a66f743eb861a49b30d9f7c51890fc21fcf4cf5dfa84
######################################

# Imported Libraries

import base64
import socket
import time
from Crypto.Random import get_random_bytes										# Library for generating a CSRNG IV
from Crypto.Cipher import AES			
from Crypto.Util.Padding import pad,unpad


#	Connection initialization

print("Searching for Server...")

try:
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)            # initialize Socket for the connection
    s.connect(('192.168.8.163',9000))								    # Specify IP of the server for the client to connect to  

    keyHEX= "acda20201a05e2bd6ac1a66f743eb861a49b30d9f7c51890fc21fcf4cf5dfa84"
    key = bytearray.fromhex(keyHEX)                                             # change the key to bytes
    print("key == ",key)

    InitialIV = get_random_bytes(16)                                            # Generate Random number
    initialIVENCODED = base64.b64encode(InitialIV)                              # Encode IV to base 64 to send it                  
    print("Initial IV : ",initialIVENCODED)
    s.send(initialIVENCODED)

##################################################################################################################

    def AEScipherENC(key,PlainText,IVrecievedDECODED):                          # AES encrypton Function
        dataTOENC = str.encode(PlainText)                                       # Encode the plaintext
        cipher = AES.new(key, AES.MODE_CBC, IVrecievedDECODED)                  # Create new AES cipher object
        CipherText = cipher.encrypt(pad(dataTOENC,AES.block_size))              # Generate the ciphertext from the plaintext
        print("[+] Plain Text (Before) ==> ",PlainText) 
        print("[+] Cipher Text (After) ==> ",base64.b64encode(CipherText))                                     # Print the corrosponding Plaintext
        return CipherText											            # Return the Cipher Text

    
    def AEScipherDECr(key,CT,IVGenerated):                                      # AES decryption Function
        cipher = AES.new(key, AES.MODE_CBC, IVGenerated)                        # Create new AES cipher object
        PlainText = (unpad(cipher.decrypt(CT),AES.block_size)).decode("utf-8")  # Get the plaintext from the ciphertext
        print("[+] Cipher Text (Before) ==> ",base64.b64encode(CT))   
        print("[+] Plain Text (After) ==> ",PlainText)   
        return PlainText		
        
##################################################################################################################
    def GameChoice(IVinitial):                                               # Game Choice Function
        GameChoose=s.recv(10000)                        # Recieve menu of games from the Server
        print("\nServer : ",AEScipherDECr(key,GameChoose,IVinitial))

        UserChoice = input("Your Choice : ")                        
        s.send(AEScipherENC(key,UserChoice,IVinitial))  ##4                            # Send Choice of game to the Server

        if int(UserChoice) == 2:                                    # Client chose to Terminate
            print("Closing Session...")                             # Closing session warning
            time.sleep(2)                                           # this is Line used to create some reality in the game. the game will wait 2 seconds then both the game and conection will closed
            s.close()                                               # Close Connection
            exit()                                                  # Close Client.py


        GameName=s.recv(10000)                           # Recieve Name of the Game from the Server
        print("\nServer : ",AEScipherDECr(key,GameName,IVinitial))

        IVGenerated=(get_random_bytes(16))
        IVGeneratedENCODED=base64.b64encode(IVGenerated)                         # Generate IV with length 16 bytes (128 bits)
        s.send(IVGeneratedENCODED)

        running = 1                                                # Set condition for the While Loop.
        
        while running:
            HowToPlay=s.recv(10000)                    # Recieve instructions of the game from the Server
            print(AEScipherDECr(key,HowToPlay,IVGenerated))

            guess = input("My Guess: ")                             # Send Client's Guess to the server
        
            s.send(AEScipherENC(key,guess,IVGenerated))  ##6

            response = s.recv(10000)                       # Recieve response that indicates whether the guess was correct ot not
            responseDecoded = AEScipherDECr(key,response,IVGenerated)
            print("Server : ",responseDecoded)

            if "Correct!" in responseDecoded:                              # If the Guess is correct then the Server will return to the Main Menu.
                GameChoice(IVGenerated)                                        # Return to the start of the function

    s.send(AEScipherENC(key,"Hello",InitialIV))                                        # Send Hello to the Server

    greetings=s.recv(10000)                                # Recieve Greetings from the Server
    print("Server : ",AEScipherDECr(key,greetings,InitialIV))                                    # Print message from the Server

    GameChoice(InitialIV)                                                    # start function for the first time 

except ConnectionRefusedError:                                      # Exception incase the Client couldn't connect to the Server
    print ("Cannot Connect to the Server\nTerminating...")          # state that the client couldn't connect to the server

