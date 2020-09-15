import os
import csv
import errno
import configparser
import argparse
from random import seed
from random import randint
from datetime import date
from datetime import datetime

# CLASSES

class player: #the player class
    def __init__(self,recklessness,malice,greed,height,gold,party,health,treasures,items,capacity,burden,mitigationEN,mitigationST,mitigationMA,mitigationMY):
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

    def setburden(self):
        self.burden += len(self.treasures)

    def healthinit(self):
        for x in range (len(self.party)):
            self.health.append(2)

    def takedamage(self,damage):
        self.damage = damage
        while self.damage > 0:
            for ahealth in self.health:
                if 2 in self.health:
                    if ahealth == 2:
                        ahealth -= 1
                else:
                    ahealth[-1] -= 1

    def selltreasure(self,delveindicator):
        for loot in self.treasures:
            if delveindicator == 1:
                self.gold += int(mastercards[loot].delve1[:-1])
            if delveindicator == 2:
                self.gold += int(mastercards[loot].delve2[:-1])
            if delveindicator == 3:
                self.gold += int(mastercards[loot].delve3[:-1])

    def statset(self):
        self.capacity = 0
        self.mitigationEN = 0
        self.mitigationST = 0
        self.mitigationMA = 0
        self.mitigationMY = 0
        self.capacity += sum(self.health)
        for x in self.party:
            if x == '121':
                self.mitigationEN += 1
                self.mitigationST += 1
                self.mitigationMA += 1
                self.mitigationMY += 1
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

# FUNCTIONS

def readcsv(currentdir): #reads the csv file
    os.chdir(currentdir) #moves to the main directory
    tabledata = [] #initialises the 'tabledata' list
    csv.register_dialect('card',delimiter=",",  quoting=csv.QUOTE_NONE) #creates a csv dialect that seperates files on commas
    with open('cards.csv', newline='') as csvfile: #opens the target filename (value storied in settings[1]
        csvobject = csv.reader(csvfile, dialect='card')  #creates a csv object
        for row in csvobject: #reads over all rows
            tabledata.append(row) #adds all rows to the 'tabledata' list
    return tabledata

def shuffle(cards):
    seed()
    shuffcards = []
    while len(cards) > 0:
        select = randint (0, len(cards))
        shuffcards.append(cards.pop(select-1))
    return shuffcards

def personality(players,player1p,player2p,player3p,player4p,player5p):
    player1p += '()';player2p += '()';player3p += '()';player4p += '()';player5p += '()'
    player1person = eval((player1p))
    player1 = player(player1person[0],player1person[1],player1person[2],player1person[3],0,[],[],[],[],0,0,0,0,0,0)
    player2person = eval((player2p))
    player2 = player(player2person[0],player2person[1],player2person[2],player2person[3],0,[],[],[],[],0,0,0,0,0,0)
    player3person = eval((player3p))
    player3 = player(player3person[0],player3person[1],player3person[2],player3person[3],0,[],[],[],[],0,0,0,0,0,0)
    player4person = eval((player4p))
    player4 = player(player4person[0],player4person[1],player4person[2],player4person[3],0,[],[],[],[],0,0,0,0,0,0)
    player5person = eval((player5p))
    player5 = player(player5person[0],player5person[1],player5person[2],player5person[3],0,[],[],[],[],0,0,0,0,0,0)
    playerinfo = [player1,player2,player3,player4,player5]
    return playerinfo

def random():
    seed()
    recklessness = randint (1,100)
    malice = randint(1,100)
    greed = randint(1,100)
    height = randint(140,220)
    personality = [recklessness,malice,greed,height]
    return personality

def leaderpick(players,playerinfo,leaderdeck):
    for player in range(players):
        if playerinfo[player].greed > 60 and playerinfo[player].recklessness > 50 and '122' in leaderdeck:
            playerinfo[player].party.append(leaderdeck.pop(leaderdeck.index('122')))
            playerinfo[player].health.append(2)
        elif playerinfo[player].greed > 50 and '125' in leaderdeck:
            playerinfo[player].party.append(leaderdeck.pop(leaderdeck.index('125')))
            playerinfo[player].health.append(2)
        elif playerinfo[player].malice > 40 and '121' in leaderdeck:
            playerinfo[player].party.append(leaderdeck.pop(leaderdeck.index('121')))
            playerinfo[player].health.append(2)
        else:
            playerinfo[player].party.append(leaderdeck.pop(0))
            playerinfo[player].health.append(2)
        playerinfo[player].statset()
        if playerinfo[player].party[0] == '122':
            playerinfo[player].gold = 40
        else:
            playerinfo[player].gold = 30
    return playerinfo

def tavern(players,playerinfo,peondeck,basicdeck,advanceddeck,delveindicator): # controls the hiring phase
    log.write (f"Hiring phase, delve {delveindicator}.\n")
    bl(1)
    tavernspread = []
    if delveindicator == 1: #sets up the first delve
        for a in range(players*2):
            tavernspread.append(peondeck.pop(-1))
        for b in range(players):
            tavernspread.append(basicdeck.pop(-1))
    if delveindicator == 2: #sets up the second delve
        for a in range(players):
            tavernspread.append(peondeck.pop(-1))
        for b in range(players):
            tavernspread.append(basicdeck.pop(-1))
        for c in range(players):
            tavernspread.append(advanceddeck.pop(-1))
    if delveindicator == 3: #sets up the third delve
        for a in range(players):
            tavernspread.append(basicdeck.pop(-1))
        for b in range(players*2):
            try:
                tavernspread.append(advanceddeck.pop(-1))
            except IndexError:
                tavernspread.append(basicdeck.pop(-1))
    log.write ('Tavern contains:\n')
    for z in tavernspread:
        log.write(f"{mastercards[z].name}")
        if (tavernspread.index(z)) < len(tavernspread)-1:
            log.write(', ')
        else:
            log.write('.\n')
    bl(1)
    goldlist = []
    for n in range (players):
        goldlist.append(playerinfo[n].gold)
    position = goldlist.index(max(goldlist))
    log.write(f"Hiring commences. Player {position+1} has the most gold ({goldlist[position]}) and is first to pick.\n")
    bl(1)
    picklist = [True] * players
    while True in picklist:
        for p in range (len(tavernspread)):
            try:
                cost = int(mastercards[tavernspread[p-1]].cost) # retrieves the cost of the card
                if cost < playerinfo[position].gold: #checks the cost of the card against the goldreserve of the player
                    playerinfo[position].party.append(tavernspread.pop(p-1)) #removes the listing from the tavern spread and adds to player info
                    playerinfo[position].health.append(2) # sets the health of the new hire to 2
                    playerinfo[position].gold -= cost #decreases the player's gold
                    log.write(f"player {position+1} buys {mastercards[playerinfo[position].party[-1]].name}")
                    playerinfo[position].statset()
                    break
                elif cost == playerinfo[position].gold:
                    diceroll = randint (1,100)
                    if diceroll <= playerinfo[position].recklessness:
                        playerinfo[position].party.append(tavernspread.pop(p - 1))  # removes the listing from the tavern spread and adds to player info
                        playerinfo[position].health.append(2)  # sets the health of the new hire to 2
                        playerinfo[position].gold -= cost  # decreases the player's gold
                        log.write(f"player {position + 1} buys {mastercards[playerinfo[position].party[-1]].name}")
                        playerinfo[position].statset()
                        break
                    else:
                        pass
                else:
                    picklist[position] = False
            except IndexError:
                if len(playerinfo[position].party) > 5:
                    picklist[position] = False
        position += 1
        if position > players-1:
            position = 0
    bl(1)
    log.write('Hiring phase concludes.\n')
    bl(1)
    for i in range (len(tavernspread)):
        if mastercards[tavernspread[i]].type == 'Peon':
            peondeck.append(tavernspread[i])
        if mastercards[tavernspread[i]].type == 'Basic Adventurer':
            basicdeck.append(tavernspread[i])
        if mastercards[tavernspread[i]].type == 'Advanced Adventurer':
            advanceddeck.append(tavernspread[i])
    for j in range (players):
        log.write(f"Player {j+1}'s party consists of:\n")
        for k in range (len(playerinfo[j].party)):
            log.write(f"{mastercards[playerinfo[j].party[k]].name}")
            if k < len(playerinfo[j].party)-1:
                log.write(', ')
            else:
                log.write('.\n')
        log.write(f"They have {playerinfo[j].gold} gold remaining.\n")
        bl(1)
    tavernpack = [playerinfo, peondeck, basicdeck, advanceddeck]
    return tavernpack

def expedition(players,playerinfo,expeditiondeck,delveindicator,firstout):
    roundcounter = 1
    timer = 1
    escaped = [0] * players
    log.write (f"Expedition phase, delve {delveindicator}.\n")
    bl(1)
    position = 0
    playlist = [x+1 for x in range (players)]
    if delveindicator == 1:
        heightlist = []
        for n in range(players):
            heightlist.append(playerinfo[n].height)
        position = heightlist.index(max(heightlist))
        log.write(f"Play commences. Player {playlist[position]} is the tallest at {heightlist[position]}cm and thus goes first.\n")
    else:
        if firstout > 0:
            position = firstout
            log.write(f"Play commences. Player {playlist[position]} was first out of the mine last delve and thus goes first.\n")
        elif firstout == 0:
            position = randint(0,players-1)
            log.write(f"Play commences. Since all players were lost on the previous delve, they roll dice. Player {playlist[position]} wins, and thus goes first.\n")
    stacks = []
    for t in range(players):
        stacks.append([])
    discardpile = []
    playing = True
    while playing:
        log.write(f"Round {roundcounter}")
        bl(1)
        for x in range(players):
            stackstats = stats(stacks, delveindicator)
            for y in range(players):
                try:
                    carddraw = expeditiondeck.pop(-1)
                    log.write(f"Player {playlist[position]} draws {mastercards[carddraw].name}\n")
                    emptystack = False
                    for z in range (len(stacks)):
                        if stacks[z] == []:
                            emptystack = True
                            emptyindex = z
                    if mastercards[carddraw].deck == 'Treasure':
                        if emptystack == True:
                            stacks[emptyindex].append(carddraw)
                            emptystack = False
                        else:
                            stacks[stackstats[2]].append(carddraw)
                    if mastercards[carddraw].deck == 'Hazard':
                        if emptystack == True:
                            stacks[emptyindex].append(carddraw)
                            emptystack = False
                        else:
                            stacks[stackstats[1]].append(carddraw)
                    if mastercards[carddraw].deck == 'Item':
                        if emptystack == True:
                            stacks[emptyindex].append(carddraw)
                            emptystack = False
                        else:
                          stacks[stackstats[3]].append(carddraw)
                    if mastercards[carddraw].deck == 'Null':
                        if emptystack == True:
                            stacks[emptyindex].append(carddraw)
                            emptystack = False
                        else:
                           stacks[stackstats[1]].append(carddraw)
                except IndexError:
                    if timer == 1:
                        if len(playlist) > 0:
                            log.write(f"Player {playlist[position]} reaches the end of the deck, and replenishes it from the discard pile. The Darkness Hungers!\n")
                            discardpile = shuffle(discardpile)
                            for x in range (len(discardpile)):
                                expeditiondeck.append(discardpile.pop(-1))
                            timer += 1
                        else:
                            log.write ("All players have escaped the dungeon!\n")
                            playing = False
                            break
                    elif timer == 2:
                        log.write(f"Darkness consumes us!\n")
                        playing = False
                        break
            bl(1)
            if playing == False:
                pass
            else:
                for w in (stacks):
                    log.write(f"stack {stacks.index(w)+1}: ")
                    for x in range(len(w)):
                        log.write(f"{mastercards[w[x]].name}")
                        if x < len(w)-1:
                            log.write(', ')
                        else:
                            log.write('.')
                    log.write(f"Size: {len(w)}\n")
                for a in range (len(stacks)):
                    if len(stacks[a]) >= 6:
                        stackstats = stats(stacks, delveindicator)
                        discardables = takestack(stacks[a],a,position,playerinfo,stackstats,playlist)
                        discardpile.extend(discardables)
                        stacks[a] = []
                if sum(playerinfo[position].health) > 0:
                    pass
                else:
                    log.write (f"Player {playlist[position]}'s party has been wiped out! {playerinfo[playlist[position]].party[0].name} limps back to the surface...\n")
                    playlist.pop(position)
                if playerinfo[position].capacity - playerinfo[position].burden < 2:
                    log.write (f"Player {playlist[position]} attempts to escape the dungeon!\n")
                    escapesequence(position,playerinfo)
                    escaped[position] = 1
                    playlist.pop(position)
            position += 1
            if position > len(playlist)-1:
                position = 0
        log.write (f"Discard pile: {len(discardpile)}\n")
        log.write (f"Deck: {len(expeditiondeck)}\n")
        roundcounter += 1
    log.write (f"Expedition phase delve {delveindicator} over.\n")
    expeditiondeck.extend(discardpile)
    bl(1)

def escapesequence(position,playerinfo):
    log.write('placeholder. Escape successful.\n')

def takestack(stacka,stackid,position,playerinfo,stackstats,playlist):
    log.write (f"Player {playlist[position]} takes stack {stackid+1} containing: \n")
    for x in range (len(stacka)):
        log.write(f"{mastercards[stacka[x]].name}")
        if x < len(stacka) - 1:
            log.write(', ')
        else:
            log.write('.\n')
    if stackstats[0][stackid].hazard > 0:
        startdamage = stackstats[0][stackid].hazard
        log.write (f"They take {startdamage} hazard from the stack.\n")
        log.write (f"{stackstats[0][stackid].ENhazard} EN Hazard\n")
        log.write(f"{stackstats[0][stackid].SThazard} ST Hazard\n")
        log.write(f"{stackstats[0][stackid].MAhazard} MA Hazard\n")
        log.write(f"{stackstats[0][stackid].MYhazard} MY Hazard\n")
        if stackstats[0][stackid].ENhazard > 0:
            stackstats[0][stackid].ENhazard -= playerinfo[position].mitigationEN
            if stackstats[0][stackid].ENhazard < 0:
                stackstats[0][stackid].ENhazard = 0
        if stackstats[0][stackid].SThazard > 0:
            stackstats[0][stackid].SThazard -= playerinfo[position].mitigationST
            if stackstats[0][stackid].SThazard < 0:
                stackstats[0][stackid].SThazard = 0
        if stackstats[0][stackid].MAhazard > 0:
            stackstats[0][stackid].MAhazard -= playerinfo[position].mitigationMA
            if stackstats[0][stackid].MAhazard < 0:
                stackstats[0][stackid].MAhazard = 0
        if stackstats[0][stackid].MYhazard > 0:
            stackstats[0][stackid].MYhazard -= playerinfo[position].mitigationMY
            if stackstats[0][stackid].MYhazard < 0:
                stackstats[0][stackid].MYhazard = 0
        mitigationtot = startdamage - stackstats[0][stackid].MYhazard
        log.write(f"They mitigate {mitigationtot} hazard. {stackstats[0][stackid].MYhazard} hazard remaining.\n")
        if stackstats[0][stackid].MYhazard > 0:
            log.write('Rolling dice.\n')
            damage = 0
            for x in range (stackstats[0][stackid].MYhazard):
                diceroll = randint(1,6)
                log.write (f"{diceroll}")
                if x < stackstats[0][stackid].MYhazard - 1:
                    log.write(', ')
                else:
                    log.write('.')
                if diceroll >= 5:
                    damage += 1
            if damage > 0:
                log.write(f"They take {damage} damage.\n")
            else:
                log.write('They take no damage.\n')
        else:
            log.write('They mitigate all hazard, and take no damage.\n')
    else:
        log.write (f"They take no hazard from the stack.\n")
    bl(1)
    stackreward = stackstats[0][stackid].reward
    log.write (f"They gain {stackreward} worth of treasure!\n")
    treasurelist = []
    for y in range (len(stacka)):
        if mastercards[stacka[y]].deck == 'Treasure' or mastercards[stacka[y]].deck == 'Artefact':
            log.write(f"{mastercards[stacka[y]].name}")
            treasurelist.append(stacka[y])
    for z in stacka:
        if z in treasurelist:
            del z
    playerinfo[position].setburden()
    localcapacity = playerinfo[position].capacity - playerinfo[position].burden
    while localcapacity > 0 and len(treasurelist) > 0:
        playerinfo[position].treasures.append(treasurelist.pop(-1))
        localcapacity -= 1
        log.write (f"Player {position+1} took {mastercards[playerinfo[position].treasures[-1]].name}!\n")
    stacka.extend(treasurelist)
    return stacka

def stats(stacks,delveindicator):#this routine helps the AI make judgements about where to put cards
    delvestring = 'delve'+str(delveindicator)
    statblock = []
    hazardstats = [0] * len(stacks)
    rewardstats = [0] * len(stacks)
    itemnum = [0] * len(stacks)
    for n in range(len(stacks)):
        if stacks[n] == []:
            substats = stack(0,randint(1,3),randint(1,3),randint(1,3),len(stacks[n]),0,0,0,0)
            hazardstats[n] = substats.hazard
            rewardstats[n] = substats.reward
            itemnum[n] = substats.items
            statblock.append(substats)
        else:
            hazard = 0
            reward = 0
            items = 0
            ENhazard, SThazard, MAhazard, MYhazard = 0,0,0,0
            for x in range(len(stacks[n])):
                if mastercards[stacks[n][x]].deck == 'Hazard':
                    hazard += sum([int(s) for s in getattr(mastercards[stacks[n][x]],delvestring) if s.isdigit()])
                    if len(getattr(mastercards[stacks[n][x]],delvestring)) == 7: # interprets hazard strings with two parts
                        hazstring1 = getattr(mastercards[stacks[n][x]],delvestring)[1:3]
                        hazstring2 = getattr(mastercards[stacks[n][x]],delvestring)[5:7]
                        haznum1 = int(getattr(mastercards[stacks[n][x]], delvestring)[0])
                        haznum2 = int(getattr(mastercards[stacks[n][x]], delvestring)[4])
                        if hazstring1 == 'EN':
                         ENhazard += haznum1
                        elif hazstring1 == 'ST':
                            SThazard += haznum1
                        elif hazstring1 == 'MA':
                            MAhazard += haznum1
                        elif hazstring1 == 'MY':
                            MYhazard += haznum1
                        if hazstring2 == 'EN':
                            ENhazard += haznum2
                        elif hazstring2 == 'ST':
                            SThazard += haznum2
                        elif hazstring2 == 'MA':
                            MAhazard += haznum2
                        elif hazstring2 == 'MY':
                            MYhazard += haznum2
                    elif len(getattr(mastercards[stacks[n][x]],delvestring)) == 3: # interprets hazard strings with one part
                        hazstring1 = getattr(mastercards[stacks[n][x]],delvestring)[1:3]
                        haznum1 = int(getattr(mastercards[stacks[n][x]], delvestring)[0])
                        if hazstring1 == 'EN':
                            ENhazard += haznum1
                        elif hazstring1 == 'ST':
                            SThazard += haznum1
                        elif hazstring1 == 'MA':
                            MAhazard += haznum1
                        elif hazstring1 == 'MY':
                            MYhazard += haznum1
                elif mastercards[stacks[n][x]].deck == 'Treasure':
                    reward += int(getattr(mastercards[stacks[n][x]],delvestring)[:-1])
                elif mastercards[stacks[n][x]].deck == 'Item':
                    items += 1
                else:
                    pass
            contents = list.copy(stacks[n])
            substats = stack(contents,hazard, reward,items,len(stacks[n]),ENhazard,SThazard,MAhazard,MYhazard)
            hazardstats[n] = hazard
            rewardstats[n] = reward
            itemnum[n] = items
            statblock.append(substats)
    stackstats = [statblock,hazardstats.index(min(hazardstats)),rewardstats.index(max(rewardstats)),itemnum.index(min(itemnum))]
    return stackstats

def resolve(playerinfo,delveindicator):
    for x in range (len(playerinfo)):
        playerinfo[x].selltreasure(delveindicator)

def bl(num):
    for x in range (num):
        log.write('\n\n')

def pathpadder(lognum,logincrement): #this routine pads out the number in the log file names
    pad = lognum - len(str(logincrement))
    padstring = '0' * pad
    return padstring

# INITIALISATION
# config read
currentdir = os.getcwd()
config = configparser.ConfigParser()  # the following lines extract the settings from the config file
config.read('Settings/config.ini')
version = config['DEFAULT']['version']
players = int(config['DEFAULT']['players'])
player1p = config['DEFAULT']['player1']
player2p = config['DEFAULT']['player2']
player3p = config['DEFAULT']['player3']
player4p = config['DEFAULT']['player4']
player5p = config['DEFAULT']['player5']
lognum = int(config['DEFAULT']['lognumber'])
timesnum = int(config['DEFAULT']['timestorun'])
# arguments
parser = argparse.ArgumentParser(prog="GreedySim") # the subsequent lines contain the command line arguments
parser.add_argument("-m", "--multiple", action='store_true', help = "runs multiple times (set in config.ini)")
parser.add_argument("-v","--version", action='version',version=version)
args = parser.parse_args()
if args.multiple:
    runs = timesnum
else:
    runs = 1


# This section of the program extracts information about the cards from the csv file and creates dictionaries and arrays for use by the rest of the program
tabledata = readcsv(currentdir) # reads the CSV file
keydata = []
counter = 0
expeditioncards,artefactcards,missioncards,leadercards,peoncards,basiccards,advancedcards,mastercards = {},{},{},{},{},{},{},{}
for n in tabledata:
    counter += 1
    padding = len(str(len(tabledata))) - len(str(counter))
    newkey = (f"{padding * '0'}{counter}")
    #name, type, gamesize, delve1, delve2, delve3, cost
    newentry = card(n[0],n[1],n[2],n[3],n[5],n[6],n[7],n[8][:-1],n[10])
    if players == 2 and newentry.gamesize == '3+' or newentry.gamesize == '4+':
        pass
    elif players == 3 and newentry.gamesize == '4+':
        pass
    else:
        if newentry.deck == 'Null' or newentry.deck == 'Treasure' or newentry.deck == 'Item' or newentry.deck == 'Hazard':
            expeditioncards.update({newkey : newentry})
        elif newentry.deck == 'Artefact':
            artefactcards.update({newkey : newentry})
        elif newentry.deck == 'Mission':
            missioncards.update({newkey : newentry})
        elif newentry.type == 'Expedition Leader':
            leadercards.update({newkey : newentry})
        elif newentry.type == 'Peon':
            peoncards.update({newkey : newentry})
        elif newentry.type == 'Basic Adventurer':
            basiccards.update({newkey: newentry})
        elif newentry.type == 'Advanced Adventurer':
            advancedcards.update({newkey: newentry})
        mastercards.update({newkey : newentry})

#LOOP

playing = True
playcount = 0
while playing:

    # START LOG
    now = datetime.now()
    smalltime = now.strftime("%H:%M:%S")
    today = str(date.today())
    try:
        os.makedirs(f"{currentdir}/Logs/")
    except OSError as exc:  # handles the error if the directory already exists
        if exc.errno != errno.EEXIST:
            raise
        pass
    logincrement = 1
    padstring = pathpadder (lognum,logincrement)
    while os.path.exists(f"{currentdir}/Logs/log {today} - {padstring}{logincrement}.txt"):
        logincrement += 1
    padstring = pathpadder (lognum,logincrement)
    log = open(f"{currentdir}/Logs/log {today} - {padstring}{logincrement}.txt", "w")
    log.write(f"GreedySim version {version}. Log number {logincrement}. Date: {today}. Time: {smalltime}\n")
    log.write(f"\'Too Greedily, Too Deep\' copyright Sydney Cardew.\n")
    bl(2)

    #DECK SETUP

    expeditiondeck = list(expeditioncards.keys())
    artefactdeck = list(artefactcards.keys())
    missiondeck = list(missioncards.keys())
    leaderdeck = list(leadercards.keys())
    peondeck = list(peoncards.keys())
    basicdeck = list(basiccards.keys())
    advanceddeck = list(advancedcards.keys())

    #PREGAME

    playcount += 1
    delveindicator = 1
    firstout = 0
    playerinfo = personality(players,player1p,player2p,player3p,player4p,player5p)
    log.write (f"There are {players} players.\n")
    playerinfo = leaderpick(players,playerinfo,leaderdeck)
    bl(1)
    for n in range (int(players)):
        log.write(f"Player {n+1} has {playerinfo[n].recklessness} recklessness, {playerinfo[n].malice} malice and {playerinfo[n].greed} greed, is {playerinfo[n].height}cm tall and has picked {mastercards[playerinfo[n].party[0]].name}.\n")
        bl(1)

    # DELVE 1

    log.write ('Delve 1 Begins\n')
    bl(1)
    expeditiondeck = shuffle(expeditiondeck)
    artefactdeck = shuffle(artefactdeck)
    artefactadd = artefactdeck.pop(0)
    expeditiondeck.append(artefactadd)
    expeditiondeck = shuffle(expeditiondeck)
    peondeck = shuffle(peondeck)
    basicdeck = shuffle(basicdeck)
    tavernpack = tavern(players,playerinfo,peondeck,basicdeck,advanceddeck,delveindicator)
    playerinfo, peondeck, basicdeck, advanceddeck = tavernpack[0], tavernpack[1], tavernpack[2], tavernpack[3]
    delvelist = expedition(players,playerinfo,expeditiondeck,delveindicator,firstout)
    resolve(playerinfo,delveindicator)
    expeditiondeck = list(expeditioncards.keys())

    # DELVE 2

    log.write ('Delve 2 Begins\n')
    bl(1)
    delveindicator += 1
    expeditiondeck = shuffle(expeditiondeck)
    artefactdeck = shuffle(artefactdeck)
    for x in range (1,3):
        artefactadd = artefactdeck.pop(0)
    expeditiondeck.append(artefactadd)
    expeditiondeck = shuffle(expeditiondeck)
    peondeck = shuffle(peondeck)
    basicdeck = shuffle(basicdeck)
    advanceddeck = shuffle(advanceddeck)
    tavernpack = tavern(players,playerinfo,peondeck,basicdeck,advanceddeck,delveindicator)
    playerinfo, peondeck, basicdeck, advanceddeck = tavernpack[0], tavernpack[1], tavernpack[2], tavernpack[3]
    delvelist = expedition(players,playerinfo,expeditiondeck,delveindicator,firstout)
    resolve(playerinfo,delveindicator)
    expeditiondeck = list(expeditioncards.keys())

    # DELVE 3

    log.write ('Delve 3 Begins\n')
    bl(1)
    delveindicator += 1
    expeditiondeck = shuffle(expeditiondeck)
    artefactdeck = shuffle(artefactdeck)
    expeditiondeck.extend(artefactdeck)
    expeditiondeck = shuffle(expeditiondeck)
    basicdeck = shuffle(basicdeck)
    advanceddeck = shuffle(advanceddeck)
    tavernpack = tavern(players,playerinfo,peondeck,basicdeck,advanceddeck,delveindicator)
    playerinfo, peondeck, basicdeck, advanceddeck = tavernpack[0], tavernpack[1], tavernpack[2], tavernpack[3]
    delvelist = expedition(players,playerinfo,expeditiondeck,delveindicator,firstout)
    resolve(playerinfo,delveindicator)
    log.close()
    if playcount == runs:
        playing = False
    else:
        pass