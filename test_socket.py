import socket
from random import random
from os import fork, getpid
from time import sleep

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
        data = conn.recv(1024)
        to_sum = map(int,[x for x in data.split(' ') if x])
        print '+ Sum is ' + str(sum(to_sum))
    def close(self):
        self.sock.close()

port = int(raw_input('Port number to use: '))
sep = ' '
count = 0

newRef = fork()

sock1 = testsocket()

if newRef != 0:
    try:
        sleep(1)
        sock1.connect(port)
        sender = True
        print 'Sender PID is ' + str(getpid())
    except:
        print 'Failed to connect'
else:
    print 'Receiver PID is ' + str(getpid())
    print 'Listening on port ' + str(port)
    conn, addr = sock1.listen(port)
    sender = False

def genNumber():
    return str(int(100*random())) + sep

while count < 10:
    if sender == True:
        num1 = genNumber()
        num2 = genNumber()
        sock1.send(num1)
        print 'Sending ' + num1
        sock1.send(num2)
        print 'Sending ' + num2
        sleep(1)
        count += 1
    if sender == False:
        sleep(0.5)
        sock1.read(conn)
        count += 1

print 'Closing...'
sock1.close()