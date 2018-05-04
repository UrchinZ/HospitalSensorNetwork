# import socket programming library
import socket
 
# import thread module
from thread import *
import threading

#import library for reading temperature
import os

#import GPIO library
import RPi.GPIO as GPIO

#import time library
import time 

#temperature measuring function
def convert_temp(info):
    celcius = float(info.split('\'')[0])
    fahrenheit = 1.8*celcius+32
    return fahrenheit

#function to turn on LED
def turn_on_LED(ledpin):
    GPIO.output(ledpin,GPIO.HIGH)    

#function to turn off LED
def turn_off_LED(ledpin):
    GPIO.output(ledpin,GPIO.LOW)
    
#function to buzz buzzer for 2 seconds
def buzz():
    GPIO.output(27,GPIO.HIGH)
    time.sleep(2)
    GPIO.output(27,GPIO.LOW)    
 
# thread fuction
def threaded(c,addr):
    while True:
 
        # data received from client
        data = c.recv(1024)
        if not data:
            print('Bye')
            break
        
        converted = convert_temp(data)
        print addr[0]+" : "+data+" to "+ str(converted)+'\'F'
	
	# Determine what client is sending data
        clientnum = int(addr[0].split('.')[-1])
    	print clientnum
        clientnum = 2 #testing
        # send CPU temperature back to client
        c.send(str(converted)+'\'F')
	if converted > 78:
	    buzz()
	    turn_on_LED(clientnum)		  
	    print("raise alarm")
	else:
	    turn_off_LED(clientnum)		    
	    print("normal")
    # connection closed
    c.close()

 
def Main():
    host = ""
 
    # reverse a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 10000+236
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)
 
    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")
    
    #setup output GPIO pins   
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for v in range(2,28):	#all led pins and buzzer ping 
        GPIO.setup(v,GPIO.OUT)
    
    # a forever loop until client wants to exit
    while True:
 
        # establish connection with client
        c, addr = s.accept()
 
        # Start a new thread and return its identifier
        start_new_thread(threaded, (c,addr,))
    s.close()
 
 
if __name__ == '__main__':
    Main()
