# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 20:51:16 2018

@author: alexa
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 17:25:33 2018

@author: alexa
"""
#first run arduino file 'sketch_oct20a.ino'

import socket         
import time
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd

vibr_data = []
full_data = []
timeout = 5   # [seconds]
#T = 0.005 #set frequence to 10ms

timeout_start = time.time()      
 
sock = socket.socket()
 
#host = "192.168.2.108" #ESP32 IP in local network
host = "192.168.8.172"
#host = "192.168.137.1"
port = 80            #ESP32 Server Port    
 
sock.connect((host, port))

#read one line from the socket
def buffered_readLine(socket):
    line = ""
    while True:
        part = sock.recv(1)
        part = part.decode('utf-8')
        if part != "\n":
            line+=part
        elif part == "\n":
            break
    return line
#time.sleep(3)
while time.time() < timeout_start + timeout: 
    data = buffered_readLine(sock)
    vibr_data.append(data.replace('\r', ''))

sock.close()

for i in vibr_data:
    plot_data = [float(x) for x in i.split(' ')]
    full_data.append(plot_data)

full_data = np.array(full_data)
df = pd.DataFrame(full_data)
df.to_csv('C:/Users/alexa/Desktop/M5/data.csv')
y1 = full_data[:,0]
y2 = full_data[:,1]
y3 = full_data[:,2]

N = len(y1)
T = timeout/N
x = np.linspace(0.0, N*T, N)
Y1 = np.fft.fft(y1) # fft computing 
Y2 = np.fft.fft(y2)
Y3 = np.fft.fft(y3)

freq = np.fft.fftfreq(N, T)

f, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(6, 1, figsize=(13, 14))
ax1.plot(x,y1)
ax1.set_xlabel('Time')
ax1.set_ylabel('Amplitude X')
ax2.plot(freq[1:int(len(freq)/2)],abs(Y1[1:int(len(Y1)/2)]),'r') # plotting the spectrum
ax2.set_xlabel('Freq (Hz)')
ax2.set_ylabel('X(freq)')

ax3.plot(x,y2)
ax3.set_xlabel('Time')
ax3.set_ylabel('Amplitude Y')
ax4.plot(freq[1:int(len(freq)/2)],abs(Y2[1:int(len(Y2)/2)]),'r') # plotting the spectrum
ax4.set_xlabel('Freq (Hz)')
ax4.set_ylabel('Y(freq)')

ax5.plot(x,y3)
ax5.set_xlabel('Time')
ax5.set_ylabel('Amplitude Z')
ax6.plot(freq[1:int(len(freq)/2)],abs(Y3[1:int(len(Y3)/2)]),'r') # plotting the spectrum
ax6.set_xlabel('Freq (Hz)')
ax6.set_ylabel('Z(freq)')



    
    
    
    
    