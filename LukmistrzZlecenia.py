from System.Collections.Generic import List
import CraftBase
 
#------------------
# user customization here:
bookOfFilled = 0xffffffff

resourcesContainer = 0x402AD05C

retryCraftUponProductFailure = False # True  False

#------------------
bodGumpType =  1009311217
bookGumpType = 1036400804
#------------------
def start():

    bulkItems = findItemsInContainer(0x2258, Player.Backpack)
    
    bulks = []
    for bulkItem in bulkItems:
        bulks.append(BOD.createFromItem(bulkItem))
        
    [bulksItemsExp, bulksItemsNorm] = sortBulkItemsByExceptional(bulkItems)
    #return
    
    for bulkItem in bulkItems:
        Misc.SendMessage('jest zlecenie: ' + str(bulkItem.Serial), 66)

        fillBODItem(bulkItem)
        Misc.Pause(100)
    
    Misc.Pause(1000)

def sortBulkItemsByExceptional(bulkItems):
    exp = []
    norm = []
    for bulkItem in bulkItems:
        bod = BOD.createFromItem(bulkItem)
        if bod.exceptional:
            exp.append(bulkItem)
        else:
            norm.append(bulkItem)
            
    Misc.SendMessage('exp: ' + str(len(exp)), 66)
    return [exp, norm]
    
def fillBODItem(bodItem):
    for i in range(1):
        bod = BOD.createFromItem(bodItem)
        
        recycleNonExceptional(bod)
        
        if bod.isFilled():
            Misc.SendMessage('Item ' + str(bodItem.Serial) + ' juz wypelnione ' + bod.toString())
            #putBODIntoBook(bodItem, bookOfFilled)
            return
        if fillBOD(bod):
            Misc.SendMessage('Item ' + str(bodItem.Serial) + ' wypelnilem! ' + bod.toString())
            break
        else:
            Misc.SendMessage('Item ' + str(bodItem.Serial) + ' nie wypelnilem ' + bod.toString())

            bod = BOD.createFromItem(bodItem)
            
            fillBOD(bod) # sprobuj wypelnic zanim zrobisz
            recycleNonExceptional(bod)
            
            missingAmount = bod.quantityMax - bod.quantityCurrent
            craftItems(bod.getProductItemID(), missingAmount, bod.exceptional)
            Misc.SendMessage('wypelniam stworzonymi...')
            if not fillBOD(bod):
                fillBOD(bod) # again
                
            recycleNonExceptional(bod)
        
    #putBODIntoBook(bodItem, bookOfFilled)  
        
def putBODIntoBook(bodItem, bookItem):
    Items.Move(bodItem, bookOfFilled, 0)
    Gumps.WaitForGump(bookGumpType, 5000)
    Gumps.SendAction(bookGumpType, 0)
    
def fillBOD(bod):
    productsContainer = Player.Backpack
    
    Misc.SendMessage('BOD: ' + bod.toString())
    products = findProductsForBOD(bod, productsContainer)
    if len(products) == 0:
        return
        
    Gumps.WaitForGump(bodGumpType, 100)
    Gumps.SendAction(bodGumpType, 1)   # exit gump

    Items.UseItem(bod.tiedItem)
    Gumps.WaitForGump(bodGumpType, 3000)
    Gumps.SendAction(bodGumpType, 2)
    
    productNumber = 0
    for product in products:
        productNumber += 1
        if productNumber > bod.quantityMax:
            break
        
        #Misc.SendMessage(str(productNumber) + ' BOD filling with product: ' + str(product.Serial))

        # Just in case:
        if not Gumps.LastGumpTextExist('Polacz zamowienie z przedmiotem'):
            Items.UseItem(bod.tiedItem)
            Gumps.WaitForGump(bodGumpType, 3000)
            Gumps.SendAction(bodGumpType, 2)
        
        Target.WaitForTarget(2000, False)
        Journal.Clear()
        Timer.Create('antiHang', 4000)
        Target.TargetExecute(product)
        
        while True and Timer.Check('antiHang'):    
            Misc.Pause(100)
            if Journal.SearchByName('Przedmiot zostal polaczony z zamowieniem', 'System'):
                #Misc.SendMessage(str(productNumber) + ' Succesfully added product ' + str(product.Serial))
                Gumps.SendAction(bodGumpType, 2)
                break
            elif Journal.SearchByName('Niewlasciwy przedmiot', 'System'):
                #Misc.SendMessage(str(productNumber) + ' Ignoring wrong product type ' + str(product.Serial))
                Gumps.SendAction(bodGumpType, 2)
                break
            elif Journal.SearchByName('Musisz miec przedmiot w plecaku', 'System'):
                #Misc.SendMessage(str(productNumber) + ' Ignoring product outside backpack ' + str(product.Serial))
                Gumps.SendAction(bodGumpType, 2)
                break
            elif Journal.SearchByName('zostala juz polaczona maksymalna ilosc przedmiotow', 'System'):
                #Gumps.SendAction(bodGumpType, 2)
                break
                
    Gumps.WaitForGump(bodGumpType, 1500)
    Gumps.SendAction(bodGumpType, 1)
    Target.Cancel()
    
    Misc.Pause(300)
    bodAfter = BOD.createFromItem(bod.tiedItem)
    Misc.SendMessage('BOD: ' + bod.toString(), 65)
    
    return bodAfter.isFilled()

def recycleNonExceptional(bod):
    if not bod.exceptional:
        Misc.SendMessage('zlecenie normalne')
        return True
    
    products = findProductsForBODRegardlessExceptional(bod, Player.Backpack)
    Misc.SendMessage('produktow w plecaku: '+str(len(products)))
    normalProducts = []
    for product in products:
        isNormal = True
        props = Items.GetPropStringList(product)
        for prop in props:
            p = prop.lower()
            if 'wyjatkowej jakosci' in p:
                isNormal = False
                break
        if isNormal:
            normalProducts.append(product)
            
    Misc.SendMessage('normalnych w plecaku: '+str(len(normalProducts)))
    
    craftSystem = CraftSystem.createFromProductId(bod.getProductItemID())            
    tool = getTool(craftSystem)
    #Items.UseItem(tool)

    for product in normalProducts:
        Gumps.WaitForGump(2066278152, 2500)
        if not Gumps.HasGump():
            Items.UseItem(tool)
            Gumps.WaitForGump(2066278152, 2500)
        Gumps.SendAction(2066278152, 14)
        Target.WaitForTarget(2500, False)
        Target.TargetExecute(product)
        Misc.Pause(200)

def findProductsForBODRegardlessExceptional(bod, container):
    products = findItemsInContainer(bod.getProductItemID(), container)
    #Misc.SendMessage('Number of candidate products: ' + str(len(products)))
    suitableProducts = []
    for product in products:
        if bod.matchesTypeAndResource(product):
            suitableProducts.append(product)
    #Misc.SendMessage('Number of suitable products:  ' + str(len(suitableProducts)))
    return suitableProducts
        
def findProductsForBOD(bod, container):
    products = findItemsInContainer(bod.getProductItemID(), container)
    Misc.SendMessage('Number of candidate products: ' + str(len(products)))
    suitableProducts = []
    for product in products:
        if bod.acceptsProductItem(product):
            suitableProducts.append(product)
    Misc.SendMessage('Number of suitable products:  ' + str(len(suitableProducts)))
    return suitableProducts
    
def findItemsInContainer(itemID, container):
    #Misc.SendMessage('searching container ' + str(container.Serial))
    f = Items.Filter()
    f.Enabled = True
    f.Graphics = List[int]([itemID])
    foundList = Items.ApplyFilter(f)
    result = []
    for item in foundList:
        if item.Container == container.Serial:
            result.append(item)
    return result

def craftTool(craftSystem, useUponCreation = True):

    container = Items.FindBySerial(resourcesContainer)
    if container == None:
        Misc.SendMessage('Nie widze pojemnika z surowcami.')
        return None
    Items.UseItem(container)
    Misc.Pause(500)
    
    containerResource = Items.FindByID(0x1BF2, 0, resourcesContainer)
    backpackResource = Items.FindByID(0x1BF2, 0, Player.Backpack.Serial) # ingot
    originalBackpackResourceAmount = 0
    if backpackResource != None:
        originalBackpackResourceAmount = backpackResource.Amount
    
    requiredAmount = 30
    
    # nie uwzgledniaj obecnego w plecaku metalu, bo braknie do kowalstwa
    #if backpackResource != None:
    #    if backpackResource.Amount >= requiredAmount:
    #        requiredAmount -= backpackResource.Amount

    if containerResource == None:
        Misc.SendMessage('Nie widze surowcow 1 w pojemniku.')
        return None
    if containerResource.Amount < requiredAmount:
        Misc.SendMessage('Za malo surowca 1 w pojemniku.')
        return None

    if requiredAmount > 0:
        Items.Move(containerResource, Player.Backpack, requiredAmount)
        Misc.Pause(600)
    
    tinkerToolId = 0x1EB8
    tinkerGumpId = 2066278152
    newTool = None
    while newTool == None:
        tinkerTool = Items.FindByID(tinkerToolId, -1, Player.Backpack.Serial)
        if tinkerTool != None:
            #Misc.Pause(500)
            Gumps.SendAction(tinkerGumpId, 0)
            Misc.Pause(500)
            Items.UseItem(tinkerTool)
            #while True:
            Gumps.WaitForGump(tinkerGumpId, 3000)
            Gumps.SendAction(tinkerGumpId, 8) # grupa: narzedzia
            Gumps.WaitForGump(tinkerGumpId, 3000)
            Misc.SendMessage('Probuje zrobic narzedzie... gump: ' + str(craftSystem.getTinkerGumpAction()))
            Gumps.SendAction(tinkerGumpId, craftSystem.getTinkerGumpAction())
            Misc.Pause(300)
            Timer.Create('waitForCraftFinish', 3000)
            while Timer.Check('waitForCraftFinish'):
                newTool = Items.FindByID(craftSystem.getTinkeredToolId(), -1, Player.Backpack.Serial)
                if newTool != None:
                    Gumps.WaitForGump(tinkerGumpId, 1000)
                    Gumps.SendAction(tinkerGumpId, 0)      # close gump
                    Misc.Pause(200)
                    if useUponCreation:
                        Items.UseItem(newTool)
                    #return newTool
                Misc.Pause(100)
                
        else:
            Misc.SendMessage('Nie mam narzedzi majstra!', 1122)
            Misc.Pause(2000)
    
    containerResource = Items.FindByID(0x1BF2, 0, resourcesContainer)
    backpackResource = Items.FindByID(0x1BF2, 0, Player.Backpack.Serial)
    containerReturnAmount = backpackResource.Amount - originalBackpackResourceAmount
    Misc.SendMessage('containerReturnAmount='+str(containerReturnAmount)+', backpackResourceAmount='+str(backpackResource.Amount)+', originalBackpackResourceAmount='+str(originalBackpackResourceAmount))
    if containerReturnAmount > 0:
        Items.Move(backpackResource, containerResource, containerReturnAmount)
    
    return newTool   
    
def craftItems(itemId, amount, exceptional):
    Misc.SendMessage('Tworze ' + str(amount) + ' produktow: ' + str(itemId))
    if amount < 1:
        return
    craftSystem = CraftSystem.createFromProductId(itemId)
    if not craftSystem.isProper():
        Misc.SendMessage('Nie umiem zrobic itemka o ID: ' + str(itemId))
        Misc.Pause(100)
        return
    if not craftSystem.producesItemId(itemId):  # double check
        Misc.SendMessage('(2) Nie umiem zrobic itemka o ID: ' + str(itemId))
        Misc.Pause(100)
        return

    backpackItemsAmount = len(Player.Backpack.Contains)
    Misc.SendMessage('Ilosc rzeczy w plecaku: ' + str(backpackItemsAmount))
    if backpackItemsAmount >= ( 125 - amount - 1 ):
        Misc.SendMessage('Za malo miejsca w plecaku! ('+str(backpackItemsAmount)+'/125)', 1100)
        return
        
    tool = getTool(craftSystem)
    if tool == None:
        Misc.SendMessage('Nie potrafie zdobyc narzedzia')
        return
    Misc.SendMessage('Robimy!')
    
    fetchResourcesForProducts(craftSystem, itemId, amount)
    Misc.Pause(500)
    
    firstTimeCraft = True

    #for i in range(amount):
    i = 0
    while True:
        i += 1
        if i > amount:
            break
        Misc.SendMessage('Robimy i='+str(i))
        gumpId = 2066278152
        Gumps.WaitForGump(gumpId, 3000)
        oldProducts = findItemsInContainer(itemId, Player.Backpack)
        products = []
        Journal.Clear()
        if firstTimeCraft:
            group = craftSystem.getGumpCategoryActionForItemId(itemId)
            Misc.SendMessage('gump group: ' + str(group))
            Gumps.SendAction(gumpId, group)
            Gumps.WaitForGump(gumpId, 3000)
            #Misc.Pause(500)
            #Gumps.SendAction(gumpId, group) # again, just in case
            #Gumps.WaitForGump(gumpId, 3000) # again, just in case
            #Misc.Pause(500)
            Gumps.SendAction(gumpId, craftSystem.getGumpProductActionForItemId(itemId))
        else:
            Gumps.SendAction(2066278152, 21) # create last
        Misc.Pause(300)
        Timer.Create('waitForCraftFinish', 3000)
        while Timer.Check('waitForCraftFinish'):
            if Journal.SearchByName('Narzedzie zuzylo sie', 'System'):
                Misc.SendMessage('Zuzyto narzedze.')
                tool = getTool(craftSystem)
                if tool == None:
                    Misc.SendMessage('Nie potrafie zdobyc kolejnego narzedzia')
                    return
            products = findItemsInContainer(itemId, Player.Backpack)
            if len(products) > len(oldProducts):
                Misc.SendMessage('Stworzony.')
                firstTimeCraft = False
                break
            if Gumps.CurrentGump() == 2066278152:
                Misc.SendMessage('Zaszlo tworzenie.')
                break
            Misc.Pause(100)
            
        Misc.Pause(100)
        if Journal.SearchByName('Narzedzie zuzylo sie', 'System'):
            Misc.SendMessage('Zuzyto narzedze (2).')
            tool = getTool(craftSystem)
            if tool == None:
                Misc.SendMessage('Nie potrafie zdobyc kolejnego narzedzia')
                return

        if len(products) >= amount:
            Misc.SendMessage('W plecaku jest '+str(amount)+' produktow, koniec tworzenia.')
            break
                
        if len(products) <= len(oldProducts):
            if retryCraftUponProductFailure:
                Misc.SendMessage('Nie stworzony. Probuj ponownie.', 1100)
                i -= 1
            else:
                Misc.SendMessage('Nie stworzony. Trudno.', 1100)
                # nie probuj ponownie, bo braknie surowcow (nie ma 100% szansy na stworzenie luku/kuszy)

def fetchResourcesForProducts(craftSystem, productId, amount):

    resource1Id = craftSystem.getResource1IdForProduct(productId)[0]
    resource1Hue = craftSystem.getResource1HueForProduct(productId)
    resource1RequiredAmount = craftSystem.getResource1AmountForProduct(productId) * amount

    #resource2Id = craftSystem.getResource2IdForProduct(productId)[0]
    #resource2Hue = craftSystem.getResource2HueForProduct(productId)
    #resource2RequiredAmount = craftSystem.getResource2AmountForProduct(productId) * amount
    
    return fetchResources(resource1Id, resource1Hue, resource1RequiredAmount) #and fetchResources(resource2Id, resource2Hue, resource2RequiredAmount)


def fetchResources(resourceId, resourceHue, resourceRequiredAmount):
    container = Items.FindBySerial(resourcesContainer)
    if container == None:
        Misc.SendMessage('Nie widze pojemnika z surowcami.')
        return False
    Items.UseItem(container)
    Misc.Pause(500)

    backpackResource = Items.FindByID(resourceId, resourceHue, Player.Backpack.Serial)
    containerResource = Items.FindByID(resourceId, resourceHue, resourcesContainer)

    if backpackResource != None:
        if backpackResource.Amount >= resourceRequiredAmount:
            return True
        resourceRequiredAmount -= backpackResource.Amount
    Misc.SendMessage('Pobieram surowiec: '+str(resourceRequiredAmount)+' (hue: '+str(resourceHue)+')')

    if containerResource == None:
       Misc.SendMessage('Nie widze surowcowca 1 w pojemniku.')
       return False
    if containerResource.Amount < resourceRequiredAmount:
       Misc.SendMessage('Za malo surowca 1 w pojemniku.')
       return False

    Items.Move(containerResource, Player.Backpack, resourceRequiredAmount)
    return True
    
def getTool(craftSystem):
    tool = None
    
    tool = Player.GetItemOnLayer('RightHand')
    if tool != None:
        Misc.SendMessage('Bron w reku uzyje jako narzedzia', 99)
        return tool
    
    for toolId in craftSystem.getToolIds():
        tool = Items.FindByID(toolId, -1, Player.Backpack.Serial)
        if tool != None:
            Misc.SendMessage('Znalazlem narzedzie w plecaku')
            Items.UseItem(tool)
            break
    if tool == None:
        Misc.SendMessage('Nie mam narzedzi dla ' + craftSystem.skill + ' - stworze je')
        tool = craftTool(craftSystem)
    return tool

#========================================================================================


class CraftSystem(object):
    def __init__(self, skill='?'):
        self.skill = skill
    
    @staticmethod
    def createFromSkill(sk):
        if sk == 'Tailor':
            return Tailor()
        elif sk == 'Fletcher':
            return Fletcher()
        elif sk == 'Blacksmith':
            return Blacksmith()
        Misc.SendMessage('createFromSkill(' + sk + ') - nieobslugiwana nazwa skilla')
        return CraftSystem() # dummy
    
    @staticmethod
    def createFromProductId(itemId):
        sys = Tailor()
        if sys.producesItemId(itemId):
            return sys
        sys = Fletcher()
        if sys.producesItemId(itemId):
            return sys
        sys = Blacksmith()
        if sys.producesItemId(itemId):
            return sys
            Misc.SendMessage('createFromProductId(' + str(itemId) + ') - nieobslugiwany itemID')
        return CraftSystem() # dummy
    
    def getToolIds(self):
        return []
    
    def getTinkeredToolId(self):
        return -1
        
    def getTinkerGumpAction(self):
        return -1
        
    def getGumpCategoryActionForItemId(self, itemId):
        return -1
        
    def getGumpProductActionForItemId(self, itemId):
        return -1
    
    def producesItemId(self, itemId):
        return False
        
    def getResource1IdForProduct(self, itemId):
        return 0xffffffff
        
    def getResource2IdForProduct(self, itemId):
        return 0xffffffff
        
    def getResource1HueForProduct(self, itemId):
        return 0xffffffff
        
    def getResource2HueForProduct(self, itemId):
        return 0xffffffff
        
    def getResource1AmountForProduct(self, itemId):
        return 0
        
    def getResource2AmountForProduct(self, itemId):
        return 0
        
    def isProper(self):
        return False

class Tailor(CraftSystem):
    def __init__(self):
        super(Tailor, self).__init__('Tailor')
        self.gump = CraftBase.tailorGumpByProductId
        self.resource1IdByProductId = CraftBase.resource1IdByProductId
        self.resource2IdByProductId = CraftBase.resource2IdByProductId
        self.resource1HueByProductId = CraftBase.resource1HueByProductId
        self.resource2HueByProductId = CraftBase.resource2HueByProductId
        self.resource1AmountByProductId = CraftBase.tailorResource1AmountByProductId

    def getToolIds(self):
        return [0x0F9D]
    
    def getTinkeredToolId(self):
        return 0x0F9D
        
    def getTinkerGumpAction(self):
        return 51

    def getGumpCategoryActionForItemId(self, itemId):
        if itemId in self.gump.keys():
            return self.gump[itemId][0]
        return -1
        
    def getGumpProductActionForItemId(self, itemId):
        if itemId in self.gump.keys():
            return self.gump[itemId][1]
        return -1
    
    def producesItemId(self, itemId):
        if itemId in self.gump.keys():
            Misc.SendMessage('Tailor produces: ' + str(itemId))
            return True
        else:
            Misc.SendMessage('Tailor doesn\'t produce: ' + str(itemId))
            return False
        
    def getResource1IdForProduct(self, itemId):
        if itemId in self.resource1IdByProductId.keys():
            return self.resource1IdByProductId[itemId]
        else:
            Misc.SendMessage('Tailor resource1 unknown for product: ' + str(itemId), 1100)
            return 0xffffffff
        
    def getResource2IdForProduct(self, itemId):
        if itemId in self.resource2IdByProductId.keys():
            return self.resource2IdByProductId[itemId]
        else:
            Misc.SendMessage('Tailor resource2 unknown for product: ' + str(itemId), 1100)
            return 0xffffffff
        
    def getResource1HueForProduct(self, itemId):
        if itemId in self.resource1HueByProductId.keys():
            return self.resource1HueByProductId[itemId]
        else:
            Misc.SendMessage('Tailor hue1 unknown for product: ' + str(itemId), 1100)
            return 0xffffffff
        
    def getResource2HueForProduct(self, itemId):
        if itemId in self.resource2HueByProductId.keys():
            return self.resource2HueByProductId[itemId]
        else:
            Misc.SendMessage('Tailor hue2 unknown for product: ' + str(itemId), 1100)
            return 0xffffffff
        
    def getResource1AmountForProduct(self, itemId):
        if itemId in self.resource1AmountByProductId.keys():
            return self.resource1AmountByProductId[itemId]
        else:
            Misc.SendMessage('Tailor amount1 unknown for product: ' + str(itemId), 1100)
            return 0xffffffff
        
    def getResource2AmountForProduct(self, itemId):
        return 0
        
    def isProper(self):
        return True

class Fletcher(CraftSystem):
    def __init__(self):
        super(Fletcher, self).__init__('Fletcher')
        self.gump = CraftBase.fletcherGumpByProductId
        self.resource1IdByProductId = CraftBase.resource1IdByProductId
        self.resource2IdByProductId = CraftBase.resource2IdByProductId
        self.resource1HueByProductId = CraftBase.resource1HueByProductId
        self.resource2HueByProductId = CraftBase.resource2HueByProductId
        self.resource1AmountByProductId = CraftBase.fletcherResource1AmountByProductId
        self.resource2AmountByProductId = CraftBase.fletcherResource2AmountByProductId

    def getToolIds(self):
        return [0x1022]
    
    def getTinkeredToolId(self):
        return 0x1022
        
    def getTinkerGumpAction(self):
        return 149
        
    def getGumpCategoryActionForItemId(self, itemId):
        if itemId in self.gump.keys():
            return self.gump[itemId][0]
        return -1
        
    def getGumpProductActionForItemId(self, itemId):
        if itemId in self.gump.keys():
            return self.gump[itemId][1]
        return -1
    
    def producesItemId(self, itemId):
        if itemId in self.gump.keys():
            Misc.SendMessage('Fletcher produces: ' + str(itemId))
            return True
        else:
            Misc.SendMessage('Fletcher doesn\'t produce: ' + str(itemId))
            return False
        
    def getResource1IdForProduct(self, itemId):
        if itemId in self.resource1IdByProductId.keys():
            return self.resource1IdByProductId[itemId]
        else:
            Misc.SendMessage('Fletcher resource1 unknown for product: ' + str(itemId), 1100)
            return 0xffffffff
        
    def getResource2IdForProduct(self, itemId):
        if itemId in self.resource2IdByProductId.keys():
            return self.resource2IdByProductId[itemId]
        else:
            Misc.SendMessage('Fletcher resource2 unknown for product: ' + str(itemId), 1100)
            return 0xffffffff
        
    def getResource1HueForProduct(self, itemId):
        if itemId in self.resource1HueByProductId.keys():
            return self.resource1HueByProductId[itemId]
        else:
            Misc.SendMessage('Fletcher hue1 unknown for product: ' + str(itemId), 1100)
            return 0xffffffff
        
    def getResource2HueForProduct(self, itemId):
        if itemId in self.resource2HueByProductId.keys():
            return self.resource2HueByProductId[itemId]
        else:
            Misc.SendMessage('Fletcher hue2 unknown for product: ' + str(itemId), 1100)
            return 0xffffffff
        
    def getResource1AmountForProduct(self, itemId):
        if itemId in self.resource1AmountByProductId.keys():
            return self.resource1AmountByProductId[itemId]
        else:
            Misc.SendMessage('Fletcher amount1 unknown for product: ' + str(itemId), 1100)
            return 0xffffffff
        
    def getResource2AmountForProduct(self, itemId):
        if itemId in self.resource2AmountByProductId.keys():
            return self.resource2AmountByProductId[itemId]
        else:
            Misc.SendMessage('Fletcher amount2 unknown for product: ' + str(itemId), 1100)
            return 0xffffffff
        
    def isProper(self):
        return True

class Blacksmith(CraftSystem):
    def __init__(self):
        super(Blacksmith, self).__init__('Blacksmith')
        self.gump = CraftBase.blacksmithGumpByProductId
        self.resource1IdByProductId = CraftBase.resource1IdByProductId
        self.resource2IdByProductId = CraftBase.resource2IdByProductId
        self.resource1HueByProductId = CraftBase.resource1HueByProductId
        self.resource2HueByProductId = CraftBase.resource2HueByProductId
        self.resource1AmountByProductId = CraftBase.blacksmithResource1AmountByProductId
        self.resource2AmountByProductId = CraftBase.blacksmithResource2AmountByProductId

    def getToolIds(self):
        return [0x0FBB, 0x13E3]
    
    def getTinkeredToolId(self):
        return 0x0FBB  # 0x13E3=mlotek,   0x0FBB=szczypce
        
    def getTinkerGumpAction(self):
        return 93   # 100=mlotek 93=szczypce
        
    def getGumpCategoryActionForItemId(self, itemId):
        if itemId in self.gump.keys():
            return self.gump[itemId][0]
        return -1
        
    def getGumpProductActionForItemId(self, itemId):
        if itemId in self.gump.keys():
            return self.gump[itemId][1]
        return -1
    
    def producesItemId(self, itemId):
        if itemId in self.gump.keys():
            Misc.SendMessage('Blacksmith produces: ' + str(itemId))
            return True
        else:
            Misc.SendMessage('Blacksmith doesn\'t produce: ' + str(itemId))
            return False
        
    def getResource1IdForProduct(self, itemId):
        if itemId in self.resource1IdByProductId.keys():
            return self.resource1IdByProductId[itemId]
        else:
            Misc.SendMessage('Blacksmith resource1 unknown for product: ' + str(itemId), 1100)
            return 0xffffffff
        
    def getResource2IdForProduct(self, itemId):
        if itemId in self.resource2IdByProductId.keys():
            return self.resource2IdByProductId[itemId]
        else:
            Misc.SendMessage('Blacksmith resource2 unknown for product: ' + str(itemId), 1100)
            return 0xffffffff
        
    def getResource1HueForProduct(self, itemId):
        if itemId in self.resource1HueByProductId.keys():
            return self.resource1HueByProductId[itemId]
        else:
            Misc.SendMessage('Blacksmith hue1 unknown for product: ' + str(itemId), 1100)
            return 0xffffffff
        
    def getResource2HueForProduct(self, itemId):
        if itemId in self.resource2HueByProductId.keys():
            return self.resource2HueByProductId[itemId]
        else:
            Misc.SendMessage('Blacksmith hue2 unknown for product: ' + str(itemId), 1100)
            return 0xffffffff
        
    def getResource1AmountForProduct(self, itemId):
        if itemId in self.resource1AmountByProductId.keys():
            return self.resource1AmountByProductId[itemId]
        else:
            Misc.SendMessage('Blacksmith amount1 unknown for product: ' + str(itemId), 1100)
            return 0xffffffff
        
    def getResource2AmountForProduct(self, itemId):
        if itemId in self.resource2AmountByProductId.keys():
            return self.resource2AmountByProductId[itemId]
        else:
            Misc.SendMessage('Blacksmith amount2 unknown for product: ' + str(itemId), 1100)
            return 0xffffffff
        
    def isProper(self):
        return True

#========================================================================================

class BOD(object):
    def __init__(self, tiedItem=0, skill='?', product='?', quantityCurrent=0, quantityMax=0, exceptional=False, small=True, resource='x', resource2='y'):
        
        self.tiedItem = tiedItem
        self.skill = skill
        self.product = product
        self.quantityCurrent = quantityCurrent
        self.quantityMax = quantityMax
        self.exceptional = exceptional
        self.small = small
        self.resource = resource
        self.resource2 = resource2
        
    @staticmethod
    def createFromItem(item):
        if item.Hue == 0x0591:
            return FletcherBOD.createFromItem(item)
        if item.Hue == 0x0483:
            return TailorBOD.createFromItem(item)
        if item.Hue == 0x044e:
            return BlacksmithBOD.createFromItem(item)
        Misc.SendMessage('nie rozpoznano skilla dla zlecenia', 1100) 
        return BOD() # dummy instance, TODO: other crafting skills support
    
    def getProductItemID(self):
        if self.skill == 'Fletcher':
            return FletcherBOD.getProductItemID(item)
        if self.skill == 'Tailor':
            return TailorBOD.getProductItemID(item)
        if self.skill == 'Blacksmith':
            return BlacksmithBOD.getProductItemID(item)
        return -1 # dummy

    def getProductItemHue(self):
        if self.skill == 'Fletcher':
            return FletcherBOD.getProductItemHue(item)
        if self.skill == 'Tailor':
            return TailorBOD.getProductItemHue(item)
        if self.skill == 'Blacksmith':
            return BlacksmithBOD.getProductItemHue(item)
        return -1 # dummy (any hue)
        
    def acceptsProductItem(item):
        if self.skill == 'Fletcher':
            return FletcherBOD.acceptsProductItem(item)
        if self.skill == 'Tailor':
            return TailorBOD.acceptsProductItem(item)
        if self.skill == 'Blacksmith':
            return BlacksmithBOD.acceptsProductItem(item)
        return False # dummy
    
    def matchesTypeAndResource(self, item):
        if self.skill == 'Fletcher':
            return FletcherBOD.matchesTypeAndResource(item)
        if self.skill == 'Tailor':
            return TailorBOD.matchesTypeAndResource(item)
        if self.skill == 'Blacksmith':
            return BlacksmithBOD.matchesTypeAndResource(item)
        Misc.SendMessage('BRAK DEFINICJI matchesTypeAndResource() w '+self.skill, 22)
        return False # dummy
        
    def toString(self):
        return '/'.join([self.skill, self.product, str(self.quantityCurrent), str(self.quantityMax), ('exceptional' if self.exceptional else 'normal'), 'small' if self.small else 'big', self.resource, self.resource2])

    def isFilled(self):
        return self.quantityCurrent == self.quantityMax and self.quantityMax > 0

class FletcherBOD(BOD):
    def __init__(self):
        super(FletcherBOD, self).__init__(0, 'Fletcher')
        
    @staticmethod
    def createFromItem(item):
        props = Items.GetPropStringList(item)
        bod = FletcherBOD()
        bod.tiedItem = item
        bod.small = True
        bod.exceptional = False
        bod.resource = 'RegularWood'
        for prop in props:
            p = prop.lower()
            
            if 'wyjatkowej jakosci' in p:
                bod.exceptional = True

            elif 'z jelitowych cieciw' in p:
                bod.resource2 = 'BowstringGut'
            elif 'ze skorzanych cieciw' in p:
                bod.resource2 = 'BowstringLeather'
            elif 'z jedwabnych cieciw' in p:
                bod.resource2 = 'BowstringSilk'
            elif 'z konopnych cieciw' in p:
                bod.resource2 = 'BowstringCannabis'

            elif 'do zrobienia' in p:
                f = p.find(':')
                if f != -1:
                    bod.quantityMax = int(p[f+2:])
                    
            elif 'musza byc wykonane z ' in p:
                # TODO: support: RegularWood, OakWood, AshWood, YewWood, Heartwood, Bloodwood, Frostwood
                666   

        lastLine = props[len(props)-1].lower()
        f = lastLine.find(':')
        if f != -1:
            bod.quantityCurrent = int(lastLine[f+1:])
            bod.product = lastLine[0:f] # no translation
                
        return bod
        
    def getProductItemID(self):
        IDs = CraftBase.fletcherProductIdByName
        if self.product in IDs.keys():
            return IDs[self.product]
        return -1

    def getProductItemHue(self):
        colors = {
            'RegularWood': 0,
            # 'BowstringLeather': 0x046c,
            # 'BowstringGut': 0x0475
        } # TODO: support all woods, utilize CraftBase
        if self.resource in colors.keys():
            return colors[self.resource]
        return -1
        
    def acceptsProductItem(self, item):
        props = Items.GetPropStringList(item)
        
        productValid = item.ItemID == self.getProductItemID()
        exceptionalValid = not self.exceptional
        resourceValid = item.Hue == self.getProductItemHue()
        resource2Valid = False
        
        for prop in props:
            p = prop.lower()
            if 'wyjatkowej jakosci' in p:
                exceptionalValid = True
            elif 'cieciwa' in p:
                txt = p.split()[1]
                bowstringType = '[undetermined]'
                if txt == 'jelitowa':
                    bowstringType = 'BowstringGut'
                elif txt == 'skorzana':
                    bowstringType = 'BowstringLeather'
                elif txt == 'konopna':
                    bowstringType = 'BowstringCannabis'
                elif txt == 'jedwabna':
                    bowstringType = 'BowstringSilk'
                if bowstringType == self.resource2:
                    resource2Valid = True
   
        return productValid and exceptionalValid and resourceValid and resource2Valid
        
    def matchesTypeAndResource(self, item): # sprawdza czy item pasuje, ale bez uwzgledniania Exceptional
        props = Items.GetPropStringList(item)
        
        productValid = item.ItemID == self.getProductItemID()
        #exceptionalValid = not self.exceptional
        resourceValid = item.Hue == self.getProductItemHue()
        resource2Valid = False
        
        for prop in props:
            p = prop.lower()
            if 'cieciwa' in p:
                txt = p.split()[1]
                bowstringType = '[undetermined]'
                if txt == 'jelitowa':
                    bowstringType = 'BowstringGut'
                elif txt == 'skorzana':
                    bowstringType = 'BowstringLeather'
                elif txt == 'konopna':
                    bowstringType = 'BowstringCannabis'
                elif txt == 'jedwabna':
                    bowstringType = 'BowstringSilk'
                if bowstringType == self.resource2:
                    resource2Valid = True
   
        return productValid and resourceValid and resource2Valid

        
class TailorBOD(BOD):
    def __init__(self):
        super(TailorBOD, self).__init__(0, 'Tailor')
        
    @staticmethod
    def createFromItem(item):
        props = Items.GetPropStringList(item)
        bod = TailorBOD()
        bod.tiedItem = item
        bod.small = True
        bod.exceptional = False
        bod.resource = 'Cloth'      # TODO: recognize the difference between cloth and plain leather
        for prop in props:
            p = prop.lower()
            
            if 'wyjatkowej jakosci' in p:
                bod.exceptional = True

            elif 'z niebieskich skor' in p:
                bod.resource = 'Spined'
            elif 'z czerwonych skor' in p:
                bod.resource = 'Horned'
            elif 'z zielonych skor' in p:
                bod.resource = 'Barbed'

            elif 'do zrobienia' in p:
                f = p.find(':')
                if f != -1:
                    bod.quantityMax = int(p[f+2:])
                    
            elif 'musza byc wykonane z ' in p:
            # zwykla skora lub material
                666   
        
        lastLine = props[len(props)-1].lower()
        f = lastLine.find(':')
        if f != -1:
            bod.quantityCurrent = int(lastLine[f+1:])
            bod.product = lastLine[0:f] # no translation

        return bod
        
    def getProductItemID(self):
        IDs = CraftBase.tailorProductIdByName
        if self.product in IDs.keys():
            return IDs[self.product]
        return -1

    def getProductItemHue(self):
        colors = { 'cloth': -1, 'spined': -1 } # TODO: support  leather colors
        if self.resource in colors.keys():
            return colors[self.resource]
        return -1
        
    def acceptsProductItem(self, item):
        props = Items.GetPropStringList(item)
        #Misc.SendMessage(self.product + ' id=' +str(self.getProductItemHue()))
        
        productValid = item.ItemID == self.getProductItemID()
        exceptionalValid = not self.exceptional
        resourceValid = item.Hue == self.getProductItemHue() or self.getProductItemHue() == -1
        
        for prop in props:
            p = prop.lower()
            if 'wyjatkowej jakosci' in p:
                exceptionalValid = True
   
        return productValid and exceptionalValid and resourceValid

    def matchesTypeAndResource(self, item):
        props = Items.GetPropStringList(item)
        #Misc.SendMessage(self.product + ' id=' +str(self.getProductItemHue()))
        
        productValid = item.ItemID == self.getProductItemID()
        #exceptionalValid = not self.exceptional
        resourceValid = item.Hue == self.getProductItemHue() or self.getProductItemHue() == -1
        
        for prop in props:
            p = prop.lower()
            if 'wyjatkowej jakosci' in p:
                exceptionalValid = True
   
        return productValid and resourceValid
        
class BlacksmithBOD(BOD):
    def __init__(self):
        super(BlacksmithBOD, self).__init__(0, 'Blacksmith')
        
    @staticmethod
    def createFromItem(item):
        props = Items.GetPropStringList(item)
        bod = BlacksmithBOD()
        bod.tiedItem = item
        bod.small = True
        bod.exceptional = False
        bod.resource = 'Iron'
        for prop in props:
            p = prop.lower()
            
            if 'wyjatkowej jakosci' in p:
                bod.exceptional = True

            elif 'sztab matowej' in p:
                bod.resource = 'Dull Copper'
            elif 'sztab shadowa' in p:
                bod.resource = 'Shadow'
            elif 'sztab miedzi' in p:
                bod.resource = 'Copper'
            elif 'sztab brazu' in p:
                bod.resource = 'Bronze'
            elif 'sztab zlota' in p:
                bod.resource = 'Golden'
            elif 'sztab agapitu' in p:
                bod.resource = 'Agapite'
            elif 'sztab verytu' in p:
                bod.resource = 'Verite'
            elif 'sztab valorytu' in p:
                bod.resource = 'Valorite'

            elif 'do zrobienia' in p:
                f = p.find(':')
                if f != -1:
                    bod.quantityMax = int(p[f+2:])

        lastLine = props[len(props)-1].lower()
        f = lastLine.find(':')
        if f != -1:
            bod.quantityCurrent = int(lastLine[f+1:])
            bod.product = lastLine[0:f] # no translation

        return bod
        
    def getProductItemID(self):
        IDs = CraftBase.blacksmithProductIdByName
            
        if self.product in IDs.keys():
            return IDs[self.product]
        return -1

    def getProductItemHue(self):
        colors = {
            'Iron':   0,
            'Shadow': 0x0966,
            'Bronze': 0x0972
            } # TODO: support metal colors
        if self.resource in colors.keys():
            return colors[self.resource]
        return -1
        
    def acceptsProductItem(self, item):
        props = Items.GetPropStringList(item)
        #Misc.SendMessage(self.product + ' id=' +str(self.getProductItemHue()))
        
        productValid = item.ItemID == self.getProductItemID()
        exceptionalValid = not self.exceptional
        resourceValid = item.Hue == self.getProductItemHue() or self.getProductItemHue() == -1
        
        for prop in props:
            p = prop.lower()
            if 'wyjatkowej jakosci' in p:
                exceptionalValid = True
   
        return productValid and exceptionalValid and resourceValid
       
    def matchesTypeAndResource(self, item):
        props = Items.GetPropStringList(item)
        #Misc.SendMessage(self.product + ' id=' +str(self.getProductItemHue()))
        
        productValid = item.ItemID == self.getProductItemID()
        #exceptionalValid = not self.exceptional
        resourceValid = item.Hue == self.getProductItemHue() or self.getProductItemHue() == -1
        
        for prop in props:
            p = prop.lower()
            if 'wyjatkowej jakosci' in p:
                exceptionalValid = True
   
        return productValid and resourceValid
        
start()