import zmq
import signal
import sys
import threading
import time
from random import randint, random

# ?????????????????????????????????????????????????????????????????????????????
# ?????????????????????????????????????????????????????????????????????????????

# __author__ = "Felipe Cruz <felipecruz@loogica.net>"
# __license__ = "MIT/X11"

# def tprint(msg):
#     """like print, but won't get newlines confused with multiple threads"""
#     sys.stdout.write(msg + '\n')
#     sys.stdout.flush()

# class ServerTask(threading.Thread):
#     """ServerTask"""
#     def __init__(self):
#         threading.Thread.__init__ (self)

#     def run(self):
#         context = zmq.Context()
#         frontend = context.socket(zmq.ROUTER)
#         # frontend = context.socket(zmq.DEALER)
#         frontend.bind('tcp://*:6670')

#         backend = context.socket(zmq.DEALER)
#         backend.bind('inproc://BACKEND')

#         workers = []
#         for i in range(5):
#             worker = ServerWorker(context)
#             worker.start()
#             workers.append(worker)

#         zmq.proxy(frontend, backend)

#         frontend.close()
#         backend.close()
#         context.term()

# class ServerWorker(threading.Thread):
#     """ServerWorker"""
#     def __init__(self, context):
#         threading.Thread.__init__ (self)
#         self.context = context

#     def run(self):
#         worker = self.context.socket(zmq.DEALER)
#         worker.connect('inproc://BACKEND')
#         tprint('Worker started')

#         while True:
#             # try:
#             ident, msg  = worker.recv_multipart()
#             time.sleep(1)
#             print("Sending message...")
#             self.receiveMessage(ident, msg)
#             myreply = bytes("HEHEHEHE GOT YOU", 'utf-8')
#             worker.send_multipart(myreply)
#             worker.send(myreply)
#                 # worker.send(b"HEHEHEEHEE GOT YOU :-)")
#             # except KeyboardInterrupt:
#             #     print("Quiting application...")
#             # except Exception as e:
#             #     print(e)
#                 # worker.send_multipart(msg)
#                 # worker.send(msg)


#         worker.close()

#     def receiveMessage(self, ident, msg):
#         tprint('%s: %s' % (ident, msg))

#     def sendMessage(self, identity, mess):
#         while True:
#             clientName = input("Client Name or ID to reply to: ")
#             time.sleep(5)


# def main():
#     """main function"""
#     server = ServerTask()
#     server.start()
#     server.join()


# if __name__ == "__main__":
#     main()


# ?????????????????????????????????????????????????????????????????????????????
# ?????????????????????????????????????????????????????????????????????????????


# Simple Router Socket
context = zmq.Context()
server = context.socket(zmq.DEALER)  
# server = context.socket(zmq.ROUTER)  # Use this if you need to ID the clients to connecting to the App Manager
server.bind('tcp://*:9999')

# poller = zmq.Poller()
# poller.register(server, zmq.POLLIN)


server_pub_Socket = zmq.Context().socket(zmq.PUB)
server_pub_Socket.bind('tcp://*:8888')


def tprint(msg):
    """like print, but won't get newlines confused with multiple threads"""
    sys.stdout.write(msg + '\n')
    sys.stdout.flush()


# sending message function
def sending_messages(server, server_pub_Socket):
  while True:
    message = input()
    # server.send_string(u'%s' % (message))
    # server.send_multipart([u'%s' % (message)])
    list_Msg = [bytes(message, 'utf-8')]
    server_pub_Socket.send_multipart(list_Msg)
    # server_pub_Socket.send_string(u'%s' % (message))
    print("You: " + message)

# receiving message function
def receiving_messages(server):
  while True:
    client_Information = [msg.decode('utf-8') for msg in server.recv_multipart()]
    client_ID           = client_Information[0]
    client_Msg          = client_Information[1]
    print(f"{client_ID}: {client_Msg}")


# threads to start both receving and sending functions
threading.Thread(target=receiving_messages, args=(server, )).start()
threading.Thread(target=sending_messages, args=(server, server_pub_Socket)).start()


# TODO: Handle ctrl-C 