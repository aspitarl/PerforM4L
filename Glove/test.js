var fs = require("fs");

var slot = 2

var notes = [
  [1, 2],
  [1, 20],  
  [3, 4],
  [5, 6],
  [5, 10]
];

var unique_times = [1,3,5]


var chords = []
for (var i = 0; i < unique_times.length; i++){
    var time = unique_times[i]
    var chord = []
    for (var j = 0; j < notes.length; j++){
        if(notes[j][0] == time){
            chord.push(notes[j][1])
        }
    }

    chords.push(chord)
    
    
}

console.log(chords)

var json_out = {
	"pattrstorage" : 	{
		"name" : "chordstore",
		"slots" : 		{


            }
        }
    }

var new_item = {'id': slot , "data" : {
        "activekeys" : [ 60, 62, 63, 65, 67, 68, 70, 72, 74, 75, 77, 79, 80, 82, 84, 86 ],
    }
}

var slot_name = "slot_" + slot.toString()

json_out.pattrstorage.slots[slot_name] = new_item

for (var i = 1; i < chords.length + 1; i++){
    var name = "chord_" + i.toString()
    json_out.pattrstorage.slots[slot_name].data[name] = chords[i-1]
}

console.log(json_out)

// fs.writeFile("./ChordInfo_temp.json", JSON.stringify(json_out, null, 4), (err) => {
//     if (err) {
//         console.error(err);
//         return;
//     };
//     console.log("File has been created");
// });


// // inlets and outlets
// inlets = 1;
// outlets = 10;

// // global variables

// // float -- run the equation once
// function msg_int(r)
// {

//         outlet(0,r);
//         break;
//     case (r >= 11 && r <= 20):
//         outlet(1,r-10);
//         break;
//     case (r >= 21 && r <= 30):
//         outlet(2,r-20);
//         break;