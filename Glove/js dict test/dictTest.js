
//https://cycling74.com/forums/javascript-and-dict


autowatch = 1;

// example
function dictionary(dictName) {
	post("incoming dict name: " + dictName + "\n");
	
	var dataDict = new Dict(dictName);  
	var data = new Object();

	data = dict_to_jsobj(dataDict);
	
	printobj(data, dictName);
	
	var newDict = jsobj_to_dict(data);
	outlet(0, "dictionary", newDict.name);
}

// returns or includes null if there is a dict without containing data.
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

function jsobj_to_dict(o) {
	var d = new Dict();
	
	for (var keyIndex in o)	{
		var value = o[keyIndex];

		if (!(typeof value === "string" || typeof value === "number")) {
			var isEmpty = true;
			for (var anything in value) {
				isEmpty = false;
				break;
			}
			
			if (isEmpty) {
				value = new Dict();
			}
			else {
				var isArray = true;
				for (var valueKeyIndex in value) {
					if (isNaN(parseInt(valueKeyIndex))) {
						isArray = false;
						break;
					}
				}
			
				if (!isArray) {
					value = jsobj_to_dict(value);
				}
			}
		}
		d.set(keyIndex, value);
	}
	return d;
}

// this function will post a JS object's content to the max window
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