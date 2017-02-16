# the code forks and creates 2 processes which run as sender and listener (sockets)
# the sender process sends 2 integers and the receiver sums them

import socket
from random import random
from os import fork, getpid
from time import sleep

#defining a class to handle the sockets with a simple interface
class testsocket:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def listen(self, port):
        self.sock.bind(('localhost',port))
        self.sock.listen(1)
        conn, addr = self.sock.accept()
        return conn, addr
    def connect(self, port):
        self.sock.connect(('localhost',port))
    def send(self,data):
        self.sock.sendall(data)
    def read(self, conn):
        # we are receiving the data as a string with space as separator
        data = conn.recv(1024)
        # building a list of integers from the string, that we will sum
        to_sum = map(int,[x for x in data.split(' ') if x])
        print '+ Sum is ' + str(sum(to_sum))
    def close(self):
        self.sock.close()

# the user will manually select the port used for communication on localhost
port = int(raw_input('Port number to use: '))
# defining a separator for the data (we'll be using strings)
sep = ' '
# the program terminates after 10 iterations
count = 0

# forking the process and storing parent/child info in newRef
newRef = fork()

# creating a socket in parent and child
sock1 = testsocket()

# parent process will be the sender
if newRef != 0:
    try:
        # allow some time to open the listener
        sleep(1)
        sock1.connect(port)
        sender = True
        print 'Sender PID is ' + str(getpid())
    except:
        print 'Failed to connect'
else:
    # child process will be the receiver
    print 'Receiver PID is ' + str(getpid())
    print 'Listening on port ' + str(port)
    conn, addr = sock1.listen(port)
    sender = False

# generate a random number
def genNumber():
    return str(int(100*random())) + sep

while count < 10:
    # code that will run only for the sender
    if sender == True:
        num1 = genNumber()
        num2 = genNumber()
        sock1.send(num1)
        print 'Sending ' + num1
        sock1.send(num2)
        print 'Sending ' + num2
        sleep(1)
        count += 1
    # code running for the receiver
    if sender == False:
        sleep(0.5)
        sock1.read(conn)
        count += 1

print 'Closing...'
sock1.close()