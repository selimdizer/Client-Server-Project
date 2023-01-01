import socket
import random
import sys
import time
class Client:
    def __init__(self, server_address,mode,ack,seq,length):
        # Set up the UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Save the server address
        self.server_address = server_address
        # Select the mode
        self.mode = mode
        # Set the ACK, SEQ and Length
        self.ack = ack
        self.seq = seq
        self.length = length
        self.order = 2

    def start(self):
        # Set the timeout for the socket
        self.sock.settimeout(30) #30 seconds
        # Create the message to send to the server
        message = f"{self.seq},{self.ack},{self.length}"
        # Send the message to the server
        message = message.encode()
        self.sock.sendto(message, self.server_address)
        
        # Wait for a response from the server
        while True:
            try:
                data, server_address = self.sock.recvfrom(5000)
                data = data.decode()
            except socket.timeout:
                # If a timeout occurs, retransmit the message
                self.sock.sendto(message, self.server_address)
                continue
            # Split the message from the server
            seq_num, ack_num, packet_len = data.split(',')
            self.next_message(seq_num, ack_num, packet_len)
            return self.start()
            

    def next_message(self,seq_num, ack_num, packet_len):
        if self.mode == "MN":
            input_string = input("Enter the SEQ, ACK, and Length values: ")
            self.seq, self.ack, self.length = input_string.split(',')
            print(f"Client -> {self.order} SEQ: {self.seq} ACK: {self.ack} LEN: {self.length}")
            self.order+=1
            print('----------------------------------------')
            
        
        if self.mode == "AU":
            seq_c = int(ack_num)
            ack_c = int(seq_num) + int(packet_len) + 1
            len_c = random.randint(ack_c-seq_c, 100)
            self.seq, self.ack, self.length = seq_c, ack_c, len_c
            print(f"Client -> {self.order} SEQ: {self.seq} ACK: {self.ack} LEN: {self.length}")
            self.order+=1
            print('----------------------------------------')
            time.sleep(2)
    

    def calculate_message(self,seq,ack,length):
        exp_seq = self.ack
        exp_ack = self.seq + self.length
        if seq != exp_seq or ack != exp_ack or self.length != length:
            self.error -=1
    
    def close(self):
        # Close the socket when the client is no longer needed
        self.sock.close()

def runClient():

    mode = input("Enter the Auto(AU) or Manuel(MN) for mode: ")
    print(f"{mode} mode is choosen.")
    print('----------------------------------------')
    if mode == "MN":
        input_string = input("Enter the SEQ, ACK, and Length values: ")
        seq, ack, length = input_string.split(',')
        print(f"Client -> {1} SEQ: {seq} ACK: {ack} LEN: {length}")
        print('----------------------------------------')

    elif mode == "AU":
        seq = random.randint(1, 100)
        ack = random.randint(seq, 100) 
        length = random.randint(ack-seq, 100)
        print(f"Client -> {1} SEQ: {seq} ACK: {ack} LEN: {length}")
        print('----------------------------------------')
    else:
        sys.exit()

    # Create a client and connect to the server at localhost:12345
    client = Client(('localhost', 12345),mode,ack,seq,length)
    message = mode
    # Send the message Mode to the server
    message = message.encode()
    client.sock.sendto(message, client.server_address)

    #Start the game
    client.start()

    # Close the client
    client.close()
