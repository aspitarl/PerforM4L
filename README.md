
## Installation

Include the folder in your max search path (Like PATH, PYTHONPATH, etc. but for max), otherwise common dependencies (Like the mapping suppatcher) will not be found. In max go to Options -> File Preferences. Use ableton to open max to make sure it's the same max installation. 

There are project 'templates' included which are just live sets meant to be dragged and dropped into projects.

## Components

### Fishman

Patches for use with Fishman Triple Play MIDI to guitar.  

* Template gives 6 tracks, one for each string of guitar. The midi is then routed to an instrument with 6 chains, one for each string. This allows for a separate pitchbend for each string of the guitar. The Fishman needs to be set to to Mono mode, as well as auto pitchbend to stop stepping during bends). 
* In order to change the instrument, delete all the chains in the instrument rack except the first one, replace the instrument in that chain, set the pitchbend to +-12 or use the PB_range patch, and then duplicate the chain 5 times. 
* To record the six clips at once, ableton needs to have the 'start record on scene launch' enabled. 
* There are also some (untested recently) to do things like to hold a chord. This uses the foot controller to toggle a gate that doesn't pass note on events until another button is pressed on the foot pedal.

### Glove

Gets data from a custom glove xy controller comprised of an OpenMV cam and an IR LED and maps to live paramters. 


* This can be used with a 'chords' patch that maps chords to notes so that saved chords can be played with a single note. Currently, the best way to load chords is to have a series of midi clips in the adjacent track to the chords device with single chords in each clip. Then press the scrape button (also triggered by foot pedal) to pull those chords in. There is also json saving functionality, not stress tested yet. 
* There is a midifilter patch that has a high and low filter to only pass high or low notes. This can be usedto split up the synth into chords and bass by having the bass notes a coupe octaves too low to pass through the filter and then just pitch them up a couple octaves before the instrument.
* Some Arduino code in here to control Neopixels attached to the glove (OpenMV cam communicates directly with arduino).

### Foot Controller

Device recieves program chanes from a FCB1010 foot controller and does things with live or sends messages to the other patches. 

* This device also can read and save a json file with the live set 'presets' (FootSettings.json) The preset includes which tracks are armed, which fishman recieve tracks should be activated, and the map paths corresponding to the foot controller pedals and the glove xyz mappers. Each of these has a 'mappath' which is the literal path pointing to the parameter, and the mappathid, which holds the id of the parameter. Once new tracks and such have been added, the paths will get screwed up. Press 'reset tracks' to recalculate the paths based off the mappathids. 
* Also reads in a text file (FootControllerinfo.txt) that describes what the program changes do. 

### Timing 

Some stuff to control tempo and scene triggering when in session view. 

### Ableton Workflow 

Some stuff to use the live object model to automate tasks. Believe the TramsposeMMC is working, which transposes all clips to change the key of a song, but haven't tested it recently. 

### Tension

An attempt to add 'tesnion' building elements (risers, claps ,etc.) in real-time. Not fully finished.

### Visual

Patches to control visual things to music. One patch controls Adafruit Neopixels with serial communicaiton to an Arduino. There are also jitter patches to work with VModule (see below), but I never got these working reliably. Got stuck tring to figure out how to use textures in order to efficiently utilize GPU.

## Credit

This library includes original M4L devices, but also M4L devices pulled from the internet that I tweaked and altered: 

Transpose MMC 1.0
Author:	Because789
License (more info):	None
http://www.maxforlive.com/library/device/1852/transpose-mmc

Chords 2.11
Author:	lilTrybe
License (more info):	None
http://www.maxforlive.com/library/device/2885/chords

V-Module
Author:	Fabrizio Poce
Creative Common “No Derivative Works” licence
http://fabriziopoce.com/max.html

Mapping: Not really sure where I got this from but includes "core by christian kleine, thanks for that!"
http://christiankleine.com/ck/home.html
