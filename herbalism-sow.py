
# Tasandora brama wschodnia, pole lewe-dolne:
x1=1723
y1=2020
x2=1717
y2=2013

# Tasandora brama wschodnia, pole prawe-dolne:
#x1=1738
#y1=2007
#x2=1730
#y2=2013

# Tasandora brama wschodnia, prawe-gorne:
#x1=1718
#y1=2001
#x2=1726
#y2=1996

seedIDs = [0x18DD, 0x0DCD, 0x18EB, 0x18E7, 0x18E3 ] # id szczepek do sadzenia (tych w plecaku)
seedColors = {0x0DCD: 438 }


seedSowTimeAdditional = 70 # zwiekszyc, jesli makro pomija lokacje (zostawia puste miejsca w grzadce)

seedSowTimeBase = 2250
journalWaitTime = 200

sizeX = abs(x1-x2)+1
sizeY = abs(y1-y2)+1
Misc.SendMessage('Pole '+str(x1)+','+str(y1)+' --> '+str(x2)+','+str(y2))
Misc.SendMessage('Wielkosc '+str(sizeX)+'x'+str(sizeY)+' czyli '+str(sizeX*sizeY)+' krzakow.')

def sowField():
    xFirst = x1
    xStep = 1 if x1 < x2 else -1
    xLast = x2
    yFirst = y1
    yStep = 1 if y1 < y2 else -1
    yLast = y2
    
    for x in range(xFirst, xLast+xStep, xStep):
        [yFirst, yStep, yLast] = [yLast, -yStep, yFirst]
        for y in range(yFirst, yLast+yStep, yStep):
            Misc.SendMessage('pozycja '+str(x)+', '+str(y))
            WalkTo(x,y)
            sowSeed()
 
    Misc.SendMessage('GOTOWE!')

def sowSeed():
    seed = None
    while True:
        Misc.NoOperation()
        seed = getSeed()
        if seed == None:
            Misc.SendMessage('Umiesc szczepki w plecaku', 33)
            Misc.Pause(2000)
        else:
            break
            
    Journal.Clear()
    Items.UseItem(seed) 

    Misc.Pause(journalWaitTime)
    if Journal.Search('W tym miejscu cos juz rosnie'):
        666
    else:
        Misc.Pause((seedSowTimeBase+seedSowTimeAdditional) - journalWaitTime)
    
def getSeed():
    for id in seedIDs:
        color = seedColors[id] if id in seedColors else -1
        seed = Items.FindByID(id, color, Player.Backpack.Serial, 2)
        if seed != None:
            return seed
    
def WalkTo(x,y):
    while Player.Position.X != x or Player.Position.Y != y:
        Misc.NoOperation()
        px = Player.Position.X
        py = Player.Position.Y
        direction = 'kierunek'
        direction = 'Up' if px > x and py > y else direction
        direction = 'West' if px > x and py == y else direction
        direction = 'Left' if px > x and py < y else direction
        direction = 'Right' if px < x and py > y else direction
        direction = 'East' if px < x and py == y else direction
        direction = 'Down' if px < x and py < y else direction
        direction = 'North' if px == x and py > y else direction
        direction = 'South' if px == x and py < y else direction
        if direction:
            Player.Run(direction)
        
sowField()