class Core(): 
    playing = 1
    attempts = 10
    eventsInLine = 1

    def __init__(self):
        noMoreEventsOnQueue = 1
        while self.playing :
            if noMoreEventsOnQueue :
                self.drawObjects() #Reload the screen
            self.searchForEvents() #Search for expired timers
            if self.eventsInLine :
                #Update objects' position and/or acquire...
                self.processEvents() #... camera information
                self.collisionTesting()  #Check for collisions
                if self.attempts <= 0 :
                    self.playing = 0
    
    def drawObjects(self):
        #draw
        pass
    
    def searchForEvents(self):
        #search
        pass
        
    def processEvents(self):
        #Process
        pass
    
    def collisionTesting(self):
        #Collision
        pass
    
    def calibration(self):
        pass
    
    def createNewElement(self):
        pass