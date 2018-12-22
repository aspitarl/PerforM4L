import sensor, image, time

from pyb import UART
from pyb import USB_VCP

def timeprint(num):
    if(1):  # set to determine if times should be printed
        print(str(num) + ":" + str(clock.avg()))
        clock.reset()
        clock.tick()

usb = USB_VCP()

uart = UART(3, 9600)                         # init with given baudrate
uart.init(9600, bits=8, parity=None, stop=1) # init with given parameters

sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.GRAYSCALE) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)   # Set frame size to QVGA (320x240)

sensor.set_auto_exposure(0,value=1)

sensor.skip_frames(time = 2000)     # Wait for settings take effect.

bg = sensor.snapshot()      # get background first from short exposure
bg = bg.copy()

sensor.set_auto_exposure(0,value=100)

clock = time.clock()                # Create a clock object to track the FPS.

x = 0
y = 0    ###X AND Y FLIPPIED

xbottom = 0
ybottom = 13   #buffer from edges

xtop = 0
ytop =  13

width = sensor.width()
halfwidth = width/2


scalex = 127/(sensor.height()-xbottom - xtop)   # scale outputs to 127
scaley = 127/(sensor.width()-ybottom -ytop)
scalez = (127/(sensor.width()*sensor.height()))*10    #factor gives fraction of area that will max out integer


yhalf = sensor.width()/2
buf = 10
scaley_half = 64/(yhalf - 2*buf)

mode = 0
debug = 0 # 0 for debug 1 for run

while(True):
    #time.sleep(100)

    if(usb.any()):
        #halfmode = int.from_bytes(usb.read(), 'little')
        mode = int(usb.read())

    if not debug:
        #timeprint(0)

        img = sensor.snapshot()         # Take a picture and return the image.

        #img.difference(bg)

        #stat = img.get_statistics()
        #print(stat.max())

        #img.binary([(30,255)])
        blob = img.find_blobs([(100,255)],area_threshold=2)

        if(len(blob)):                  #Don't do anything if there are no blobs
            bloblenlist = [0]*len(blob)

            for i, blobobj in enumerate(blob):
                bloblenlist[i] = blobobj.pixels()

            largeblob = blob[bloblenlist.index(max(bloblenlist))]

            if(mode == 0): # Half Mode
                yraw = largeblob.x()
                if(yraw>halfwidth):
                    y = int((width - yraw)*(scaley*2)-ybottom) ###Flipped
                else:
                    y = int(yraw*(scaley*2)-ybottom) ###Flipped
            elif(mode == 1): # Regular
                y = int((width - largeblob.x() - ybottom)*(scaley)) ###Flipped
            else:
                yraw = width - largeblob.x()###Flipped
                if(yraw < buf):
                    y = 0
                elif(yraw > width - buf):
                    y = 127
                elif (abs(yraw - yhalf) <  buf + 1):
                    y = 64
                elif ( (yraw > buf) and (yraw< yhalf-buf ) ):
                    y = int((yraw - buf)*(scaley_half))
                elif ( (yraw > yhalf+ buf) and (yraw< width-buf ) ):
                    y = int((yraw+buf-width)*(scaley_half)+127)


            #timeprint(3)

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

            #print(y)

            if mode == 0 or mode == 1:
                color = x
                bright = y
            else:
                if y < 64:
                    bright = (y)+15
                else:
                    bright = (127-y)+15

                if y != 64:
                    color = 0
                else:
                    color = 124
            uart.writechar(color)
            uart.writechar(bright)
            uart.writechar(z)
            uart.writechar(10)

            #timeprint(3)
    #else:
        #img = sensor.snapshot()         # Take a picture and return the image.

        #stat = img.get_statistics()
        #usb.write(chr((stat.max())))

        #bg = sensor.snapshot()
        #bg = bg.copy()

