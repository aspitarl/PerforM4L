

//var fs = require("fs");



// inlets and outlets
inlets = 1;
outlets = 1;

// global variables
var json_out = {
     "pattrstorage" : 	{
         "name" : "chordstore",
         "slots" : 		{


             }
         }
     }


var path = this.patcher.filepath
var path = path.split('/').slice(0,-1).join('/') + "/ChordInfo.json"; 



function bang(){
//Resets the global json_out variable and erases the file


json_out = {
     "pattrstorage" : 	{
         "name" : "chordstore",
         "slots" : 		{


             }
         }
     }


var f = new File(path,'write','TEXT');
f.eof = 0;
f.close();



}



function dictionary(){
// Adds a dictionary to json_out



dictname = arguments[0]
var dict = new Dict(dictname); 
var data = new Object();
data = dict_to_jsobj(dict); 

var notes = data['notes']
var times = data['times']
var slot = data['slot']

var unique_times = times.filter(onlyUnique)
unique_times.sort(sortNumber)




var chords = []
for (var i = 0; i < 16; i++){
	var chord = []
	if (i < unique_times.length){		
		var time = unique_times[i]
		
		for (var j = 0; j < notes.length; j++){
			if(times[j] == time){
				chord.push(notes[j])
			}
		}
    }
	else{
		chord.push(999)
	}

    chords.push(chord)
    
    
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

}



function write(){
//Write json_out to the file

var json_string = JSON.stringify(json_out, null, 4)


var f = new File(path,'write','TEXT');
f.writestring(json_string);
f.close();

outlet(0,path)
}



// ------------utilities---------

//not all being used, kept for reference. 


function dict_to_jsobj(dict) {
	if (dict == null) return null;
	var o = new Object();
	var keys = dict.getkeys();
	if (keys == null || keys.length == 0) return null;

	if (keys instanceof Array) {
		for (var i = 0; i < keys.length; i++)
		{
			var value = dict.get(keys[i]);
			
			if (value && value instanceof Dict) {
				value = dict_to_jsobj(value);
			}
			o[keys[i]] = value;
		}		
	} else {
		var value = dict.get(keys);
		
		if (value && value instanceof Dict) {
			value = dict_to_jsobj(value);
		}
		o[keys] = value;
	}

	return o;
}

function printobj (obj, name) {
    post("---- object " + name + "----" +"\n");
    printobjrecurse(obj, name);
}

function printobjrecurse (obj, name) {
    if (typeof obj === "undefined") {
        post(name + " : undefined" +"\n");
        return;
    }
    if (obj == null) {
        post(name + " : null" +"\n");
        return;
    }

    if ((typeof obj == "number") || (typeof obj == "string")) {
        post(name +  " :" + obj + "\n");
    } else {
        var num = 0;
        for (var k in obj) {
            post(k)
            if (obj[k] && typeof obj[k] == "object")
            {
                printobjrecurse(obj[k], name + "[" + k + "]");
            } else {
                post(name + "[" + k + "] : " + obj[k] +"\n")
            }
            num++;
        }
        if (num == 0) {
            post(name + " : empty object" +"\n");
        }
    }
}

function read(path) {
	memstr = "";
	data = "";
	maxchars = 800;
	var f = new File(path,"read");
	f.open();
	if (f.isopen) {
		while(f.position<f.eof) {
			memstr+=f.readstring(maxchars);
		}
		f.close();
	} else {
		post("Error\n");
	}
    UI = JSON.parse(memstr);
    
    return UI
	//UI = eval("("+memstr+")"); //much less secure, but could work
	// post("\nJSON Read",path);
}

function sortNumber(a,b) {
    return a - b;
}


function onlyUnique(value, index, self) { 
    return self.indexOf(value) === index;
}