from triad_openvr import triad_openvr
import time
import sys
import rtmidi
import os
import signal

interval = 1/250
# interval = 0

print('wait interval is ' + str(interval))

v = triad_openvr.triad_openvr()
v.print_discovered_objects()


if len(sys.argv) == 1:
    controller_name = "controller_1"
elif len(sys.argv) == 2:
    controller_name = "controller_" + str(sys.argv[1])

print("connecting to " + controller_name)
contr = v.devices[controller_name]

if controller_name == "controller_1":
    cc_dict = {
    'x': 22,
    'y': 23,
    'z': 24
}

    midiportname = 'Controller A'

elif controller_name == "controller_2":
    cc_dict = {
    'x': 25,
    'y': 26,
    'z': 27
}

    midiportname = 'Controller B'

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

def signal_handler(signal, frame):
    """Runs and exits when crtl-C is pressed"""
    print("\nprogram exiting gracefully")
    midiout.close_port()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# here we're printing the ports to check that we see the one that loopMidi created. 
# In the list we should see a port called "loopMIDI port".

midi_connected = False

for i, port in enumerate(available_ports):
    if midiportname in port:
        print('Connecting to midi port: ' + port)
        midiout.open_port(i)
        midi_connected = True

if not midi_connected:
    print('Could not find port ' + midiportname + ' in following midi ports')
    print(available_ports)

cube_ranges = {
    'x': {'min': 0.7, 'max': 1.3},
    'y': {'min': 0.7, 'max': 1.3},
    'z': {'min': 0.7, 'max': 1.3}
}

outscale = 127

data_scaled = {
    'x': outscale/2,
    'y': outscale/2,
    'z': outscale/2
}

def scale_data(data_raw, cube_ranges, dim):
    length = cube_ranges[dim]['max'] - cube_ranges[dim]['min']
    scaled = ((data_raw[dim]-cube_ranges[dim]['min'])/length)*outscale

    if scaled < 0:
        scaled = 0
    elif scaled > outscale:
        scaled = outscale

    return scaled

def scale_data_half(data_raw, cube_ranges, dim):
    halflength = (cube_ranges[dim]['max'] - cube_ranges[dim]['min'])/2

    data = data_raw[dim] - cube_ranges[dim]['min']

    if data < halflength:
        data = data
    elif data > halflength:
        data = (2*halflength) - data

    scaled = (data/halflength)*outscale

    if scaled < 0:
        scaled = 0
    elif scaled > outscale:
        scaled = outscale

    return scaled

def range_set_mode(contr, debugstr=''):
    inputs, pose = get_inputs_and_pose(contr)

    cube_ranges = {
        'x': {'min': pose['x'], 'max': pose['x']},
        'y': {'min': pose['y'], 'max': pose['y']},
        'z': {'min': pose['z'], 'max': pose['z']}
    }      

    while(inputs['button'] == 'b'):
        inputs, pose = get_inputs_and_pose(contr)

        if debug: debugstr = 'Range Set Mode: '
        if debug: debugstr = debugstr + '\nPose: ' + str(pose)

        if pose is not None:
            for dim in pose:
                if pose[dim] < cube_ranges[dim]['min']:
                    cube_ranges[dim]['min'] = pose[dim]
                elif pose[dim] > cube_ranges[dim]['max']:
                    cube_ranges[dim]['max'] = pose[dim]

            if debug: debugstr = debugstr + '\nRange: ' + str(cube_ranges)
        
        #Old code for exiting
        # trigger = inputs['trigger']
        # if  trigger == 1:
        #     #exit button (have to fully pull trigger)
        #     running = False
        #     rangesetbutton = False

        sleep_time = interval-(time.time()-start)
        if sleep_time>0:
            time.sleep(sleep_time)
        
        if debug:
            #not working in anaconda prompt?
            os.system('cls')
            print(debugstr)

    return cube_ranges
    
def get_inputs_and_pose(contr):

    #Pose
    positionarray = contr.get_pose_euler()

    if positionarray == None:
        pose = None
    else:
        pose = {
            'x': positionarray[0],
            'y': positionarray[1],
            'z': positionarray[2]
            }

    #Inputs
    inputs = contr.get_controller_inputs()

    button= inputs['ulButtonPressed']
    
    if button==2 or button==6:
        inputs['button'] = 'b'
    elif button == 4:
        inputs['button'] = 'a'
    else:
        inputs['button'] = None

    return inputs, pose

debug = True
running = True
while(running):
    start = time.time()

    inputs, pose = get_inputs_and_pose(contr)

    if debug: 
        debugstr = 'Controller: ' + controller_name + '\nMidi Port Name: ' + midiportname + '\nInputs ' + str(inputs)

    if inputs['button'] == 'b':
        #enter range set mode
        cube_ranges = range_set_mode(contr, debugstr)
    else:
        #normal mode
        if debug: debugstr = debugstr + '\nNormal Mode:'
        if debug: debugstr = debugstr + '\nPose: ' + str(pose)
        trigger = inputs['trigger']
        
        if pose is not None:   
            for dim in pose:
                if (dim == 'y') and (trigger == 1):
                    data_scaled[dim] = scale_data_half(pose, cube_ranges, dim)
                else: 
                    data_scaled[dim] = scale_data(pose, cube_ranges, dim)

            if debug: debugstr = debugstr + '\nScaled Pose: ' + str(data_scaled)

            if inputs['trackpad_touched']:
                ccx = [176, cc_dict['x'], data_scaled['x']]
                midiout.send_message(ccx)            
                ccy = [176, cc_dict['y'], data_scaled['y']]
                midiout.send_message(ccy)                  
                ccz = [176, cc_dict['z'], data_scaled['z']]
                midiout.send_message(ccz)  

                if debug: debugstr = debugstr + '\nCCx Message: ' + str(ccx)
                if debug: debugstr = debugstr + '\nCCy Message: ' + str(ccy)
                if debug: debugstr = debugstr + '\nCCz Message: ' + str(ccz)


    sleep_time = interval-(time.time()-start)
    if sleep_time>0:
        time.sleep(sleep_time)
        
    if debug: 
        os.system('cls')
        print(debugstr)
        

