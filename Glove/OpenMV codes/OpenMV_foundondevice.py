import sensor, image, time
from pyb import UART
from pyb import USB_VCP
def timeprint(num):
	if(0):
		print(str(num) + ":" + str(clock.avg()))
		clock.reset()
		clock.tick()
usb = USB_VCP()
uart = UART(3, 9600)
uart.init(9600, bits=8, parity=None, stop=1)
sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)
sensor.set_auto_exposure(0,value=1)
sensor.skip_frames(time = 2000)
bg = sensor.snapshot()
bg = bg.copy()
sensor.set_auto_exposure(0,value=100)
clock = time.clock()
x = 0
y = 0
xbottom = 0
ybottom = 13
xtop = 0
ytop =  13
scalex = 127/(sensor.height()-xbottom - xtop)
scaley = 127/(sensor.width()-ybottom -ytop)
scalez = (127/(sensor.width()*sensor.height()))*10
mode = 1
while(True):
	if(mode):
		timeprint(0)
		img = sensor.snapshot()
		blob = img.find_blobs([(100,255)],area_threshold=2)
		if(len(blob)):
			bloblenlist = [0]*len(blob)
			i = 0
			for blobobj in blob:
				bloblenlist[i] = blobobj.pixels()
				i = i+1
			largeblob = blob[bloblenlist.index(max(bloblenlist))]
			y = int((largeblob.x() - ybottom)*(scaley))
			x = int((largeblob.y() - xbottom)*(scalex))
			z = int(largeblob.pixels()*scalez)
			if(x < 0):
				x = 0
			if(y < 0):
				y = 0
			if(x > 127):
				x = 127
			if(y > 127):
				y = 127
			usb.write(chr(x))
			usb.write(chr(y))
			usb.write(chr(z))
			usb.write("\r")
			uart.writechar(x)
			uart.writechar(y)
			uart.writechar(z)
			uart.writechar(10)
