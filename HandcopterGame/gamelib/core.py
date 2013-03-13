public Class Core{ 

while playing
    if no more events on queue then
        DrawObjects() #Reload the screen
    end if
    SearchForEvents() #Search for expired timers
    if events in line then
        #Update objects' position and/or acquire...
        ProcessEvents() #... camera information
        CollisionTesting()  #Ceck for collisions
        if attempts <= 0 then
            playing = false
        end if
    end if
end while

}