import socket
import random
import sys
import time

class Server:
    def __init__(self, server_address,mode):
        # Set up the UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Save the server address
        self.server_address = server_address
        self.sock.bind(server_address)
        self.receive_address = None
       
        # Select the mode
        self.mode = mode
        # Set the ACK, SEQ and Length
        self.length = 10
        self.ack = 10
        self.seq = 0
        
        # Set the receive ACK, SEQ and Length
        self.rcv_ack_num = 0
        self.rcv_seq_num = 0 
        self.rcv_packet_len = 0

        # Set the wrong SEQ and ACK
        self.wrong_seq = 0
        self.wrong_ack = 0

        # Round
        self.round = 1
        
        # Heath Point
        self.ClientHealth = 2

    def create_manuel_message(self):

            # Get the input from the user as a string
            print(f'--------------- Server Input --------------------')
            input_string = input("Enter the ACK, SEQ, and length values: ")

            # Split the input string on the comma delimiter to get the individual values
            seq, ack, length = input_string.split(',')

            # Convert the values to the desired data type
            self.seq = int(seq)
            self.ack = int(ack)
            self.length = int(length)
            message = f"{seq},{ack},{length}"
            return self.send_message(message)
            

    # rcv = receive
    def create_auto_message(self):
        
        # Create 1/5 random probability
        prob = random.randint(1,5)
        
        if prob == 5:
            self.wrong_seq = random.randint(1,100)
            self.wrong_ack = random.randint(self.wrong_seq,100)
            message = f"{self.wrong_seq},{self.wrong_ack},{self.length}"
            return self.send_message(message)

        # calculate message
        else:
            self.seq = int(self.rcv_ack_num)
            self.ack = int(self.rcv_seq_num) + int(self.rcv_packet_len)
            message =  f"{self.seq},{self.ack},{self.length}"
            return self.send_message(message)
    
    # Send Message
    def send_message(self,message):
        seq, ack, length = message.split(',')
        print(f'---------------Round -> {self.round}--------------------')
        print("Client Health <3 -> ", self.ClientHealth)
        print(f"Server ->  SEQ: {seq} ACK: {ack} LEN: {length}")
        print('----------------------------------------')
        # Encode message
        message = message.encode()
        time.sleep(1)
        # Send a message to receive address
        self.sock.sendto(message, self.receive_address)
        # Update round
        self.round+=1
        return self.receive_message(message)

    
    # Wait Receive Message
    def receive_message(self,message):
        self.sock.settimeout(10) #10 seconds
        while True:
            try:
                # Wait Receive Message
                data, self.receive_address = self.sock.recvfrom(5000)
                data = data.decode()
            
            # If a timeout occurs, retransmit the message
            except socket.timeout:
                
                # if a timeout occurs, mode is Auto
                if self.mode == "AU":
                    self.sock.settimeout(10) #10 seconds
                    print("Client Message is time out ! ")
                    self.receive_message(message)
                
                # if a timeout occurs, mode is Manual
                else:
                    # if timeout occurs, first round
                    if self.round == 1:
                        print("Client Message is time out !")
                        return self.receive_message(message)
                    # if timeout occurs, other rounds
                    else:
                        self.sock.settimeout(10) #10 seconds
                        print("Client Message is time out !")
                        self.receive_message(message)
            # Set receive args
            self.rcv_seq_num, self.rcv_ack_num, self.rcv_packet_len = data.split(',')
            print(f"Client ->  SEQ: {self.rcv_seq_num} ACK: {self.rcv_ack_num} LEN: {self.rcv_packet_len}")
            return self.calculate_message()

    def close(self):
        # Close the socket when the client is no longer needed
        self.sock.close()

    def calculate_message(self):
        # if ServerHealth is 0
        if self.ClientHealth == 0:
            print("Server WON !!")
            self.close()
            sys.exit()

        # Manual Mode
        if self.mode == "MN":
            
            # First Round
            if self.round == 1:
                return self.create_manuel_message()

            # Receive message is not correct 
            if int(self.ack) != int(self.rcv_seq_num) or (int(self.seq) + int(self.length)) != int(self.rcv_ack_num):
                self.ClientHealth-=1
                print("Client message is corrupted !")
                return self.create_manuel_message()
            # Receive message is correct
            else:
                return self.create_manuel_message()

        # Auto Mode
        elif self.mode == "AU":
            
            # First Round
            if self.round == 1:
                return self.create_auto_message()
            
            # Receive message is not correct
            if int(self.ack) != int(self.rcv_seq_num) or (int(self.seq) + int(self.length)) != int(self.rcv_ack_num):
                # Set ServerHealth
                self.ClientHealth-=1
                message = f"{self.seq},{self.ack},{self.length}"
                print("Client message is corrupted !")
                self.send_message(message)
            
            # Receive message is correct
            else:
                return self.create_auto_message()
            
def runServer():
    mode = input("Enter the Auto(AU) or Manual(MN) modes ")
   # Create a Server and connect to the server at localhost:12345
    server = Server(('localhost', 12345),mode)
    #server.mode_message()
    message = f"{server.seq},{server.ack},{server.length}"
    while(1):
        if server.mode == "MN":
            server.receive_message(message)

        elif server.mode == "AU":
            server.receive_message(message)
            
        else:
            sys.exit()

runServer()


        

