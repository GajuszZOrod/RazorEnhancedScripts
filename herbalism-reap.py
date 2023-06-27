from System.Collections.Generic import List

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

weedIDs = [ 0x18E2, 0x0F3B, 0x18E0, 0x18E6, 0x18E9 ]


weedReapTimeAdditional = 70 # zwiekszyc, jesli makro pomija lokacje (zostawia puste miejsca w grzadce)

weedReapTimeBase = 2250
journalWaitTime = 200

sizeX = abs(x1-x2)+1
sizeY = abs(y1-y2)+1
Misc.SendMessage('Pole '+str(x1)+','+str(y1)+' --> '+str(x2)+','+str(y2))
Misc.SendMessage('Wielkosc '+str(sizeX)+'x'+str(sizeY)+' czyli '+str(sizeX*sizeY)+' krzakow.')

def harvestField():
    
    xStep = 3 if x1 < x2 else -3
    xFirst = x1 + int(xStep/abs(xStep))
    xLast = x2 + (( 3-sizeX%3 if sizeX%3>0 else 0 ) - 1) * int(xStep/abs(xStep))
    
    yStep = 3 if y1 < y2 else -3
    yFirst = y1 + int(yStep/abs(yStep))
    yLast = y2 + (( 3-sizeY%3 if sizeY%3>0 else 0 ) - 1) * int(yStep/abs(yStep))
    
    Misc.SendMessage('xFirst '+str(xFirst))
    Misc.SendMessage('xLast '+str(xLast))
    Misc.SendMessage('yFirst '+str(yFirst))
    Misc.SendMessage('yLast '+str(yLast))
    for x in range(xFirst, xLast+xStep, xStep):
        for y in range(yFirst, yLast+yStep, yStep):
            Misc.SendMessage('pozycja '+str(x)+', '+str(y))
            WalkTo(x,y)
            if not reap(): # try again
                WalkTo(x,y)
                reap()
                
        [yFirst, yStep, yLast] = [yLast, -yStep, yFirst]
    Misc.SendMessage('GOTOWE!')

def reap():
    Misc.SendMessage('zbieram tutaj')
    f = Items.Filter()
    f.OnGround = 1
    f.RangeMax = 1
    f.Graphics = List[int](weedIDs)
    weeds = Items.ApplyFilter(f)
    Misc.SendMessage('Mam w poblizu '+str(len(weeds))+' krzaczkow.')
    leftovers = False
    for weed in weeds:
        
        while True:
            Misc.NoOperation()
            
            Journal.Clear()
            
            Items.UseItem(weed)
        
            Misc.Pause(journalWaitTime)
            if Journal.Search('Jestes juz czyms zajety'):
                Misc.Pause(500)
                continue
            elif Journal.Search('Nie mozesz zbierac roslin bedac konno'):
                Misc.SendMessage('Zejdz z konia!', 33)
                Misc.Pause(2000)
                continue
            elif Journal.Search('Roslina jest jeszcze niedojrzala'):
                Misc.SendMessage('Niedojrzala roslina, pomijam '+str(weed.Position.X)+','+str(weed.Position.Y), 44)
                break
            elif Journal.Search('Twoja wiedza o tej roslinie jest za mala'):
                Misc.SendMessage('Za malo skilla na rosline, pomijam '+str(weed.Position.X)+','+str(weed.Position.Y), 44)
                break
            else:
                Misc.Pause(weedReapTimeBase+weedReapTimeAdditional - journalWaitTime)
                
                if Journal.Search('Nie udalo ci sie zebrac ziela'):
                    continue
                elif Journal.Search('Udalo ci sie zebrac rosline'):
                    Misc.SendMessage('Krzak zebrany.', 55)
                    break
                else:
                    leftovers = True
                    break
    return not leftovers
    
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
        
harvestField()