import tkinter as tk

from src.game.utils.colors import Colors

WHITE_NOTE_STRING = "white_note"
BLACK_NOTE_STRING = "black_note"


class KeyboardCanvasView:
    def __init__(self, game_frame, note_min=0, note_max=127):

        self.canvasDimensions = (200, 100)
        self.octaveMin, self.numberOfOctavesToShow = self.calculateNumberOfOctaveNeeded(note_min, note_max)

        # Values are not important because canvas will be resized as soon as it is packed
        self.octaveWidth = self.canvasDimensions[0] / self.numberOfOctavesToShow
        self.octaveHeight = self.canvasDimensions[1]
        self.whiteNoteRectHeight = self.octaveHeight
        self.blackNoteRectHeight = self.octaveHeight / 2
        self.allWhiteNotes = None
        self.allBlackNotes = None
        self.octaveOffset = 0

        self.gameFrame = game_frame
        self.canvas = tk.Canvas(self.gameFrame, width=self.canvasDimensions[0], height=self.canvasDimensions[1])
        self.canvas.pack(expand=1, side=tk.BOTTOM, fill=tk.BOTH)
        self.octaves = []
        self.drawKeyboard()
        self.canvas.bind("<Configure>", self.onCanvasConfigure)

    def resetAllNotes(self):
        for note in self.allWhiteNotes:
            self.resetNote(note)
        for note in self.allBlackNotes:
            self.resetNote(note)

    def drawKeyboard(self):
        keyboard_origin = (0, 0)
        self.octaveWidth = self.canvasDimensions[0] / self.numberOfOctavesToShow
        self.octaveHeight = self.canvasDimensions[1]
        self.whiteNoteRectHeight = self.octaveHeight
        self.blackNoteRectHeight = self.whiteNoteRectHeight * 2 / 3

        for i in range(0, self.numberOfOctavesToShow):
            self.octaves.append(
                Octave(self.canvas,
                       keyboard_origin=keyboard_origin,
                       octave_number=i,
                       octave_dimensions=(self.octaveWidth, self.octaveHeight)
                       ))
        self.allWhiteNotes = list(self.canvas.find_withtag('white_note'))
        self.allBlackNotes = list(self.canvas.find_withtag('black_note'))

    def resetNote(self, note_number: int):
        try:
            note_to_reset = self.canvas.find_withtag("tag{}".format(note_number - self.octaveOffset))
        except RuntimeError as e:
            return
        if len(note_to_reset) != 1:
            # print("No note find in canvas", note_to_reset)
            return
        note_to_reset = note_to_reset[0]
        # print('searching...', note_to_reset, self.allWhiteNotes, self.allBlackNotes)
        # check it it is a black or white note
        note_color = self.getColorOfNote(note_to_reset, self.allWhiteNotes, self.allBlackNotes)
        if note_color == WHITE_NOTE_STRING:
            self.canvas.itemconfig(note_to_reset, fill='white')
        elif note_color == BLACK_NOTE_STRING:
            self.canvas.itemconfig(note_to_reset, fill='black')

    def lightNote(self, note_number: int):
        try:
            note_to_light = self.canvas.find_withtag("tag{}".format(note_number - self.octaveOffset))
        except RuntimeError as e:
            return
        if len(note_to_light) == 1:
            # We want to map the notes for the first octave, so that we don't need to "move" the canvas
            # note_to_light -= self.octaveOffset
            self.canvas.itemconfig(note_to_light, fill=Colors.KEYBOARD_CANVAS_NOTE_LIGHT)
        else:
            print("SOMETHING BAD, TAG NOT FOUND", note_number, note_to_light)

    def onCanvasConfigure(self, event):
        new_width = event.width
        new_height = event.height
        # print('canvas resize', new_width, new_height)
        self.updateCanvasDimensions(new_width, new_height)

    def updateCanvasDimensions(self, new_canvas_width, new_canvas_height):
        self.canvasDimensions = (new_canvas_width, new_canvas_height)
        # print('previous octave width,', self.octaveWidth)
        self.octaveWidth = self.canvasDimensions[0] / self.numberOfOctavesToShow
        # print("new octave width", self.octaveWidth)
        self.octaveHeight = self.canvasDimensions[1]
        self.whiteNoteRectHeight = self.octaveHeight
        self.blackNoteRectHeight = self.whiteNoteRectHeight * 2 / 3
        for octave in self.octaves:
            # print('updating octave')
            octave.updateOctaveDimensions((self.octaveWidth, self.octaveHeight))

    def updateMinAndMaxNotes(self, note_min, note_max):
        (min_octave, number_of_octaves_needed) = self.calculateNumberOfOctaveNeeded(note_min, note_max)
        self.octaveMin = min_octave
        self.numberOfOctavesToShow = number_of_octaves_needed
        # We update because we changed the number_of_octaves to show. No need to update the canvas size
        self.updateCanvasDimensions(self.canvasDimensions[0], self.canvasDimensions[1])
        # we calculate the offset needed to display each note lighting
        self.octaveOffset = self.octaveMin * 12  # because 12 notes per octave

    @staticmethod
    def getColorOfNote(note_number, all_white_notes, all_black_notes) -> str:
        if note_number in all_white_notes:
            return WHITE_NOTE_STRING
        elif note_number in all_black_notes:
            return BLACK_NOTE_STRING
        else:
            raise Exception("Can't determine black or white note")

    @staticmethod
    def calculateNumberOfOctaveNeeded(min_note, max_note) -> tuple:
        if min_note > max_note:
            raise Exception("min_note must be lower than max_note")
        counter = 1
        min_octave = 0
        max_octave = 0
        while True:
            # print('again', min_note, 12 * counter)
            if min_note < 12 * counter:
                break
            min_octave += 1
            counter += 1
        counter = 1
        while True:
            if max_note < 12 * counter:
                break
            max_octave += 1
            counter += 1
        number_of_octaves_needed = max_octave - min_octave + 1
        # print('result', min_octave, number_of_octaves_needed)
        return min_octave, number_of_octaves_needed

    def destroy(self):
        pass


class Octave:
    def __init__(self, canvas, keyboard_origin, octave_number, octave_dimensions):
        self.keyboardOrigin = keyboard_origin
        self.octaveNumber = octave_number
        self.octaveOrigin = (self.keyboardOrigin[0] + self.octaveNumber * octave_dimensions[0], self.keyboardOrigin[1])
        self.canvas = canvas

        self.whiteNoteRectWidth = octave_dimensions[0] / 7
        self.blackNoteRectWidth = self.whiteNoteRectWidth * 2 / 3
        self.whiteNoteRectHeight = octave_dimensions[1]
        self.blackNoteRectHeight = octave_dimensions[1] * 3 / 5

        self.whiteNotes = []
        self.blackNotes = []
        counter = 0
        mapped_white_notes_values = [0, 2, 4, 5, 7, 9, 11]
        mapped_black_notes_values = [1, 3, 6, 8, 10]
        # print("OCTAVE_CREATION", self.octaveOrigin)
        # Handle of white notes
        for i in range(0, 7):
            note_position_X = self.octaveOrigin[0] + i * self.whiteNoteRectWidth
            note_position_Y = self.octaveOrigin[1]
            self.whiteNotes.append(WhiteNote(
                self.canvas,
                octave_number=self.octaveNumber,
                note_origin=(note_position_X, note_position_Y),
                note_dimensions=(self.whiteNoteRectWidth, self.whiteNoteRectHeight),
                note=mapped_white_notes_values[i]))
        # Handle of blackNotes
        counter = 0
        for i in range(0, 7):
            if i in [1, 2, 4, 5, 6]:
                note_position_X = self.octaveOrigin[0] + i * self.whiteNoteRectWidth - (self.blackNoteRectWidth * .5)
                note_position_Y = self.octaveOrigin[1]
                self.blackNotes.append(BlackNote(
                    self.canvas,
                    octave_number=self.octaveNumber,
                    note_origin=(note_position_X, note_position_Y),
                    note_dimensions=(self.blackNoteRectWidth, self.blackNoteRectHeight),
                    note=mapped_black_notes_values[counter]))
                counter += 1

    def updateOctaveDimensions(self, new_octave_dimensions: tuple):
        # print('previous octave origin', self.octaveOrigin)
        self.octaveOrigin = (self.keyboardOrigin[0] + self.octaveNumber * new_octave_dimensions[0], self.keyboardOrigin[1])
        # print('new octave origin', self.octaveOrigin)
        self.whiteNoteRectWidth = new_octave_dimensions[0] / 7
        self.blackNoteRectWidth = self.whiteNoteRectWidth * 2 / 3
        self.whiteNoteRectHeight = new_octave_dimensions[1]
        self.blackNoteRectHeight = new_octave_dimensions[1] * 3 / 5

        counter = 0
        # print("OCTAVE RESIZE", self.octaveOrigin)

        for whiteNote in self.whiteNotes:
            note_position_X = self.octaveOrigin[0] + counter * self.whiteNoteRectWidth
            note_position_Y = self.octaveOrigin[1]
            whiteNote.updateDimensions(
                note_origin=(note_position_X, note_position_Y),
                note_dimensions=(self.whiteNoteRectWidth, self.whiteNoteRectHeight))
            counter += 1

        counter_index = 0
        counter_values = [1, 2, 4, 5, 6]

        for blackNote in self.blackNotes:
            note_position_X = self.octaveOrigin[0] + counter_values[counter_index] * self.whiteNoteRectWidth - (self.blackNoteRectWidth / 3)
            note_position_Y = self.octaveOrigin[1]
            blackNote.updateDimensions(
                note_origin=(note_position_X, note_position_Y),
                note_dimensions=(self.blackNoteRectWidth, self.blackNoteRectHeight))
            counter_index += 1


class WhiteNote:
    def __init__(self, canvas, octave_number, note_origin, note_dimensions, note: int):
        self.note_rectangle = None
        self.canvas = canvas
        self.octave_number = octave_number
        self.midi_note = note
        self.note_origin = note_origin
        self.note_dimensions = note_dimensions
        self.rect_width = note_dimensions[0]
        self.rect_height = note_dimensions[1]
        self.draw()

    def draw(self):
        self.note_rectangle = self.canvas.create_rectangle(
            self.note_origin[0],
            self.note_origin[1],
            self.note_origin[0] + self.rect_width,
            self.note_origin[1] + self.rect_height,
            fill='white', tags=('tag{}'.format(12 * self.octave_number + self.midi_note), 'white_note'))

    def updateDimensions(self, note_origin: tuple, note_dimensions: tuple):
        self.rect_width = note_dimensions[0]
        self.rect_height = note_dimensions[1]
        self.canvas.coords(self.note_rectangle,
                           note_origin[0],
                           note_origin[1],
                           note_origin[0] + self.rect_width,
                           note_origin[1] + self.rect_height
                           )


class BlackNote:
    def __init__(self, canvas, octave_number, note_origin, note_dimensions, note: int):
        self.note_rectangle = None
        self.canvas = canvas
        self.octave_number = octave_number
        self.midi_note = note
        self.note_origin = note_origin
        self.note_dimensions = note_dimensions
        self.rect_width = note_dimensions[0]
        self.rect_height = note_dimensions[1]
        self.draw()

    def draw(self):
        self.note_rectangle = self.canvas.create_rectangle(
            self.note_origin[0],
            self.note_origin[1],
            self.note_origin[0] + self.rect_width,
            self.note_origin[1] + self.rect_height,
            fill='black', tag=('tag{}'.format(12 * self.octave_number + self.midi_note), 'black_note'))

    def updateDimensions(self, note_origin: tuple, note_dimensions: tuple):
        self.rect_width = note_dimensions[0]
        self.rect_height = note_dimensions[1]
        self.canvas.coords(self.note_rectangle,
                           note_origin[0],
                           note_origin[1],
                           note_origin[0] + self.rect_width,
                           note_origin[1] + self.rect_height
                           )
