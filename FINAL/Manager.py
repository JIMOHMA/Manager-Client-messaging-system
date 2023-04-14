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
server = context.socket(zmq.ROUTER)
server.bind('tcp://*:9999')


# senderSocket = context.socket(zmq.PUB)
# senderSocket.bind('tcp://*:8888')

# sending message function
def sending_messages(server):
  while True:
    message = input()
    server.send_string(u'%s' % (message))
    # server.send_multipart([u'%s' % (message)])
    print("You: " + message)

# receiving message function
def receiving_messages(server):
  while True:
    print("Client: " + server.recv().decode('utf-8'))


# threads to start both receving and sending functions
threading.Thread(target=receiving_messages, args=(server,)).start()
threading.Thread(target=sending_messages, args=(server,)).start()