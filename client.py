# Import socket module
import socket
import string
import time
#import library for reading temperature
import os
import smbus

def measure_temp(bus):
	info = bus.read_byte_data(0x48, 0x00)
	return str(info)

def Main():
	#Sensor set up code
	i2c_bus = smbus.SMBus(1)	
	# local host IP '127.0.0.1'
	server = '192.168.1.124'
	local = socket.gethostbyname(socket.gethostname())
	# Define the port on which you want to connect
	port = 10000+236
	
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

	# connect to server on local computer
	s.connect((server,port))

	# message you send to server
	message = measure_temp(i2c_bus)
	while True:
		print "The body temperature of the patient "+local+" is "+message
		# message sent to server
		message ='2 ' + message 
		s.send(message.encode('ascii'))
		
		# messaga received from server
		data = s.recv(1024)

		# print the received message
		# here it would be a reverse of sent message
		print("The converted temperature received from the server "+server+ " is "+str(data.decode('ascii')))
		#wait for 2 seconds for another measurement
		time.sleep(2)
		message = measure_temp(i2c_bus)
	# close the connection
	s.close()

if __name__ == '__main__':
	Main()

