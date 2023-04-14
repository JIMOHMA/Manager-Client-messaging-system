import zmq
import signal
import sys
import threading
import time
from random import randint, random

# Inheriting from the thread class 
# Multithreading to be used for receiving and sending of messages
class AppManager(threading.Thread):

  def __init__(self):
    threading.Thread.__init__ (self)
    
    # Simple DEALER Socket for receiving asynchronous messages
    self.context = zmq.Context()
    self.server = self.context.socket(zmq.DEALER)  
    # server = context.socket(zmq.ROUTER)  # if unique messaging is required between clients and  the App Manager
    self.server.bind('tcp://*:9999')

    # Simple PUB Socket for broadcasting messages to every clientApp {N} connected
    self.server_pub_Socket = self.context.socket(zmq.PUB)
    self.server_pub_Socket.bind('tcp://*:8888')

  def run(self):
    try:
      # threads to start both receving and sending messages
      # since we're using the command line for input from the user, using two threads
      # to simulate this interaction between the AppManager and Client {N}. 
      # A sending action is not prevented by a receiving action
      t1 = threading.Thread(target=self.receiving_messages, args=())
      t2 = threading.Thread(target=self.sending_messages, args=())

      t1.daemon = True # die when the main thread dies
      t2.daemon = True
      t1.start()
      t2.start()

      t1.join()
      t2.join()
      
    except Exception as e:
      print(e, " this is the error")
      # Close the server socket
      self.exit()

  def exit(self):
      """Close the socket"""
      self.server.close()
      self.server_pub_Socket.close()
      self.context.term()

    # poll = zmq.Poller()
    # poll.register(server, zmq.POLLIN)
    # poll.register(server_pub_Socket, zmq.POLLIN)

  # sending message function
  def sending_messages(self):
    while True:
      try:
        message = input()
        list_Msg = [bytes(message, 'utf-8')]
        self.server_pub_Socket.send_multipart(list_Msg)
        # server_pub_Socket.send_string(u'%s' % (message))
        print("You: " + message)

      except:
        print("W: interrupt received, stopping...")
        time.sleep(3)  # do some work...
        break
    self.context.term() # terminating here so the receiving connection also terminates 
                        # thus causing the except block to get triggered for the receiving_messages function


  # receiving message function
  def receiving_messages(self):
    while True:
      try:
        client_Information = [msg.decode('utf-8') for msg in self.server.recv_multipart()]
        client_ID           = client_Information[0]
        client_Msg          = client_Information[1]
        print(f"{client_ID}: {client_Msg}")
      except Exception as e:
        print("Terminating receiving connection...") # this gets triggered when the context is terminated
        break

if __name__ == '__main__':
    #Create and start the AppManager
    AppManager = AppManager()
    AppManager.run()

