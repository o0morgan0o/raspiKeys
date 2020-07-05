# RaspiKeys

RaspiKeys is a raspberry based project, for intermediate or advanced pianists. It provides a practise tool which help musicians to practise their Ear and to practise a collection of licks in all keys. It also provides drum loops playing.

# Usage

**Wanring:** In order to work for the moment you must have a digital keyboard which supports USB-Midi transmission.


### Connection and parts

(schema de connection)


## Main Window

When you power on the device, after startup you should see this screen:
(image)



## Modes

The differents practise modes of the raspiKeys are the following:

1. EarN : Ear Training of note intervals. When you push a note, you hear another note, you should find the interval played between these two notes.
2. EarC : Ear Training of chords. When you push a note, you will hear several other notes (all compose a more or less difficult chord inversion), you should guess all the notes proposed.
3. BkTr : Play a drum loop. Just practise a groove on a random drum loop of the collection.
4. Lick : Practise your favorites licks or chord progression. Record you own short chord progression and melody and practise it in all keys.


## EarN (Ear Training Note)

## EarC (Ear Training Chord)

## BkTr (DrumLoop)

## Lick 

##

Work in progress ...

Program is autostarted at boot in /etc/xdg/autostart/raspiKeys.desktop

```sh
[Desktop Entry]
Type=Application
Name=RaspiKeys
Comment=Run at startup raspiKeys application
NoDisplay=false
Exec=/home/pi/raspiKeys/runPi.sh
NotShowIn=GNOME;KDE;XFCE;
```

TODO : make documentation, and tutorial
TODO : solve bug order of licks loaded
TODO:  solve gui problems and fixes
TODO : improve on hover , etc, (read tkinter doc about that)
TODO : better handle of midi inputs and audio
TODO: choice of midi interface
TODO: option menu
TODO : refactor gameplays modes

TODO: make separate screens in mode 2 and 3
TOOD : implement recording with the backgroundChord


## Modes:

- EarTraining Note-by-note : Learn single interval
- EarTraining Chords
- EarTraining Record and practise licks

- BackinTrack (only for wav files)


## Structure of midi .json files:

// this section should be moved in another doc in the future
- get a bass note (used for transposition)
- get all note_on notes with their timings
- get all note_off notes with their timings
- store all this


```
{
"info": "",
"bass": 60,
"type": "minor",
"notes": [
		{"note": 40, "type": "note_on", "time": 1234},
		{"note": 40, "type": "note_off", "time": 2234},
	]

```

ulimit -s newvalue pour augmenter le nombre de threads. diminuer newvalue pour avoir plus de threads
aconnect -x  # close all alsa connections 