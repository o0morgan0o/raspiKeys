import tkinter


class DotsAnimations:
    def __init__(self, widget: tkinter.Widget, text_variations: list, delay=300):
        self.isAlive = True
        self.widget = widget
        self.text_variations = text_variations
        self.delay = delay

    def animate(self):
        self.isAlive = True
        self._animate()

    def _animate(self):
        print('animation loop')
        if not self.isAlive:
            return
        if self.widget['text'] == self.text_variations[0]:
            self.widget['text'] = self.text_variations[1]
            self.widget.after(self.delay, self._animate)
        elif self.widget['text'] == self.text_variations[1]:
            self.widget['text'] = self.text_variations[2]
            self.widget.after(self.delay, self._animate)
        elif self.widget['text'] == self.text_variations[2]:
            self.widget['text'] = self.text_variations[3]
            self.widget.after(self.delay, self._animate)
        elif self.widget['text'] == self.text_variations[3]:
            self.widget['text'] = self.text_variations[0]
            self.widget.after(self.delay, self._animate)

    def stop(self):
        self.isAlive = False
