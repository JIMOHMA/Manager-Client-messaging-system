import zmq
import sys, time, threading


# Inheriting from the thread class 
# Multithreading to be used for receiving and sending of messages
class ClientApp(threading.Thread):

  def __init__(self):
    # Simple Dealer Socket
    self.context  = zmq.Context()
    self.client   = self.context.socket(zmq.DEALER)
    self.client.connect('tcp://localhost:9999')

    # The ID could be anything; a number or alphabet or alphanumeric. 
    # It's only being used to distinguish on the App Manager side which 
    # client sent an information to it
    self.clientID         = input("Enter your ID or userName: ")
    print("You can start sending messages...\n")
    self.identity         = u'%s' % self.clientID
    self.client.identity  = self.identity.encode('ascii')

    self.client_sub_Socket = self.context.socket(zmq.SUB)
    self.client_sub_Socket.connect('tcp://127.0.0.1:8888')
    # client_sub_Socket.setsockopt(zmq.SUBSCRIBE, b'')
    self.client_sub_Socket.setsockopt_string(zmq.SUBSCRIBE, '')
  def run(self) -> None:
    try:
      # threads to start both receving and sending messages
      # since we're using the command line for input from the user, using two threads
      # to simulate this interaction between the AppManager and Client {N} was required.
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
      # Close the client socket
      self.exit()

  def exit(self) -> None:
      """Close the socket"""
      self.server.close()
      self.server_pub_Socket.close()
      self.context.term()

  # sending message function
  def sending_messages(self) -> None:
    
    while True:
      try:
        message   = input()
        list_Msg  = [bytes(self.clientID, 'utf-8'), bytes(message, 'utf-8')]
        self.client.send_multipart(list_Msg)
        # client.send_string(u'%s' % (message)) # Implementation for the DEALER on the server side
        # client.send_multipart([u'%s' % (message)]) # Implementation for a ROUTER on the server side
        print("You: " + message)
      except:
        print("W: Interrupt received, terminating all connections...")
        time.sleep(3)
        break
    self.context.term()


  # receiving message function
  def receiving_messages(self) -> None:
    while True:
      try:
        string_Msg = [msg.decode('utf-8') for msg in self.client_sub_Socket.recv_multipart()]

        if len(string_Msg) == 1:
          print(f'AppManager: {string_Msg[0]}') # this 
        elif len(string_Msg) == 0:
          pass
        else:
          print(x for x in string_Msg)
          # print(f'AppManager: {x}' for x in string_Msg) # if multiple messages were sent by the AppManager to the client
        # print("%s: %s" % ("AppManager", client_sub_Socket.recv_multipart()))
      except:
        print("W: interrupt received, STOPPING...")
        break
    # self.context.term()

if __name__ == '__main__':
    #Create and start the Client Application
    ClientApp = ClientApp()
    ClientApp.run()
