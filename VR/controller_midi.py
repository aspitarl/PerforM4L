from triad_openvr import triad_openvr
import time
import sys
import rtmidi
import os

interval = 1/250
# interval = 0

print('wait interval is ' + str(interval))

v = triad_openvr.triad_openvr()
v.print_discovered_objects()


if len(sys.argv) == 1:
    controller_name = "controller_1"
elif len(sys.argv) == 2:
    controller_name = "controller_" + str(sys.argv[1])


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

print(controller_name)

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

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
    'x': {
        'min': 0.7,
        'max': 1.3
    },
    'y': {
        'min': 0.7,
        'max': 1.3
    },
    'z':  {
        'min': 0.7,
        'max': 1.3
    }
}

data_raw = {
    'x': 1,
    'y': 1,
    'z': 1
}

outscale = 127

data_scaled = {
    'x': outscale/2,
    'y': outscale/2,
    'z': outscale/2
}

def extractxyz(data):
    x = data[0]
    y = data[1]
    z = data[2]

    return x, y, z

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

# debug = True

running = True
while(running):
    start = time.time()

    inputs = contr.get_controller_inputs()

    debug=True if inputs['grip_button'] else False #a button. note that this also correponds to grip button. can't figure out a way to distinguish.
    if debug: 
        debugstr = 'Controller: ' + controller_name + '\nMidi Port Name: ' + midiportname + '\nInputs ' + str(inputs)

    rangesetbutton = inputs['ulButtonPressed']

    if rangesetbutton == 2:
        #enter range set mode
           

        data = contr.get_pose_euler()

        while(data is None):
            debugstr = debugstr + '\nGot None for data, trying again'
            time.sleep(0.01)
            data = contr.get_pose_euler()


        x, y, z = extractxyz(data)

        cube_ranges = {
            'x': {
                'min': x,
                'max': x
            },
            'y': {
                'min': y,
                'max': y
            },
            'z':  {
                'min': z,
                'max': z
            }
        }      

        while(rangesetbutton==2):
            debug = True  
            rangesetbutton = inputs['ulButtonPressed']

            if debug: debugstr = 'Range Set Mode: '
            if debug: debugstr = debugstr + '\nPose: ' + str(data)

            data = contr.get_pose_euler()

            if data is not None:
                x, y, z = extractxyz(data)
                data_raw = {'x': x, 'y': y, 'z': z}

                for dim in data_raw:
                    if data_raw[dim] < cube_ranges[dim]['min']:
                        cube_ranges[dim]['min'] = data_raw[dim]
                    elif data_raw[dim] > cube_ranges[dim]['max']:
                        cube_ranges[dim]['max'] = data_raw[dim]

                if debug: debugstr = debugstr + '\nRange: ' + str(cube_ranges)
            
            trigger = contr.get_controller_inputs()['trigger']

            if  trigger == 1:
                #exit button (have to fully pull trigger)
                running = False
                rangesetbutton = False

            inputs = contr.get_controller_inputs()

            sleep_time = interval-(time.time()-start)
            if sleep_time>0:
                time.sleep(sleep_time)
            
            if debug:
                #not working in anaconda prompt?
                os.system('cls')
                print(debugstr)
                
    else:
        #normal mode
        if debug: debugstr = debugstr + '\nNormal Mode:'
        data = contr.get_pose_euler()
        if debug: debugstr = debugstr + '\nPose: ' + str(data)
        trigger = inputs['trigger']
        
        if data is not None:
            
            x, y, z = extractxyz(data)
            data_raw = {'x': x, 'y': y, 'z': z}
            
            for dim in data_raw:

                if (dim == 'y') and (trigger == 1):
                    data_scaled[dim] = scale_data_half(data_raw, cube_ranges, dim)
                else: 
                    data_scaled[dim] = scale_data(data_raw, cube_ranges, dim)


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
        

midiout.close_port()