import zmq
import sys
import threading


def tprint(msg):
    """like print, but won't get newlines confused with multiple threads"""
    sys.stdout.write(msg + '\n')
    sys.stdout.flush()

class ClientTask(threading.Thread):
    """ClientTask"""
    def __init__(self, clientName):
        self.clientName = clientName
        threading.Thread.__init__ (self)

    def run(self):
        context = zmq.Context()
        socket = context.socket(zmq.DEALER)
        identity = u'%s' % self.clientName
        socket.identity = identity.encode('ascii')
        socket.connect('tcp://localhost:5570')
        print('Client-%s started' % (identity))
        poll = zmq.Poller()
        poll.register(socket, zmq.POLLIN)
        # reqs = 0  ## this will be an input from the user
        while True:
            # reqs = reqs + 1
            clientMsg = input("Enter your message here: ")
            print('{ %s } has been sent..' % (clientMsg))
            socket.send_string(u'%s' % (clientMsg))
            for i in range(5):
                sockets = dict(poll.poll(1000))
                if socket in sockets:
                    msg = socket.recv()
                    tprint('%s: %s' % ("AppManager", msg))

        socket.close()
        context.term()

def main():

    clientName = input("Please enter the client's name or ID: ")
    client = ClientTask(clientName)
    client.start()
    
if __name__ == "__main__":
    main()