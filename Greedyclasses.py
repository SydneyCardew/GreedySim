#Classes for GreedySim

class player: #the player class
    def __init__(self,recklessness,malice,greed,height,gold,party,health,treasures,items,capacity,burden,
                 mitigationEN,mitigationST,mitigationMA,mitigationMY,totalhealth,artefacts):
        self.recklessness = recklessness
        self.malice = malice
        self.greed = greed
        self.height = height
        self.gold = gold
        self.party = party
        self.health = health
        self.treasures = treasures
        self.items = items
        self.capacity = capacity
        self.burden = burden
        self.mitigationEN = mitigationEN
        self.mitigationST = mitigationST
        self.mitigationMA = mitigationMA
        self.mitigationMY = mitigationMY
        self.totalhealth = totalhealth
        self.artefacts = artefacts

    def setburden(self):
        self.burden = len(self.treasures)

    def healthget(self):
        self.totalhealth = sum(self.health)

    def takedamage(self,damage):
        self.damage = damage
        for x in range (damage):
            self.health[self.health.index(max(self.health))] -= 1
        if sum(self.health) <= 0:
            for y in range (len(self.health)):
                self.health[y] = 0


    def selltreasure(self,delveindicator,mastercards):
        soldtreasure = 0
        for loot in self.treasures: # the if/else statements account for the special rule of the Fence
            if mastercards[loot].deck == 'Treasure':
                if delveindicator == 1:
                    if '144' in self.party:
                        self.gold += int(mastercards[loot].delve1[:-1])+5
                        soldtreasure += 1
                    else:
                        self.gold += int(mastercards[loot].delve1[:-1])
                        soldtreasure += 1
                if delveindicator == 2:
                    if '144' in self.party:
                        self.gold += int(mastercards[loot].delve1[:-1])+10
                        soldtreasure += 1
                    else:
                        self.gold += int(mastercards[loot].delve2[:-1])
                        soldtreasure += 1
                if delveindicator == 3:
                    if '144' in self.party:
                        self.gold += int(mastercards[loot].delve1[:-1])+15
                        soldtreasure += 1
                    else:
                        self.gold += int(mastercards[loot].delve3[:-1])
                        soldtreasure += 1
            elif mastercards[loot].deck == 'Artefact':
                self.artefacts.append(self.treasures.pop(self.treasures.index(loot)))
        return soldtreasure

    def statset(self,mastercards):
        self.capacity = 0
        self.mitigationEN = 0
        self.mitigationST = 0
        self.mitigationMA = 0
        self.mitigationMY = 0
        self.capacity += sum(self.health)
        if '143' in self.party: #Extra treasure for Quartermaster
            self.capacity += 1
        for x in self.party:
            if x == '121': #'Lucky' Dhorzan
                self.mitigationEN += 1
                self.mitigationST += 1
                self.mitigationMA += 1
                self.mitigationMY += 1
            if x == '165': #Jack of All Trades
                self.mitigationEN += 2
                self.mitigationST += 2
                self.mitigationMA += 2
                self.mitigationMY += 2
            if int(x) >= 149 and int(x) <= 164:
                mitnumber = int(mastercards[x].maintext[7])
                mitstring = mastercards[x].maintext[9:11]
                if mitstring == 'EN':
                    self.mitigationEN += mitnumber
                elif mitstring == 'ST':
                    self.mitigationST += mitnumber
                elif mitstring == 'MA':
                    self.mitigationMA += mitnumber
                elif mitstring == 'MY':
                    self.mitigationMY += mitnumber

class card: #the card class
    def __init__(self,name,type,gamesize,maintext,delve1,delve2,delve3,cost,deck):
        self.name = name
        self.type = type
        self.gamesize = gamesize
        self.maintext = maintext
        self.delve1 = delve1
        self.delve2 = delve2
        self.delve3 = delve3
        self.cost = cost
        self.deck = deck

class stack: #the stack class
    def __init__(self,contents,hazard,reward,items,size,ENhazard,SThazard,MAhazard,MYhazard):
        self.contents = contents
        self.hazard = hazard
        self.reward  = reward
        self.items = items
        self.size = size
        self.ENhazard = ENhazard
        self.SThazard = SThazard
        self.MAhazard = MAhazard
        self.MYhazard = MYhazard
