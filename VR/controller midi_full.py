from triad_openvr import triad_openvr
import time
import sys
import rtmidi
import os

v = triad_openvr.triad_openvr()
v.print_discovered_objects()



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
    x = abs(data[0])
    y = abs(data[1])
    z = abs(data[2])

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

# if(yraw>halfwidth):
#     y = int((width - yraw)*(scaley*2)-ybottom) ###Flipped
# else:
#     y = int(yraw*(scaley*2)-ybottom) ###Flipped


while(True):
    start = time.time()

    contr = v.devices["controller_1"]

    inputs = contr.get_controller_inputs()
    
    buttonpress = inputs['ulButtonPressed']
    if buttonpress == 4:
        #enter range set mode

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

        while(buttonpress==4):
            data = contr.get_pose_euler()
            

            if data is not None:
                x, y, z = extractxyz(data)
                data_raw = {'x': x, 'y': y, 'z': z}

                for dim in data_raw:
                    if data_raw[dim] < cube_ranges[dim]['min']:
                        cube_ranges[dim]['min'] = data_raw[dim]
                    elif data_raw[dim] > cube_ranges[dim]['max']:
                        cube_ranges[dim]['max'] = data_raw[dim]


            buttonpress = contr.get_controller_inputs()['ulButtonPressed']

    else:
        #normal mode
        data = contr.get_pose_euler()

        trigger = inputs['trigger']
        
        if data is not None:
            
            x, y, z = extractxyz(data)
            data_raw = {'x': x, 'y': y, 'z': z}
            
            for dim in data_raw:

                if (dim == 'y') and (trigger == 1):
                    data_scaled[dim] = scale_data_half(data_raw, cube_ranges, dim)
                else: 
                    data_scaled[dim] = scale_data(data_raw, cube_ranges, dim)


            os.system('cls')
            print('raw data')
            print(data_raw['y'])
            print('scaled data')
            print(data_scaled['y'])

            # cc = [176, 23, y]
            # midiout.send_message(cc)