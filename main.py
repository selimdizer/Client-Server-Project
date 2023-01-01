import threading
from Client import runClient
from Server import runServer

serverThread = threading.Thread(target=runServer)
ClientThread = threading.Thread(target=runClient)
serverThread.start()
ClientThread.start()
serverThread.join()
ClientThread.join()

