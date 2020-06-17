# RaspyKeyz

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
