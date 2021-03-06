#!/usr/bin/env python
import sys
import socket
import json

#method names to validate
API_METHOD_BREW = "brew"
API_METHOD_RESET = "reset"

#IP address of the smarter coffee machine on your network
TCP_IP = 'XXX.XXX.XXX.XXX'
TCP_PORT = 2081
BUFFER_SIZE = 10

#default method to call
api_method = sys.argv[1]

if api_method == API_METHOD_BREW:
	message_to_send = "7"
elif api_method == API_METHOD_RESET:
	message_to_send = "\x10"

#make connection to machine and send message
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((TCP_IP, TCP_PORT))
	s.send(message_to_send)
	data = s.recv(BUFFER_SIZE)
	s.close()
except socket.error, msg:
	print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
	sys.exit();

#convert response from machine to unicode
return_code = unicode(data)

#set default values to ouput
success=0
message=""

#find out what the machine response means
if return_code =="\x03\x00~":
	success=1
	message="brewing"
elif return_code=="\x03\x01~":
	message="already brewing"
elif return_code=="\x03\x05~":
	message="no carafe"
elif return_code=="\x03\x06~":
	message="no water"
elif return_code=="\x03i~":
	success=1
	message="reset"
else:
	message="check machine"

#ouput JSON to whatever called this script
print json.dumps({'success': success,'message':message,'return_code':repr(data)[1:10]})

quit()
sys.exit()
