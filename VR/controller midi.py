from triad_openvr import triad_openvr
import time
import sys
import rtmidi

v = triad_openvr.triad_openvr()
v.print_discovered_objects()


midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

# here we're printing the ports to check that we see the one that loopMidi created. 
# In the list we should see a port called "loopMIDI port".
print(available_ports)

# Attempt to open the port
if available_ports:
    midiout.open_port(0)



if len(sys.argv) == 1:
    interval = 1/250
elif len(sys.argv) == 2:
    interval = 1/float(sys.argv[1])
else:
    print("Invalid number of arguments")
    interval = False


max = 1.3
min = 0.6
range = max-min


if interval:
    while(True):
        start = time.time()
        # txt = ""

        contr = v.devices["controller_1"]

        data = contr.get_pose_euler()

        if data is not None:
            
            y = abs(data[1])
            
            print(y)

            y = ((y-min)/range)*127

            if y < 0:
                y = 0
            elif y>127:
                y=127


            print(y)

            cc = [176, 23, y]

            midiout.send_message(cc)

            # for each in data:
            #     txt += "%.4f" % each
            #     txt += " "
            # print("\r" + txt, end="")
        sleep_time = interval-(time.time()-start)
        if sleep_time>0:
            time.sleep(sleep_time)