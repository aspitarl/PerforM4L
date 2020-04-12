from triad_openvr import triad_openvr
import time
import sys
import rtmidi
import os
import signal

from rtmidi.midiconstants import CONTROL_CHANGE, PITCH_BEND

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

#TODO: Figure out whether these dicts should be same or different (stress test 1 midi channel...)

if controller_name == "controller_1":
    cc_dict = {
    'x': 22,
    'y': 23,
    'z': 24,
    'tpy':25,
}

    midiportname = 'Controller A'

elif controller_name == "controller_2":
    cc_dict = {
    'x': 22,
    'y': 23,
    'z': 24,
    'tpy':25,
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

rangesetbutton = 'b'
senddatabutton = 'a'


def scale_data(data_raw, cube_ranges, dim, half):

    length = cube_ranges[dim]['max'] - cube_ranges[dim]['min']
    relative_dist = data_raw[dim] - cube_ranges[dim]['min']

    if half:
        halflength = length/2

        if relative_dist < halflength:
            relative_dist = relative_dist
        elif relative_dist > halflength:
            relative_dist = length - relative_dist

        scaled = (relative_dist/halflength)*outscale  
    else:  
        scaled = (relative_dist/length)*outscale

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

    while(inputs['button'] == rangesetbutton):
        debugstr = ''

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

    #Convert weird button number system into something simpler
    if inputs['ulButtonPressed']==2 or inputs['ulButtonPressed']==6:
        inputs['button'] = 'b'
    elif inputs['grip_button'] == True: # inputs['ulButtonPressed'] == 4 not true when trigger
        inputs['button'] = 'a'
    else:
        inputs['button'] = None

    return inputs, pose

debug = False
running = True

trackpad_reset = False #used to reset pitchbend after letting go of touchpad
while(running):
    start = time.time()

    inputs, pose = get_inputs_and_pose(contr)

    if debug: 
        debugstr = 'Controller: ' + controller_name + '\nMidi Port Name: ' + midiportname + '\nInputs ' + str(inputs)

    if inputs['button'] == rangesetbutton:
        #enter range set mode
        cube_ranges = range_set_mode(contr)
    else:
        #normal mode
        if debug: debugstr = debugstr + '\nNormal Mode:'
        if debug: debugstr = debugstr + '\nPose: ' + str(pose)
        trigger = inputs['trigger']
        
        if pose is not None:   
            for dim in pose:
                if (dim == 'y') and (trigger == 1):
                    data_scaled[dim] = scale_data(pose, cube_ranges, dim, half=True)
                else: 
                    data_scaled[dim] = scale_data(pose, cube_ranges, dim, half=False)

            if debug: debugstr = debugstr + '\nScaled Pose: ' + str(data_scaled)

            if inputs['button'] == senddatabutton or inputs['trackpad_touched']:
                ccx = [CONTROL_CHANGE, cc_dict['x'], data_scaled['x']]
                midiout.send_message(ccx)            
                ccy = [CONTROL_CHANGE, cc_dict['y'], data_scaled['y']]
                midiout.send_message(ccy)                  
                ccz = [CONTROL_CHANGE, cc_dict['z'], data_scaled['z']]
                midiout.send_message(ccz)  

                if debug: debugstr = debugstr + '\nCCx Message: ' + str(ccx)
                if debug: debugstr = debugstr + '\nCCy Message: ' + str(ccy)
                if debug: debugstr = debugstr + '\nCCz Message: ' + str(ccz)

                if inputs['trackpad_touched']:
                    tpy = int(inputs['trackpad_y']*64+64)

                    cctpy = [CONTROL_CHANGE, cc_dict['tpy'], tpy]
                    midiout.send_message(cctpy)  


                    # pb = [PITCH_BEND, 0 , pb]
                    # midiout.send_message(pb)

                    # if debug: debugstr = debugstr + '\npb Message: ' + str(pb)
                    trackpad_reset = True
            else:
                if trackpad_reset:
                    cctpy = [CONTROL_CHANGE, cc_dict['tpy'], 64]
                    midiout.send_message(cctpy)
                    trackpad_reset = False
                    


    sleep_time = interval-(time.time()-start)
    if sleep_time>0:
        time.sleep(sleep_time)
        
    if debug: 
        os.system('cls')
        print(debugstr)
        

