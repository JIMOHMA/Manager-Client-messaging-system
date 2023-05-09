'''
import zmq
import sys, threading, time
import argparse

# Inheriting from the thread class 
# Multithreading to be used for receiving and sending of messages
class AppManager(threading.Thread):

  def __init__(self, dealer_port: int, pub_port: int) -> None:
    threading.Thread.__init__ (self)
    try:

      # Simple DEALER Socket for receiving asynchronous messages
      self.context      = zmq.Context()
      self.server       = self.context.socket(zmq.DEALER)  
      self.dealer_port  = dealer_port
      # server = context.socket(zmq.ROUTER)  # if unique messaging is required between clients and  the App Manager
      self.server.bind(f'tcp://*:{self.dealer_port}')

      # Simple PUB Socket for broadcasting messages to every clientApp {N} connected
      self.server_pub_Socket  = self.context.socket(zmq.PUB)
      self.pub_port           = pub_port
      self.server_pub_Socket.bind(f'tcp://*:{self.pub_port}')
      print("You can start sending messages...\n")
    except:
      print(e, " this is the error")
      # Close the server socket
      self.exit()

  def run(self) -> None:
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

  def exit(self) -> None:
      """Close the socket"""
      self.server.close()
      self.server_pub_Socket.close()
      self.context.term()

    # poll = zmq.Poller()
    # poll.register(server, zmq.POLLIN)
    # poll.register(server_pub_Socket, zmq.POLLIN)

  # sending message function
  def sending_messages(self) -> None:
    while True:
      try:
        message   = input()
        list_Msg  = [bytes(message, 'utf-8')]
        self.server_pub_Socket.send_multipart(list_Msg)
        # server_pub_Socket.send_string(u'%s' % (message))
        print("You: " + message)

      except:
        print("W: Interrupt received, terminating all connections...")
        time.sleep(3)  # do some work...
        break
    self.context.term() # terminating here so the receiving connection also terminates 
                        # thus causing the except block to get triggered for the receiving_messages function


  # receiving message function
  def receiving_messages(self) -> None:
    while True:
      try:
        client_Information  = [msg.decode('utf-8') for msg in self.server.recv_multipart()]
        client_ID           = client_Information[0]
        client_Msg          = client_Information[1]
        print(f"{client_ID}: {client_Msg}")
      except Exception as e:
        print("Herehshshshs")
        break # this gets triggered when the context is terminated

if __name__ == '__main__':
    
    # Accepting arguments for port # for the DEALER and PUB sockets. 
    # If either of these port numbers are not provided, the application
    # defaults to [DEALER:9999] and [PUB:8888]
    parser = argparse.ArgumentParser()
    parser.add_argument('-p1', '--PORT1', type=int, default=9999, help="define the port# that's avaialable on your machine for the DEALER socket")
    parser.add_argument('-p2', '--PORT2', type=int, default=8888, help="define the port# that's avaialable on your machine for the PUB socket")

    # ports
    args = parser.parse_args()
    dealer_port = args.PORT1
    pub_port    = args.PORT2

    # Create and start the Application Manager
    AppManager = AppManager(dealer_port, pub_port)
    AppManager.run()
'''

import zmq
import sys, time
from .models import Message

class AppManager:

  # Default port # numbers if they are not specified by when an object of this AppManager class 
  # is created.
  def __init__(self, dealer_port: int = 9999, pub_port: int = 8888) -> None:
    try:
      # Simple DEALER Socket for receiving asynchronous messages
      self.context      = zmq.Context()
      self.server       = self.context.socket(zmq.DEALER)  
      self.dealer_port  = dealer_port
      # server = context.socket(zmq.ROUTER)  # if unique messaging is required between clients and  the App Manager
      self.server.bind(f'tcp://*:{self.dealer_port}')

      # Simple PUB Socket for broadcasting messages to every clientApp {N} connected
      self.server_pub_Socket  = self.context.socket(zmq.PUB)
      self.pub_port           = pub_port
      self.server_pub_Socket.bind(f'tcp://*:{self.pub_port}')
      print("You can start sending messages...\n")
    except:
      print(e, " this is the error")
      # Close the server socket
      self.exit()

  def exit(self) -> None:
      """Close the socket"""
      self.server.close()
      self.server_pub_Socket.close()
      self.context.term()

  # sending message function
  def sending_messages(self, messageObject: Message) -> None:
    while True:
      try:
        # No longer taking input from the user anymore, this will be 
        # received through some HTML page
        # message   = input()
        list_Msg  = [bytes(message, 'utf-8')]
        self.server_pub_Socket.send_multipart(list_Msg)
        # server_pub_Socket.send_string(u'%s' % (message))
        print("You: " + message)

      except:
        print("W: Interrupt received, terminating all connections...")
        time.sleep(3)  # do some work...
        break
    self.context.term() # terminating here so the receiving connection also terminates 
                        # thus causing the except block to get triggered for the receiving_messages function


  # receiving message function
  def receiving_messages(self) -> None:
    while True:
      try:
        client_Information  = [msg.decode('utf-8') for msg in self.server.recv_multipart()]
        client_ID           = client_Information[0]
        client_Msg          = client_Information[1]
        client_timeStamp    = client_Information[2]
        print(f"{client_ID}: {client_Msg}")
      except Exception as e:
        print("Herehshshshs")
        break # this gets triggered when the context is terminated

def main():
    
    # Accepting arguments for port # for the DEALER and PUB sockets. 
    # If either of these port numbers are not provided, the application
    # defaults to [DEALER:9999] and [PUB:8888]
    dealer_port: int = None # User can specify a port number for the dealer socket otherwise it defaults to port 9999
    pub_port: int    = None # User can specify a port number for the publisher socket otherwise it defaults to port 8888

    # Create and start the Application Manager
    AppManager = AppManager(dealer_port, pub_port)
    AppManager.run()

