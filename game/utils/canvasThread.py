import threading

class MyThread(threading.Thread):
    def __init__(self, name, canvas, audioInstance, totalLength,parent):
        threading.Thread.__init__(self)
        self.parent=parent
        self.audioInstance =audioInstance
        self.canvas = canvas
        self.totalLength =totalLength
        self.name=name
        self.isAlive = True
        self.canvasWidth= 260
        self.canvasHeight= 30
    def run(self):
        while self.isAlive == True:
            timePlayed= self.audioInstance.getTimePlayed()
            if self.audioInstance.checkIsPlayingMusic()== False:
                print("end of recording ...")
                self.isAlive=False
                self.parent.endRecording()
            
            percentage = timePlayed/ self.totalLength
            self.canvas.create_rectangle(0,0, percentage * self.canvasWidth,self.canvasHeight,fill="red" )

class MyThreadForBacktrackScreen(threading.Thread):
    def __init__(self, name, canvas, audioInstance, totalLength,parent):
        threading.Thread.__init__(self)
        self.parent=parent
        self.audioInstance =audioInstance
        self.canvas = canvas
        self.totalLength =totalLength
        self.name=name
        self.isAlive = True
        self.canvasWidth= 340
        self.canvasHeight= 10
        self.nbOfLoops=1
        self.canvas.create_rectangle(0,0,self.canvasWidth, self.canvasHeight, fill="black")
    def run(self):
        while self.isAlive == True:
            timePlayed= self.audioInstance.getTimePlayed()
            if self.audioInstance.checkIsPlayingMusic()== False:
                self.isAlive=False
            
            
            percentage = timePlayed/ self.totalLength
            if percentage // 1 >= self.nbOfLoops:
                self.canvas.create_rectangle(0,0,self.canvasWidth, self.canvasHeight, fill="black")
                self.nbOfLoops+= 1
            
            percentage = ((percentage * 100) % 100)/100
            
            self.canvas.create_rectangle(0,0, percentage * self.canvasWidth,self.canvasHeight,fill="red" )

        self.canvas.create_rectangle(0,0,self.canvasWidth, self.canvasHeight, fill="black")