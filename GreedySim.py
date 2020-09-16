import argparse
import configparser
import csv
import errno
import os
from datetime import date
from datetime import datetime
from random import randint
from random import seed


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
        for x in range (damage):
            self.health[self.health.index(max(self.health))] -= 1


    def selltreasure(self,delveindicator):
        soldtreasure = 0
        for loot in self.treasures:
            if delveindicator == 1:
                self.gold += int(mastercards[loot].delve1[:-1])
                soldtreasure += 1
            if delveindicator == 2:
                self.gold += int(mastercards[loot].delve2[:-1])
                soldtreasure += 1
            if delveindicator == 3:
                self.gold += int(mastercards[loot].delve3[:-1])
                soldtreasure += 1
        return soldtreasure

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
            try: # this substitutes in basic adventurers if the game runs out of advanced adventurers, which it invariably will in a 5 player game
                tavernspread.append(advanceddeck.pop(-1))
            except IndexError:
                tavernspread.append(basicdeck.pop(-1))
    log.write ('Tavern contains:\n')
    for z in tavernspread: # logs the cards in the tavern tableau
        log.write(f"{mastercards[z].name}")
        if (tavernspread.index(z)) < len(tavernspread)-1:
            log.write(', ')
        else:
            log.write('.\n')
    bl(1)
    goldlist = [] # these lines are used to determine which player has the most gold
    for n in range (players):
        goldlist.append(playerinfo[n].gold)
    goldmaxnum = goldlist.count(max(goldlist))
    if goldmaxnum > 1: # this controls what happens if more than one player has the same gold totals
        log.write(f"Two players have the same gold totals. rolling dice!\n")
        maxlist = []
        maxid = -1
        while True:
            try:
                maxid = goldlist.index(max(goldlist), maxid+1)
                maxlist.append(maxid)
            except ValueError:
                break
        chooser = randint (1,len(maxlist))
        position = maxlist[chooser-1]
        log.write(f"Player{position+1} wins the roll and will go first!")
        rolloff = True
    else:
        position = goldlist.index(max(goldlist))
        rolloff = False
    log.write(f"Hiring commences. ")
    if rolloff == False:
       log.write(f"Player {position+1} has the most gold ({goldlist[position]}) and is first to pick.\n")
    elif rolloff == True:
        log.write(f"Player {position+1} has won the roll-off and is first to pick.\n")
    bl(1)
    picklist = [True] * players # records which players are still picking
    while True in picklist:
        for p in range (len(tavernspread)): # runs through the picking process
            try:
                cost = int(mastercards[tavernspread[p-1]].cost) # retrieves the cost of the card
                if cost < playerinfo[position].gold: #checks the cost of the card against the goldreserve of the player
                    playerinfo[position].party.append(tavernspread.pop(p-1)) #removes the listing from the tavern spread and adds to player info
                    playerinfo[position].health.append(2) # sets the health of the new hire to 2
                    playerinfo[position].gold -= cost #decreases the player's gold
                    log.write(f"player {position+1} buys {mastercards[playerinfo[position].party[-1]].name}\n")
                    playerinfo[position].statset()
                    break
                elif cost == playerinfo[position].gold:
                    diceroll = randint (1,100)
                    if diceroll <= playerinfo[position].recklessness:
                        playerinfo[position].party.append(tavernspread.pop(p - 1))  # removes the listing from the tavern spread and adds to player info
                        playerinfo[position].health.append(2)  # sets the health of the new hire to 2
                        playerinfo[position].gold -= cost  # decreases the player's gold
                        log.write(f"player {position + 1} buys {mastercards[playerinfo[position].party[-1]].name}\n")
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
    for i in range (len(tavernspread)): #returns the unpicked cards to their correct decks
        if mastercards[tavernspread[i]].type == 'Peon':
            peondeck.append(tavernspread[i])
        if mastercards[tavernspread[i]].type == 'Basic Adventurer':
            basicdeck.append(tavernspread[i])
        if mastercards[tavernspread[i]].type == 'Advanced Adventurer':
            advanceddeck.append(tavernspread[i])
    for j in range (players): # reads out party make-ups
        log.write(f"Player {j+1}'s party consists of:\n")
        for dwarf in range (len(playerinfo[j].party)):
            log.write(f"{mastercards[playerinfo[j].party[dwarf]].name}")
            if dwarf < len(playerinfo[j].party)-1:
                log.write(', ')
            else:
                log.write('.\n')
        log.write(f"They have {playerinfo[j].gold} gold remaining.\n")
        bl(1)
    tavernpack = [playerinfo, peondeck, basicdeck, advanceddeck]
    return tavernpack

def expedition(players,playerinfo,expeditiondeck,delveindicator,firstout): #Controls the expedition phase
    roundcounter = 1
    timer = 1
    escapedcount = 0
    escapeflag = False
    log.write (f"Expedition phase, delve {delveindicator}.\n")
    bl(1)
    position = 0
    playlist = [x+1 for x in range (players)] # this array lets the game know which players are in the game and which are not without jumbling the indices
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
    for t in range(players): # creates an appropriate number of empty lists to hold stacks
        stacks.append([])
    discardpile = []
    playing = True
    while playing: # The expedition loop
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
                for playstack in (stacks):
                    log.write(f"stack {stacks.index(playstack)+1}: ")
                    for x in range(len(playstack)):
                        log.write(f"{mastercards[playstack[x]].name}")
                        if x < len(playstack)-1:
                            log.write(', ')
                        else:
                            log.write('.')
                    log.write(f"Size: {len(playstack)}\n")
                bl(1)
                for a in range (len(stacks)):
                    if len(stacks[a]) >= 6:
                        stackstats = stats(stacks, delveindicator)
                        discardables = takestack(stacks[a],a,position,playerinfo,stackstats,playlist)
                        discardpile.extend(discardables)
                        stacks[a] = []
                if sum(playerinfo[position].health) > 0:
                    pass
                elif sum(playerinfo[position].health) <= 0:
                    log.write (f"Player {playlist[position]}'s party has been wiped out! They limp back to the surface...\n")
                    playlist.pop(position)
                elif playerinfo[position].capacity - playerinfo[position].burden < 2 and sum(playerinfo[position].health) > 0:
                    log.write (f"Player {playlist[position]} attempts to escape the dungeon!\n")
                    escapesequence(position,playerinfo)
                    escapedcount += 1
                    playlist.pop(position)
                    if escapeflag == False:
                        firstout = position
                        escapeflag = True
            position += 1
            if position > len(playlist)-1:
                position = 0
        log.write (f"Discard pile: {len(discardpile)}\n")
        log.write (f"Deck: {len(expeditiondeck)}\n")
        roundcounter += 1
    log.write (f"Expedition phase delve {delveindicator} over.\n")
    log.write (f"{escapedcount} parties made it back to the surface in relative safety.\n")
    log.write (f"{players-escapedcount} parties crawled bleeding from the haunted depths!\n")
    expeditiondeck.extend(discardpile)
    bl(1)
    delvepack = [firstout,expeditiondeck,playerinfo]
    return delvepack

def escapesequence(position,playerinfo):
    log.write('placeholder. Escape successful.\n')

def takestack(stacka,stackid,position,playerinfo,stackstats,playlist): #This function 'takes' a stack and deals with the consequences
    log.write (f"Player {playlist[position]} takes stack {stackid+1} containing: \n")
    for stackcard in range (len(stacka)):
        log.write(f"{mastercards[stacka[stackcard]].name}")
        if stackcard < len(stacka) - 1:
            log.write(', ')
        else:
            log.write('.\n')
    if stackstats[0][stackid].hazard > 0: #this segment controls the damage and damage mitigation
        startdamage = stackstats[0][stackid].hazard
        endamage = stackstats[0][stackid].ENhazard
        stdamage = stackstats[0][stackid].SThazard
        madamage = stackstats[0][stackid].MAhazard
        mydamage = stackstats[0][stackid].MYhazard
        enmit = playerinfo[position].mitigationEN
        stmit = playerinfo[position].mitigationST
        mamit = playerinfo[position].mitigationMA
        mymit = playerinfo[position].mitigationMY
        log.write (f"They take {startdamage} hazard from the stack.\n")
        log.write (f"{endamage} EN Hazard\n")
        log.write(f"{stdamage} ST Hazard\n")
        log.write(f"{madamage} MA Hazard\n")
        log.write(f"{mydamage} MY Hazard\n")
        mitigationtot = (enmit + stmit + mamit + mymit)
        finaldamage = startdamage - mitigationtot
        log.write(f"They mitigate {mitigationtot} hazard. {finaldamage} hazard remaining.\n")
        if finaldamage > 0:
            log.write('Rolling dice.\n')
            damage = 0
            for hazdice in range (finaldamage):
                diceroll = randint(1,6)
                log.write (f"{diceroll}")
                if hazdice < finaldamage - 1:
                    log.write(', ')
                else:
                    log.write('.\n')
                if diceroll >= 5:
                    damage += 1
            if damage > 0:
                if '145' in playerinfo[position].party: # Deploys the paladin's special power
                    log.write(f"The paladin absorbs 1 point of damage!\n")
                    damage -= 1
                log.write(f"They take {damage} damage.\n")
                playerinfo[position].takedamage(damage)
                log.write(f"{playerinfo[position].health}")
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
            log.write(f"{mastercards[stacka[y]].name}\n")
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
    bl(1)
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

def resolve(playerinfo,delveindicator,deaths,totaltreasure): # the resolution phase
    for x in range (len(playerinfo)):
        soldtreasure = playerinfo[x].selltreasure(delveindicator)
        totaltreasure += soldtreasure
        if '142' in playerinfo[x].party:
            accountmoney = 10 * delveindicator
            log.write(f"The Accountant cooks the books and generates an extra {accountmoney}G for player {x+1}\n\n")
            playerinfo[x].gold += accountmoney
        try:
            playerinfo[x].health[0] = 1
        except IndexError:
            playerinfo[x].health.append(1)
        for y in range (len(playerinfo[x].health)):
            if playerinfo[x].health[y] == 0:
                try:
                    log.write(f"{mastercards[playerinfo[x].party[y]].name} has died!\n")
                    playerinfo[x].party.pop(y)
                    deaths += 1
                except IndexError:
                    pass
    resolvestats = [deaths,totaltreasure]
    return resolvestats

def bl(num): # inserts blank lines to help format the log file
    for x in range (num):
        log.write('\n\n')

def pathpadder(lognum,logincrement): #this routine pads out the number in the log file names
    pad = lognum - len(str(logincrement))
    padstring = '0' * pad
    return padstring

def loginit(currentdir,version,lognum,runs,playcount,setpath):
    now = datetime.now()
    smalltime = now.strftime("%H:%M:%S")
    today = str(date.today())
    if runs > 1:
        pathmod = f"/Logs/Multi/{today} - ({runs}) - "
        pathincrement = 1
        padstring = pathpadder (lognum,pathincrement)
        while os.path.exists(f"{currentdir}{pathmod}{padstring}{pathincrement}/"):
            pathincrement += 1
            padstring = pathpadder (lognum,pathincrement)
        if setpath == True:
            pathincrement -= 1
        elif setpath == False:
            pass
        pathmod = f"{pathmod}{padstring}{pathincrement}/"
    elif runs == 1:
        pathmod = '/Logs/'
    try:
        os.makedirs(f"{currentdir}{pathmod}")
    except OSError as exc:  # handles the error if the directory already exists
        if exc.errno != errno.EEXIST:
            raise
        pass
    logincrement = 1
    padstring = pathpadder (lognum,logincrement)
    while os.path.exists(f"{currentdir}{pathmod}log {today} - {padstring}{logincrement}.txt"):
        logincrement += 1
        padstring = pathpadder (lognum,logincrement)
    log = open(f"{currentdir}{pathmod}log {today} - {padstring}{logincrement}.txt", "w")
    log.write(f"GreedySim version {version}. Log number {logincrement}. Date: {today}. Time: {smalltime}. ")
    if runs > 1:
        log.write(f"Log Number: {playcount+1}.\n")
    else:
        log.write('\n')
    log.write(f"\'Too Greedily, Too Deep\' copyright Sydney Cardew.\n")
    return [log,pathmod,today,padstring,logincrement]

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
multimode = config['DEFAULT']['multimode']
# arguments
parser = argparse.ArgumentParser(prog="GreedySim") # the subsequent lines contain the command line arguments
parser.add_argument("-m", "--multiple", action='store_true', help = "runs multiple times (set in config.ini)")
parser.add_argument("-v","--version", action='version',version=version)
args = parser.parse_args()
if args.multiple: #sets to run the simulation multiple times in a row
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
    #name, type, gamesize, maintext, delve1, delve2, delve3, cost, deck
    newentry = card(n[0],n[1],n[2],n[3],n[5],n[6],n[7],n[8][:-1],n[10])
    if players == 2 and newentry.gamesize == '3+' or newentry.gamesize == '4+': # removes the appropriate cards for a 2 player game
        pass
    elif players == 3 and newentry.gamesize == '4+': # removes the appropriate cards for a 3 player game
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

#SETUP MASS LOGGING VARIABLES AND MULTIMODE
if runs > 1:
    summaryarray = []
    if multimode == 'spread': #This cuts up the runs into games with different numbers of players
        multispread = True
        multirandom = False
        multiarray = []
        multisegment = runs // 4
        multiremainder = runs - (multisegment * 4)
        for x in range(2, 6):
            builderarray = []
            builderarray = [x] * multisegment
            multiarray.extend(builderarray)
        if multiremainder == 0:
            pass
        else:
            builderarray = []
            builderarray = [5] * multiremainder
            multiarray.extend(builderarray)
    elif multimode == 'random':
        multirandom = True
        multispread = False
    elif multimode == 'normal':
        multispread =  False
        multirandom = False
    else:
        print(f"Multimode setting error.")
        multirandom = False
        multispread = False
else:
    multirandom,multispread = False,False

#LOOP

setpath = False # initialises the special subdirectory for multiple runs
playing = True
playcount = 0
deaths,totaltreasure = 0,0
while playing:

    pathpack = loginit(currentdir,version,lognum,runs,playcount,setpath)
    log, pathmod,today,padstring,logincrement = pathpack[0],pathpack[1],pathpack[2],pathpack[3],pathpack[4]
    setpath = True

    #DECK SETUP
    expeditiondeck = list(expeditioncards.keys())
    artefactdeck = list(artefactcards.keys())
    missiondeck = list(missioncards.keys())
    leaderdeck = list(leadercards.keys())
    peondeck = list(peoncards.keys())
    basicdeck = list(basiccards.keys())
    advanceddeck = list(advancedcards.keys())

    #PREGAME

    if multispread == True:
        players = multiarray[playcount]
    elif multirandom == True:
        players = randint(2,5)
    else:
        pass
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
    delvepack = expedition(players,playerinfo,expeditiondeck,delveindicator,firstout)
    firstout, expeditiondeck, playerinfo = delvepack[0],delvepack[1],delvepack[2]
    resolvestats = resolve(playerinfo,delveindicator,deaths,totaltreasure)
    deaths,totaltreasure = resolvestats[0],resolvestats[1]
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
    delvepack = expedition(players,playerinfo,expeditiondeck,delveindicator,firstout)
    firstout, expeditiondeck, playerinfo = delvepack[0], delvepack[1], delvepack[2]
    resolvestats = resolve(playerinfo,delveindicator,deaths,totaltreasure)
    deaths,totaltreasure = resolvestats[0],resolvestats[1]
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
    delvepack = expedition(players,playerinfo,expeditiondeck,delveindicator,firstout)
    firstout, expeditiondeck, playerinfo = delvepack[0], delvepack[1], delvepack[2]
    resolvestats = resolve(playerinfo,delveindicator,deaths,totaltreasure)
    deaths,totaltreasure = resolvestats[0],resolvestats[1]
    log.close()
    if runs > 1:
        gamediff = len(str(runs)) - len(str(playcount))
        gamepad = '0' * gamediff
        summary = (f"Game {gamepad}{playcount}/{runs}: {players} players. {deaths} adventurer deaths. {totaltreasure} items of loot recovered.")
        summaryarray.append(summary)
        deaths,totaltreasure = 0,0
    if playcount == runs:
        playing = False

# WRITE MASS LOG

if runs > 1:
    masslog = open(f"{currentdir}{pathmod}Summary {today} - {padstring}{logincrement}.txt", "w")
    for x in range (len(summaryarray)):
        masslog.write(f"{summaryarray[x]}\n")
    masslog.close()

