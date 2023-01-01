import socket
import random
import sys
import time
class Server:
    def __init__(self, server_address):
        # Set up the UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.server_address = server_address

        self.sock.bind(server_address)

        self.receive_address = None
        
        self.mode = None
        self.order = 1

        self.seq = 0
        self.ack = 0
        self.length = 0
        
    def start(self):
        # Set the timeout for the socket"
        
        if self.mode == None:
            data, receive_address = self.sock.recvfrom(5000)
            data = data.decode()
            self.receive_address = receive_address
            self.mode = data
            print("Server Mode: ", self.mode)
            return self.start()
        
    
        self.sock.settimeout(30)
        
        message = f"{self.seq},{self.ack},{self.length}"
        # Send the message to the server
        message = message.encode()

        while True:

            try:
                # Wait for a message from the client
                data, self.receive_address = self.sock.recvfrom(5000)
                data = data.decode()
            except socket.timeout:
                # If a timeout occurs, retransmit the last message
                self.sock.sendto(message, self.receive_address)
                continue

            # Split the message from the server
            seq_num_C, ack_num_C, packet_len_C = data.split(',')
            self.next_message(seq_num_C, ack_num_C, packet_len_C)
            return self.start()
        
    def next_message(self,seq_num_C, ack_num_C, packet_len_C):

        if self.mode == "MN":
            input_string = input("Enter the SEQ, ACK, and Length values: ")
            self.seq, self.ack, self.length = input_string.split(',')
            print(f"Server -> {self.order} SEQ: {self.seq} ACK: {self.ack} LEN: {self.length}")
            self.order+=1
            print('----------------------------------------')
            message = f"{self.seq},{self.ack},{self.length}"
            # Send the message to the server
            message = message.encode()   
            self.sock.sendto(message, self.receive_address)

        if self.mode == "AU":
            seq_S = int(ack_num_C)
            ack_S = int(seq_num_C) + int(packet_len_C) + 1
            len_S = random.randint(ack_S-seq_S, 100) 
            self.seq, self.ack, self.length = seq_S, ack_S, len_S
            print(f"Server -> {self.order} SEQ: {self.seq} ACK: {self.ack} LEN: {self.length}")
            self.order+=1
            print('----------------------------------------')
            message = f"{self.seq},{self.ack},{self.length}"
            # Send the message to the server
            message = message.encode()   
            self.sock.sendto(message, self.receive_address)
            time.sleep(2)

    def close(self):
        # Close the socket when the client is no longer needed
        self.sock.close()


def runServer():
    # Create a client and connect to the server at localhost:12345
    server = Server(('localhost', 12345))
    #Start the game
    server.start()
    # Close the client
    server.close()
