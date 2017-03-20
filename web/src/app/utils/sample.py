import socket
import os
import datetime as dt
from os import path

HOST = "192.168.4.1"
PORT = 23

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create the socket
print "Connecting..."
s.connect((HOST, PORT)) # Connect to the broom
print "Connected to %s!" % HOST
name = dt.datetime.now()
f = open('samples/sample_data_%s.kermit' % name, mode='w')
for i in range(500):
    res = s.recv(71) # receive some data
    if not path.exists('samples'):
        os.mkdir('samples')
    f.write(res)
    print res
f.close()
print "File saved in samples/sample_data_%s.kermit." % name
