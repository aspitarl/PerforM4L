A collection of max for live devices that I use. Mostly geared toward jamming/performance. 

*Installation*
Include the folder in your max search path (Like PATH, PYTHONPATH, etc. but for max), otherwise common dependencies (Like the mapping suppatcher) will not be found. In max go to Options -> File Preferences 

*Explanation/Instructions*
Fishman: template gives 6 tracks, one for each string of guitar. The midi is then routed to an instrument with 6 chains, one for each string. This allows for a separate pitchbend for each string of the guitar
Glove: Gets data from a custom glove xy controller comprised of an OpenMV cam and an IR LED and maps to live paramters. Some Arduino code in here to control Neopixels attached to the glove (OpenMV cam communicates directly with arduino). 
Foot Controller: Device controlled a FCB1010 foot controller and does things with live or sends messages to the other patches.
Tension: an attempt to add 'tesnion' building elements (risers, claps ,etc.) in real-time. Not fully finished.
Timing: Some stuff to control tempo and scene triggering when in session view. 
Visual: Patches to control visual things to music. One patch controls Adafruit Neopixels with serial communicaiton to an Arduino. There are also jitter patches to work with VModule (see below), but I never got these working reliably. Got stuck tring to figure out how to use textures in order to efficiently utilize GPU.

*Credit*
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
Creative Common �No Derivative Works� licence
http://fabriziopoce.com/max.html

Mapping: Not really sure where I got this from but includes "core by christian kleine, thanks for that!"
http://christiankleine.com/ck/home.html