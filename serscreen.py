import cv2;
import numpy as np
import socket
import sys
import pickle
import struct, thread
from PIL import ImageGrab
import time
from PIL import Image
from StringIO import StringIO
import PIL
import pyautogui

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

s.bind(('127.0.0.1',8000));
s.listen(10);
conn_list=[]

def serverScreenShare(conn) :
	while True:
		imgobj=ImageGrab.grab()
		st = StringIO()
		imgobj=imgobj.resize((1180,620), PIL.Image.ANTIALIAS)
		imgobj.save(st, "JPEG", quality=70, optimize=True, progressive=True)
		print len(st.getvalue())
		conn.send(str(len(st.getvalue())))
		conn.send(st.getvalue())   # notify the client of the change
		st.close()
		time.sleep(0.1)


while True:

	conn, addr = s.accept();
	conn_list.append(conn);
	print addr
	thread.start_new(serverScreenShare,(conn,));