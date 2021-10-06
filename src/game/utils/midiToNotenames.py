def noteName(midiNum: int) -> str:
    # convert note number to name "A", "B", ...
    num = midiNum % 12
    if num == 0:
        return "C"
    elif num == 1:
        return "C#"
    elif num == 2:
        return "D"
    elif num == 3:
        return "D#"
    elif num == 4:
        return "E"
    elif num == 5:
        return "F"
    elif num == 6:
        return "F#"
    elif num == 7:
        return "G"
    elif num == 8:
        return "G#"
    elif num == 9:
        return "A"
    elif num == 10:
        return "A#"
    elif num == 11:
        return "B"


def noteNameFull(midiNum: int) -> str:
    entier = int(midiNum/12)
    # print(entier)
    key = noteName(midiNum)
    return "{}{}".format(key, str(entier))
