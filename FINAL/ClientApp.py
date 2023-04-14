import zmq
import sys
import threading


# ?????????????????????????????????????????????????????????????????????????????
# ?????????????????????????????????????????????????????????????????????????????

# def tprint(msg):
#     """like print, but won't get newlines confused with multiple threads"""
#     sys.stdout.write(msg + '\n')
#     sys.stdout.flush()

# class ClientTask(threading.Thread):
#     """ClientTask"""
#     def __init__(self, clientName):
#         self.clientName = clientName
#         threading.Thread.__init__ (self)

#     def run(self):
#         context = zmq.Context()
#         socket = context.socket(zmq.DEALER)
#         identity = u'%s' % self.clientName
#         socket.identity = identity.encode('ascii')
#         socket.connect('tcp://localhost:6670')
#         print('Client-%s started' % (identity))
#         poll = zmq.Poller()
#         poll.register(socket, zmq.POLLIN)
#         # reqs = 0  ## this will be an input from the user
#         while True:
#             # reqs = reqs + 1
#             clientMsg = input("Enter your message here: ")
#             print('{ %s } has been sent..' % (clientMsg))
#             socket.send_string(u'%s' % (clientMsg))
#             for i in range(5):
#                 sockets = dict(poll.poll(1000))
#                 if socket in sockets:
#                     msg = socket.recv()
#                     tprint('%s: %s' % ("AppManager:", msg))

#         socket.close()
#         context.term()

# def main():

#     clientName = input("Please enter the client's name or ID: ")
#     client = ClientTask(clientName)
#     client.start()
    
# if __name__ == "__main__":
#     main()


# ?????????????????????????????????????????????????????????????????????????????
# ?????????????????????????????????????????????????????????????????????????????


# Simple Dealer Socket
context = zmq.Context()
client = context.socket(zmq.DEALER)
client.connect('tcp://localhost:9999')

# The ID could be anything; a number or alphabet or alphanumeris. 
# It's only being used to distinguish on the App Manager side which 
# client sent an information
clientID = input("Enter the your ID or userName: ")
identity = u'%s' % clientID
print("identity is: ", type(identity), identity)
client.identity = identity.encode('ascii')

client_sub_Socket = context.socket(zmq.SUB)
client_sub_Socket.connect('tcp://127.0.0.1:8888')
# client_sub_Socket.setsockopt(zmq.SUBSCRIBE, b'')
client_sub_Socket.setsockopt_string(zmq.SUBSCRIBE, '')

# sending message function
def sending_messages(client, clientID):
  while True:
    message = input()

    list_Msg = [bytes(clientID, 'utf-8'), bytes(message, 'utf-8')]
    client.send_multipart(list_Msg)
    # client.send_string(u'%s' % (message)) # Implementation for the DEALER on the server side
    # client.send_multipart([u'%s' % (message)]) # Implementation for a ROUTER on the server side
    print("You: " + message)

# receiving message function
def receiving_messages(client, client_sub_Socket):
  while True:
    string_Msg = [msg.decode('utf-8') for msg in client_sub_Socket.recv_multipart()]
    
    # I
    if len(string_Msg) == 1:
      print(f'AppManager: {string_Msg[0]}')
    elif len(string_Msg) == 0:
      pass
    else:
      print(x for x in string_Msg)
    # print("%s: %s" % ("AppManager", client_sub_Socket.recv_multipart()))


# threads to start both receving and sending functions
threading.Thread(target=receiving_messages, args=(client, client_sub_Socket,)).start()
threading.Thread(target=sending_messages, args=(client, clientID,)).start()


# TODO: Handle ctrl-C 

# TODO: Create a pretty-print function for handling bytes and strings dynamically