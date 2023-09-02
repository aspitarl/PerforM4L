inlets = 1;
outlets = 1;

var note=0;

var octave_out_offset=0;
var wrap_low_note=0;
var octave_out=0;


function msg_int(i)
{
    var result;

    var octave = Math.floor((i)/12);

    octave = octave % 2;

    var wrap_note_in = i % 12;

    if (wrap_note_in < wrap_low_note){
        wrap_note_in = wrap_note_in + 12
    }

    octave_out = octave + octave_out_offset

    result = wrap_note_in + octave_out*12

    outlet(0,result)
}


function set_oct_out_offset(v){
    octave_out_offset = v
}


function set_wrap_low_note(v){
    wrap_low_note = v
}