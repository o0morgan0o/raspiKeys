import random


class MidiChords:
    def __init__(self):
        self.chords = [
            ("min", [0, 3, 7]),
            ("maj", [0, 4, 7]),
            ("dim", [0, 3, 6]),
            ("aug", [0, 4, 8]),
            ("min7", [0, 3, 7, 10]),
            ("m7b5", [0, 3, 6, 10]),
            ("maj7", [0, 4, 7, 11]),
            ("dom7", [0, 4, 7, 10]),
            ('min/1stInv', [0, 4, 9]),
            ('maj/1stInv', [0, 3, 8]),
            ('dim/1stInv', [0, 3, 9]),
            ('aug/1stInv', [0, 4, 8]),
            ('min7/1stInv', [0, 4, 7, 9]),
            ('m7b5/1stInv', [0, 3, 7, 9]),
            ('maj7/1stInv', [0, 3, 7, 8]),
            ('dom7/1stInv', [0, 3, 6, 8]),
            ('min/2ndInv', [0, 5, 8]),
            ('maj/2ndInv', [0, 5, 9]),
            ('dim/2ndInv', [0, 6, 9]),
            ('aug/2ndInv', [0, 4, 8]),
            ('min7/2ndInv', [0, 3, 5, 8]),
            ('m7b5/2ndInv', [0, 4, 6, 9]),
            ('maj7/2ndInv', [0, 4, 5, 9]),
            ('dom7/2ndInv', [0, 3, 5, 9]),
            ('min/3rdInv', [0, 3, 7]),
            ('maj/3rdInv', [0, 4, 7]),
            ('dim/3rdInv', [0, 3, 6]),
            ('aug/3rdInv', [0, 4, 8]),
            ('min7/3rdInv', [0, 2, 5, 9]),
            ('m7b5/3rdInv', [0, 2, 5, 8]),
            ('maj7/3rdInv', [0, 1, 5, 8]),
            ('dom7/3rdInv', [0, 2, 6, 9]),
            ('min9', [0, 3, 7, 10, 14]),
            ('maj9', [0, 4, 7, 11, 14]),
            ('dom9', [0, 4, 7, 10, 14]),
            ('m9b5', [0, 3, 6, 10, 13]),
            ('min9/1stInv', [0, 4, 7, 9, 11]),
            ('maj9/1stInv', [0, 3, 7, 8, 10]),
            ('dom9/1stInv', [0, 3, 6, 8, 10]),
            ('min9/2ndInv', [0, 3, 5, 7, 8]),
            ('maj9/2ndInv', [0, 4, 5, 7, 9]),
            ('dom9/2ndInv', [0, 3, 5, 7, 9]),
            ('min9/3rdInv', [0, 2, 4, 5, 9]),
            ('maj9/3rdInv', [0, 1, 3, 5, 8]),
            ('dom9/3rdInv', [0, 2, 4, 6, 9]),
            ('m9b5/1stInv', [0, 3, 7, 9, 10]),
            ('m9b5/2ndInv', [0, 4, 6, 7, 9]),
            ('m9b5/3rdInv', [0, 2, 3, 5, 8]),
            ('alt', [0, 4, 7, 13, 15]),
            ('alt/1stInv', [0, 3, 8, 9, 11]),
            ('alt/2ndInv', [0, 5, 6, 8, 9]),
            ('alt/3rdInv', [-1, 0, 2, 3, 6]),
        ]

    def pickRandom(self):
        size = len(self.chords)
        rand = random.randint(0, size - 1)
        return self.chords[rand]

    @staticmethod
    def get1stInversion(chord_tuple):
        """ Next functions are just an util for having chord inversions before hard-coding. They are not used outside of dev context"""
        name = chord_tuple[0]
        name += "/1stInv"
        chord = chord_tuple[1]
        newChord = chord[1:]
        init = newChord[0]
        for i in range(len(newChord)):
            newChord[i] = newChord[i] - init

        lastInterval = 12 - chord[-1]
        end = newChord[-1] + lastInterval

        newChord.append(end)
        return name, newChord

    def get2ndInversion(self, chord_tuple):
        name = chord_tuple[0]
        name += "/2ndInv"
        tmp = self.get1stInversion(chord_tuple)
        chord = self.get1stInversion(tmp)
        return name, chord[1]

    def get3rdInversion(self, chord_tuple):
        name = chord_tuple[0]
        name += "/3rdInv"
        tmp = self.get2ndInversion(chord_tuple)
        chord = self.get1stInversion(tmp)
        return name, chord[1]

    def printAllInversion(self):
        tmpChords = [
            ("alt", [0, 4, 7, 13, 15]),
        ]
        for chord in tmpChords:
            ch = self.get1stInversion(chord)
            a = ch[0]
            b = ch[1]
            b.sort()
            cc = (a, b)
            # print (cc)

        for chord in tmpChords:
            ch = self.get2ndInversion(chord)
            a = ch[0]
            b = ch[1]
            b.sort()
            cc = (a, b)
            # print (cc)
        for chord in tmpChords:
            ch = self.get3rdInversion(chord)
            a = ch[0]
            b = ch[1]
            b.sort()
            cc = (a, b)
            # print (cc)
