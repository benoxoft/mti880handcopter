class Core(): 
    playing = 1
    attempts = 10
    eventsInLine = 1

    def __init__(self):
        noMoreEventsOnQueue = 1
        while self.playing :
            if noMoreEventsOnQueue :
                self.DrawObjects() #Reload the screen
            self.SearchForEvents() #Search for expired timers
            if self.eventsInLine :
                #Update objects' position and/or acquire...
                self.ProcessEvents() #... camera information
                self.CollisionTesting()  #Check for collisions
                if self.attempts <= 0 :
                    self.playing = 0
    
    def DrawObjects(self):
        #draw
    
    def SearchForEvents(self):
        #search
        
    def ProcessEvents(self):
        #Process
    
    def CollisionTesting(self):
        #Collision