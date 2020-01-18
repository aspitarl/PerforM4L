from triad_openvr import triad_openvr
import time
import sys
import rtmidi

v = triad_openvr.triad_openvr()
v.print_discovered_objects()



range = {
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



while(True):
    start = time.time()

    contr = v.devices["controller_1"]
    
    trigger = contr.get_controller_inputs()['trigger']

    if trigger == 1:
        #enter range set mode

        data = contr.get_pose_euler()
        x, y, z = extractxyz(data)

        range = {
            'x': [x, x],
            'y': [y, y],
            'z': [z, z]
        }        

        while(trigger):
            data = contr.get_pose_euler()
            

            if data is not None:
                x, y, z = extractxyz(data)
                data_raw = {'x': x, 'y': y, 'z': z}

                for dim in data_raw:
                    if data_raw[dim] < range[dim]['min']:
                        range[dim]['min'] = data_raw[dim]
                    elif data_raw[dim] > range[dim]['max']:
                        range[dim]['max'] = data_raw[dim]

    else:
        #normal mode
        data = contr.get_pose_euler()
        
        if data is not None:
            
            x, y, z = extractxyz(data)
            data_raw = {'x': x, 'y': y, 'z': z}
            
            for dim in data_raw:
                length = range[dim]['max'] - range[dim]['min']
                scaled = ((data_raw[dim]-range[dim]['min'])/range[dim]['max'])*outscale

                if scaled < 0:
                    scaled = 0
                elif scaled > outscale:
                    scaled = outscale

                data_scaled[dim] = scaled



            print('raw data')
            print(data_raw)
            print('scaled data')
            print(data_scaled)

            # cc = [176, 23, y]
            # midiout.send_message(cc)