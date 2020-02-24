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

trigger_on_mem = 0

if interval:
    while(True):
        start = time.time()
        # txt = ""

        contr = v.devices["controller_1"]

        trigger = contr.get_controller_inputs()['trigger']

        
        if trigger < 0.3:
            trigger_on = 0
        else:
            trigger_on = 127
        

        if trigger_on != trigger_on_mem:

            trigger_on_mem = trigger_on


            cc = [176, 23, trigger_on]

            print(cc)

            midiout.send_message(cc)

            # for each in data:
            #     txt += "%.4f" % each
            #     txt += " "
            # print("\r" + txt, end="")
        sleep_time = interval-(time.time()-start)
        if sleep_time>0:
            time.sleep(sleep_time)