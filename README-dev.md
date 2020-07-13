# Installation from Blank Raspian

-> Installation of touch screen

```
sudo rm -rf LCD-show
git clone https://github.com/goodtft/LCD-show.git
chmod -R 755 LCD-show
cd LCD-show/
sudo ./LCD35-show
```

-> Rotate screen orientation

```
cd LCD-show/
sudo ./LCD35-show 270
```

-> raspi-config
    ==> activate output on headphones
    ==> activate i2c for screen


-> Libraries to install

1. Mido.
`pip3 install mido`

2. SimpleAudio
`pip3 install simpleaudio`

3. Soundfile
`pip3 install soundfile`

4. pydub
`pip3 install pydub`

5. rtmidi
`pip3 install python-rtmidi --install-option="--no-jack"`

6. xdotool
`pip3 install xdotool`

7. pygame
`pip3 install pygame`
