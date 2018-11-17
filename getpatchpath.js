// inlets and outlets
inlets = 1;
outlets = 1;

// global variables

// float -- run the equation once


function bang()
{
var path = this.patcher.filepath
var path = path.split('/').slice(0,-1).join('/'); 

outlet(0,path)

}
