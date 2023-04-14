import zmq
import sys
import threading

# Simple Dealer Socket
context = zmq.Context()
client = context.socket(zmq.DEALER)
client.connect('tcp://localhost:9999')

# The ID could be anything; a number or alphabet or alphanumeris. 
# It's only being used to distinguish on the App Manager side which 
# client sent an information
clientID = input("Enter the your ID or userName: ")
identity = u'%s' % clientID
client.identity = identity.encode('ascii')

client_sub_Socket = context.socket(zmq.SUB)
client_sub_Socket.connect('tcp://127.0.0.1:8888')
# client_sub_Socket.setsockopt(zmq.SUBSCRIBE, b'')
client_sub_Socket.setsockopt_string(zmq.SUBSCRIBE, '')

# sending message function
def sending_messages(client, clientID):
  try:
    while True:
      message = input()

      list_Msg = [bytes(clientID, 'utf-8'), bytes(message, 'utf-8')]
      client.send_multipart(list_Msg)
      # client.send_string(u'%s' % (message)) # Implementation for the DEALER on the server side
      # client.send_multipart([u'%s' % (message)]) # Implementation for a ROUTER on the server side
      print("You: " + message)
  except:
    print("W: interrupt received, stopping...")
  return


# receiving message function
def receiving_messages(client, client_sub_Socket):
  while True:
    try:
      string_Msg = [msg.decode('utf-8') for msg in client_sub_Socket.recv_multipart()]
      # I
      if len(string_Msg) == 1:
        print(f'AppManager: {string_Msg[0]}')
      elif len(string_Msg) == 0:
        pass
      else:
        print(x for x in string_Msg)
      # print("%s: %s" % ("AppManager", client_sub_Socket.recv_multipart()))
    except:
      print("W: interrupt received, STOPPING...")
  return

# threads to start both receving and sending messages
# since we're using the command line for input from the user, using two threads
# to simulate this interaction between the AppManager and Client {N} was required.
# A sending action is not prevented by a receiving action
t1 = threading.Thread(target=receiving_messages, args=(client, client_sub_Socket,))
t1.start()
t2 = threading.Thread(target=sending_messages, args=(client, clientID,))
t2.start()

# TODO: Create a pretty-print function for handling bytes and strings dynamically
