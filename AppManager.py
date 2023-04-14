import zmq
import signal
import sys
import threading
import time
from random import randint, random

__author__ = "Felipe Cruz <felipecruz@loogica.net>"
__license__ = "MIT/X11"

def tprint(msg):
    """like print, but won't get newlines confused with multiple threads"""
    sys.stdout.write(msg + '\n')
    sys.stdout.flush()

class ServerTask(threading.Thread):
    """ServerTask"""
    def __init__(self):
        threading.Thread.__init__ (self)

    def run(self):
        context = zmq.Context()
        frontend = context.socket(zmq.ROUTER)
        frontend.bind('tcp://*:5570')

        backend = context.socket(zmq.DEALER)
        backend.bind('inproc://backend')

        workers = []
        for i in range(5):
            worker = ServerWorker(context)
            worker.start()
            workers.append(worker)

        zmq.proxy(frontend, backend)

        frontend.close()
        backend.close()
        context.term()

class ServerWorker(threading.Thread):
    """ServerWorker"""
    def __init__(self, context):
        threading.Thread.__init__ (self)
        self.context = context

    def run(self):
        worker = self.context.socket(zmq.DEALER)
        worker.connect('inproc://backend')
        tprint('Worker started')

        while True:
            try:
                ident, msg  = worker.recv_multipart()
                time.sleep(1)
                print("Sending message...")
                self.receiveMessage(ident, msg)

                worker.send_multipart([ident, msg])
                worker.send(msg)
                # worker.send(b"HEHEHEEHEE GOT YOU :-)")
            except KeyboardInterrupt:
                print("Quiting application...")
            except e:
                print(e)
                # worker.send_multipart(msg)
                # worker.send(msg)


        worker.close()

    def receiveMessage(self, ident, msg):
        tprint('%s: %s' % (ident, msg))

    def sendMessage(self, identity, mess):
        while True:
            clientName = input("Client Name or ID to reply to: ")
            time.sleep(5)


def main():
    """main function"""
    server = ServerTask()
    server.start()
    server.join()


if __name__ == "__main__":
    main()



#
#   Reading from multiple sockets
#   This version uses zmq.Poller()
#
#   Author: Jeremy Avnet (brainsik) <spork(dash)zmq(at)theory(dot)org>
#

# import zmq

# # Prepare our context and sockets
# context = zmq.Context()

# # Connect to task ventilator
# receiver = context.socket(zmq.PULL)
# receiver.connect("tcp://localhost:5557")

# # Connect to weather server
# subscriber = context.socket(zmq.SUB)
# subscriber.connect("tcp://localhost:5556")
# subscriber.setsockopt(zmq.SUBSCRIBE, b"10001")

# # Initialize poll set
# poller = zmq.Poller()
# poller.register(receiver, zmq.POLLIN)
# poller.register(subscriber, zmq.POLLIN)

# # Process messages from both sockets
# while True:
#     try:
#         socks = dict(poller.poll())
#     except KeyboardInterrupt:
#         break

#     if receiver in socks:
#         message = receiver.recv()
#         # process task

#     if subscriber in socks:
#         message = subscriber.recv()
#         # process weather update
