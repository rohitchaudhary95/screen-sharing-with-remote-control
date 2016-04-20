import socket, cv2, pickle, struct, thread
import numpy as np
from PIL import ImageGrab
from PIL import Image
from StringIO import StringIO
import wx
import time

HOST="192.168.43.28"
PORT=8000

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM);
print "Socket created";

s.connect((HOST, PORT));
print "connected"

class MyFrame(wx.Frame):
    def __init__(self, parent,title):
        wx.Frame.__init__(self, parent,title=title, size=(1200,750))
        self.SetCursor(wx.StockCursor(wx.CURSOR_PENCIL))
        self.panel = wx.Panel(self)
        self.panel.SetSize((1180,620))
        self.myWxImage = wx.EmptyImage( 1180, 620 )
        self.imageCtrl = wx.StaticBitmap(self.panel,wx.ID_ANY,wx.BitmapFromImage(self.myWxImage))
        self.NH=0
        self.NW=0
        # hook some mouse events
        self.imageCtrl.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.imageCtrl.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.imageCtrl.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDouble)
        self.panel.Bind(wx.EVT_KEY_DOWN, self.OnKeyPress)
        self.Show(True)

    def OnLeftDown(self, event):
        ptx = event.GetX()
        pty = event.GetY()
        print "x--->" + str(ptx)
        print "y--->"+str(pty)
        s.send("10")
        s.send("1")
        s.send(str(len(str(ptx))))
        s.send(str(ptx))
        s.send(str(len(str(pty))))
        s.send(str(pty))
        
    
    def OnRightDown(self, event):
        ptx = event.GetX()
        pty = event.GetY()
        print "x--->" + str(ptx)
        print "y--->"+str(pty)
        s.send("10")
        s.send("2")
        s.send(str(len(str(ptx))))
        s.send(str(ptx))
        s.send(str(len(str(pty))))
        s.send(str(pty))
        

    def OnLeftDouble(self, event):
        ptx = event.GetX()
        pty = event.GetY()
        print "x--->" + str(ptx)
        print "y--->"+str(pty)
        s.send("10")
        s.send("3")
        s.send(str(len(str(ptx))))
        s.send(str(ptx))
        s.send(str(len(str(pty))))
        s.send(str(pty))

    def OnKeyPress(self, event):
		keycode = event.GetKeyCode()
		s.send("10")
		s.send("4")
		print "adasdf" + str(chr(keycode))
		s.send(str(len(str(keycode))))
		s.send(str(keycode))
    
    def onView(self,a):
    	si=StringIO(a)
    	im = Image.open(si)
    	print im.size[0],im.size[1]
    	img=wx.ImageFromBuffer(im.size[0],im.size[1],im.tobytes())
    	self.NW=1180
    	self.NH=620
    	self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
    	self.panel.Refresh()
    	#img = img.Scale(1080,720)
    	si.close()



app = wx.App(False)
frame = MyFrame(None,'screen sharing')
def fun(sr):
	while True:
		lent = int(s.recv(6))
		s.send("ok")
		a = s.recv(lent)
		frame.onView(a)
		time.sleep(0.1)
thread.start_new(fun,("fh",))
app.MainLoop()
s.close()
	