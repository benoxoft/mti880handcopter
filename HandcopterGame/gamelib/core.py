class Core(): 
    playing = True
    attempts = 10
    eventsInLine = True

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
                    self.playing = False
    
    def drawObjects(self):
        #draw
        pass
    
    def searchForEvents(self):
        #search
        pass
        
    def processEvents(self):
        #initialise(); % Initialises OpenCV and camera.
        #cvQueryFrame(camera); % Capture one frame.
        #cvCvtColor(CV BGR2HSV); % Image RGB to HSV.
        #cvInRange(min, max); % Only pixels within range.
        #% Finds out external contour.
        #cvFindContours(CV RETR EXTERNAL);
        #if contour 6= null then
        #% Determines CH for the external contour.
        #cvConvexHull2(CV CLOCKWISE);
        #for all convex hull points do
        #% Generates all points from the detected CH.
        #cvSeqPush(sequence, point);
        #end for
        #area = cvContourArea(sequence);
        #end if
        #return area;
        pass
    
    def collisionTesting(self):
        #Collision
        pass
    
    def calibration(self):
        pass
    
    def createNewElement(self):
        pass