import argparse
import configparser
import csv
import errno
import os
import requests
from datetime import date
from datetime import datetime
from random import randint
from random import seed

# CLASSES

class player: #the player class
    def __init__(self,recklessness,malice,greed,height,gold,party,health,treasures,items,capacity,burden,
                 mitigationEN,mitigationST,mitigationMA,mitigationMY,totalhealth):
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
    csv.register_dialect('card',delimiter=",",  quoting=csv.QUOTE_NONE) #creates a csv dialect that seperates on commas
    with open('cards.csv', newline='') as csvfile:
        csvobject = csv.reader(csvfile, dialect='card')  #creates a csv object
        for row in csvobject:
            tabledata.append(row)
    return tabledata

def seedget():
    r =requests.get('https://www.random.org/integers/?num=1&min=10000&max=99999&col=5&base=10&format=plain&rnd=new')
    if r.status_code == 200:
        requestsuccess = True
    else:
        requestsuccess = False
    if requestsuccess == True:
        for line in r:
            randomread = str(line)
        randseed = int(randomread[2:7])
    else:
        seed()
        randseed = randint(10000,99999)
    return randseed

def shuffle(cards): #card shuffling routine
    shuffcards = []
    while len(cards) > 0:
        select = randint (0, len(cards))
        shuffcards.append(cards.pop(select-1))
    return shuffcards

def personality(players,player1p,player2p,player3p,player4p,player5p): #Initialises the player classes and calls the personality routines
    player1p += '()';player2p += '()';player3p += '()';player4p += '()';player5p += '()'
    player1person = eval((player1p))
    player1 = player(player1person[0],player1person[1],player1person[2],
                     player1person[3],0,[],[],[],[],0,0,0,0,0,0,0)
    player2person = eval((player2p))
    player2 = player(player2person[0],player2person[1],player2person[2],
                     player2person[3],0,[],[],[],[],0,0,0,0,0,0,0)
    player3person = eval((player3p))
    player3 = player(player3person[0],player3person[1],player3person[2],
                     player3person[3],0,[],[],[],[],0,0,0,0,0,0,0)
    player4person = eval((player4p))
    player4 = player(player4person[0],player4person[1],player4person[2],
                     player4person[3],0,[],[],[],[],0,0,0,0,0,0,0)
    player5person = eval((player5p))
    player5 = player(player5person[0],player5person[1],player5person[2],
                     player5person[3],0,[],[],[],[],0,0,0,0,0,0,0)
    playerinfo = [player1,player2,player3,player4,player5]
    return playerinfo

def random():
    recklessness = randint (1,100)
    malice = randint(1,100)
    greed = randint(1,100)
    height = randint(140,220)
    personality = [recklessness,malice,greed,height]
    return personality

def aggressive():
    recklessness = randint (50,100)
    malice = randint (50,100)
    greed = randint (30,80)
    height = randint(140,220)
    personality = [recklessness,malice,greed,height]
    return personality

def leaderpick(players,playerinfo,leaderdeck): # the players pick their leaders
    for player in range(players):
        if playerinfo[player].greed > 60 and playerinfo[player].recklessness > 50 and '122' in leaderdeck: #picks Lady Minewater
            playerinfo[player].party.append(leaderdeck.pop(leaderdeck.index('122')))
            playerinfo[player].health.append(2)
        elif playerinfo[player].greed > 50 and '125' in leaderdeck: #picks Ulgrim the Auctioneer
            playerinfo[player].party.append(leaderdeck.pop(leaderdeck.index('125')))
            playerinfo[player].health.append(2)
        elif playerinfo[player].malice > 40 and '121' in leaderdeck: #picks 'Lucky' Dhorzan
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
    hr()
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
    for tavcards in tavernspread: # logs the cards in the tavern tableau, in the appropriate rows
        try:
            log.write(f"{mastercards[tavcards].name}")
            if (tavernspread.index(tavcards)) < len(tavernspread)-1 and (tavernspread.index(tavcards)+1) % players != 0:
                log.write(', ')
            elif (tavernspread.index(tavcards)) < len(tavernspread) - 1 and (tavernspread.index(tavcards)+1) % players == 0:
                log.write(',\n')
            else:
                log.write('.\n')
        except KeyError:
            log.write(f"!!!UNKNOWN ERROR IN TAVERN SPREAD FUNCTION {tavcards}!!!")
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
    else: # this is if only one player has the largest total gold
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
    for j in range (len(playerinfo)): # reads out party make-ups
        log.write(f"Player {j+1}'s party consists of:\n")
        for dwarf in range (len(playerinfo[j].party)):
            log.write(f"{mastercards[playerinfo[j].party[dwarf]].name} "
                      f"| ({playerinfo[j].health[dwarf]}) Health")
            if dwarf < len(playerinfo[j].party)-1:
                log.write(', ')
            else:
                log.write('.\n')
        log.write(f"They have {playerinfo[j].gold} gold remaining.\n")
        bl(1)
    tavernpack = [playerinfo, peondeck, basicdeck, advanceddeck]
    return tavernpack

def expedition(players,playerinfo,expeditiondeck,delveindicator,firstout): #Controls the expedition phase
    playcounter = 1
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
        log.write(f"Play commences. Player {playlist[position]} is the tallest "
                  f"at {heightlist[position]}cm and thus goes first.\n")
    else:
        if firstout > 0:
            position = firstout
            log.write(f"Play commences. Player {playlist[position]} was first "
                      f"out of the mine last delve and thus goes first.\n")
        elif firstout == 0:
            position = randint(0,players-1)
            log.write(f"Play commences. Since all players were lost on the previous delve, "
                      f"they roll dice. Player {playlist[position]} wins, and thus goes first.\n")
    stacks = []
    for t in range(players): # creates an appropriate number of empty lists to hold stacks
        stacks.append([])
    discardpile = []
    playing = True
    while playing: # The expedition loop
        for party in range (len(playerinfo)):
            playerinfo[party].healthget()
        if playcounter == 1: # writes the round number after all players have gone
            hr()
            log.write(f"Round {roundcounter}")
            roundcounter += 1
        bl(1)
        takenflag = False
        voidedflag = False
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
                        log.write(f"Player {playlist[position]} reaches the end of the deck, and "
                                  f"replenishes it from the discard pile. The Darkness Hungers!\n")
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
                if len(stacks[a]) == 1 and voidedflag == False:
                    if mastercards[stacks[a][0]].type == 'Null':
                        airoll = randint (1,100)
                        try:
                            if playerinfo[playlist[position]].greed >= airoll:
                                discardpile.extend(stacks[a])
                                stacks[a] = []
                                log.write(f"Player {playlist[position]} voids stack {stacks.index(stacks[a])+1}.\n\n")
                                voidedflag = True
                            else:
                                pass
                        except IndexError:
                            pass
                    elif mastercards[stacks[a][0]].type == 'Hazard':
                        airoll = randint (1,100)
                        try:
                            if playerinfo[playlist[position]].recklessness <= airoll:
                                discardpile.extend(stacks[a])
                                stacks[a] = []
                                log.write(f"Player {playlist[position]} voids stack {stacks.index(stacks[a])+1}.\n\n")
                                voidedflag = True
                            else:
                                pass
                        except IndexError:
                            pass
                if len(stacks[a]) >= 6 and takenflag == False:
                    stackstats = stats(stacks, delveindicator)
                    discardables = takestack(stacks[a],a,position,playerinfo,stackstats,playlist)
                    discardpile.extend(discardables)
                    stacks[a] = []
                    takenflag = True
            try:
                playerinfo[playlist[position]].healthget()
                if playerinfo[playlist[position]].totalhealth > 0:
                    pass
                elif playerinfo[playlist[position]].totalhealth == 0:
                    log.write (f"Player {playlist[position]}'s party has been wiped out! "
                               f"They limp back to the surface...\n")
                    playlist.pop(position)
            except IndexError:
                pass
            try:
                if (playerinfo[playlist[position]].capacity - playerinfo[playlist[position]].burden) < 2 \
                        and sum(playerinfo[playlist[position]-1].health) > 0:
                    log.write (f"Player {playlist[position]} attempts to escape the dungeon!\n")
                    discardpile = escapesequence(position,playerinfo,expeditiondeck,playlist,discardpile,delveindicator)
                    escapedcount += 1
                    playlist.pop(position)
                    if escapeflag == False:
                        firstout = position
                        escapeflag = True
            except IndexError:
                pass
        position += 1
        playcounter += 1
        if position >= len(playlist):
            position = 0
        if playcounter > len(playlist)+1:
            playcounter = 1
        log.write (f"Discard pile: {len(discardpile)}\n")
        log.write (f"Deck: {len(expeditiondeck)}\n")
    log.write (f"Expedition phase delve {delveindicator} over.\n")
    log.write (f"{escapedcount} parties made it back to the surface in relative safety.\n")
    log.write (f"{players-escapedcount} parties crawled bleeding from the haunted depths!\n")
    expeditiondeck.extend(discardpile)
    bl(1)
    delvepack = [firstout,expeditiondeck,playerinfo,roundcounter]
    return delvepack

def escapesequence(position,playerinfo,expeditiondeck,playlist,discardpile,delveindicator):
    delvestring = 'delve'+str(delveindicator)
    escapelength = len(playerinfo[playlist[position]].treasures)
    if len(playerinfo[playlist[position]].treasures) == 0:
        escapelength = 2
    for x in range (escapelength):
        carddraw = expeditiondeck.pop(-1)
        log.write(f"Player {playlist[position]} draws {mastercards[carddraw].name}\n")
        if mastercards[carddraw].type == 'Hazard':
            hazard = 0
            endamage, stdamage, madamage, mydamage = 0, 0, 0, 0
            hazard += sum([int(s) for s in getattr(mastercards[carddraw], delvestring) if s.isdigit()])
            if len(getattr(mastercards[carddraw],delvestring)) == 7:  # interprets hazard strings with two parts
                hazstring1 = getattr(mastercards[carddraw], delvestring)[1:3]
                hazstring2 = getattr(mastercards[carddraw], delvestring)[5:7]
                haznum1 = int(getattr(mastercards[carddraw], delvestring)[0])
                haznum2 = int(getattr(mastercards[carddraw], delvestring)[4])
                if hazstring1 == 'EN':
                    endamage += haznum1
                elif hazstring1 == 'ST':
                    stdamage += haznum1
                elif hazstring1 == 'MA':
                    madamage += haznum1
                elif hazstring1 == 'MY':
                    mydamage += haznum1
                if hazstring2 == 'EN':
                    endamage += haznum2
                elif hazstring2 == 'ST':
                    stdamage += haznum2
                elif hazstring2 == 'MA':
                    madamage += haznum2
                elif hazstring2 == 'MY':
                    mydamage += haznum2
                totalhazard = haznum1 + haznum2
            elif len(getattr(mastercards[carddraw],delvestring)) == 3:  # interprets hazard strings with one part
                hazstring1 = getattr(mastercards[carddraw], delvestring)[1:3]
                haznum1 = int(getattr(mastercards[carddraw], delvestring)[0])
                if hazstring1 == 'EN':
                    endamage += haznum1
                elif hazstring1 == 'ST':
                    stdamage += haznum1
                elif hazstring1 == 'MA':
                    madamage += haznum1
                elif hazstring1 == 'MY':
                    mydamage += haznum1
                totalhazard = haznum1
            startdamage = totalhazard
            enmit = playerinfo[playlist[position]].mitigationEN
            stmit = playerinfo[playlist[position]].mitigationST
            mamit = playerinfo[playlist[position]].mitigationMA
            mymit = playerinfo[playlist[position]].mitigationMY
            log.write(f"They take {startdamage} hazard from the card.\n")
            log.write(f"{endamage} EN Hazard\n")
            log.write(f"{stdamage} ST Hazard\n")
            log.write(f"{madamage} MA Hazard\n")
            log.write(f"{mydamage} MY Hazard\n")
            mitigationtot = (enmit + stmit + mamit + mymit)
            finaldamage = startdamage - mitigationtot
            log.write(f"They mitigate {mitigationtot} hazard. {finaldamage} hazard remaining.\n")
            if finaldamage > 0:
                log.write('Rolling dice.\n')
                damage = 0
                for hazdice in range(finaldamage):
                    diceroll = randint(1, 6)
                    log.write(f"{diceroll}")
                    if hazdice < finaldamage - 1:
                        log.write(', ')
                    else:
                        log.write('.\n')
                    if diceroll >= 5:
                        damage += 1
                if damage > 0:
                    if '145' in playerinfo[playlist[position]].party:  # Deploys the paladin's special power
                        log.write(f"The paladin absorbs 1 point of damage!\n")
                        damage -= 1
                    log.write(f"They take {damage} damage.\n")
                    playerinfo[position].takedamage(damage)
                    log.write(f"{playerinfo[position].health}")
                else:
                    log.write('They take no damage.\n')
            else:
                log.write('They mitigate all hazard, and take no damage.\n')
        discardpile.append(carddraw)
    log.write(f"placeholder. Escape of player {playlist[position]} successful.\n")
    return discardpile

def takestack(stacka,stackid,position,playerinfo,stackstats,playlist): #This function 'takes' a stack and deals with the consequences
    try:
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
            enmit = playerinfo[playlist[position]].mitigationEN
            stmit = playerinfo[playlist[position]].mitigationST
            mamit = playerinfo[playlist[position]].mitigationMA
            mymit = playerinfo[playlist[position]].mitigationMY
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
                    if '145' in playerinfo[playlist[position]].party: # Deploys the paladin's special power
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
        if stackstats[0][stackid].items > 0:
            log.write (f"They pick up {stackstats[0][stackid].items} items!\n")
            for carditem in range (len(stacka)):
                if mastercards[stacka[carditem]].deck == 'Item':
                    log.write(f"{mastercards[stacka[carditem]].name}\n")
                    playerinfo[playlist[position]].items.append(stacka.pop(carditem))
        stackreward = stackstats[0][stackid].reward
        log.write (f"They have the pick of {stackreward}G worth of treasure!\n")
        treasurelist = []
        for cardtreasure in range (len(stacka)):
            if mastercards[stacka[cardtreasure]].deck == 'Treasure' or mastercards[stacka[cardtreasure]].deck == 'Artefact':
                log.write(f"{mastercards[stacka[cardtreasure]].name}\n")
                treasurelist.append(stacka[cardtreasure])
        for cardsremaining in stacka:
            if cardsremaining in treasurelist:
                del cardsremaining
        playerinfo[playlist[position]].setburden()
        localcapacity = playerinfo[playlist[position]].capacity - playerinfo[playlist[position]-1].burden
        if localcapacity < 0:
            localcapacity = 0
        bl(1)
        log.write (f"Player can pick up {localcapacity} treasures.\n")
        for x in range (localcapacity):
            try:
                playerinfo[playlist[position]].treasures.append(treasurelist.pop(-1))
                log.write (f"Player {playlist[position]} took {mastercards[playerinfo[playlist[position]].treasures[-1]].name}!\n")
            except IndexError:
                pass
        playerinfo[playlist[position]].setburden()
        log.write (f"Player has {playerinfo[playlist[position]].capacity} total capacity "
                   f"and is carrying {playerinfo[playlist[position]].burden} loot.\n")
        while playerinfo[playlist[position]].burden > playerinfo[playlist[position]].capacity:
            log.write(f"Player drops {mastercards[playerinfo[playlist[position]].treasures[-1]].name}!")
            playerinfo[playlist[position]].treasures.pop()
        bl(1)
        stacka.extend(treasurelist)
    except IndexError:
        log.write (f"\n!!!UNKNOWN FAULT IN TAKESTACK FUNCTION!!!.\n")
        for x in range (len(playlist)):
            log.write (f"{playlist[x]-1} ")
        for y in range (len(playerinfo)):
            log.write (f"{y} ")
        log.write (f"({position})\n")
    return stacka

def stats(stacks,delveindicator):#this routine helps the AI make judgements about where to put cards
    delvestring = 'delve'+str(delveindicator)
    statblock = []
    hazardstats = [0] * len(stacks)
    rewardstats = [0] * len(stacks)
    itemnum = [0] * len(stacks)
    for n in range(len(stacks)):
        if stacks[n] == []: #assigns small random values to an empty stack to add some pseudo-randomness to the AI
            substats = stack(0,randint(1,3),randint(1,10),randint(1,3),len(stacks[n]),0,0,0,0)
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

def resolve(playerinfo,delveindicator,deaths,totaltreasure,roundcounter,roundarray): # the resolution phase
    hr()
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
    roundarray.append(roundcounter)
    resolvestats = [deaths,totaltreasure,roundarray]
    return resolvestats

def bl(num): # inserts blank lines to help format the log file
    for x in range (num):
        log.write('\n\n')

def hr(): # inserts a horizontal rule to help format the log file
    log.write("\n----------------\n\n")

def pathpadder(lognum,logincrement): #this routine pads out the number in the log file names
    pad = lognum - len(str(logincrement))
    padstring = '0' * pad
    return padstring

def loginit(currentdir,version,lognum,runs,playcount,setpath,randseed):
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
    log.write(f"\nSeed: {randseed}\n")
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
setseed = config['DEFAULT']['setseed']

# arguments

parser = argparse.ArgumentParser(prog="GreedySim") # the subsequent lines contain the command line arguments
parser.add_argument("-m", "--multiple", action='store_true', help = "runs multiple times (set in config.ini)")
rangroup = parser.add_mutually_exclusive_group()
rangroup.add_argument("-r", "--truerandom", action='store_true',help = "initialises GreedySim with a truly random number from random.org")
rangroup.add_argument("-s", "--setseed", action = 'store_true',help = "initialises GreedySim with a seed from config.ini")
parser.add_argument("-v", "--version", action='version',version=version)
args = parser.parse_args()
if args.multiple: #sets to run the simulation multiple times in a row
    runs = timesnum
else:
    runs = 1
if args.truerandom: #gets true random number
    randseed = seedget()
    seed(randseed)
elif args.setseed:
    randseed = setseed
    seed(setseed)
else:
    seed()


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
roundarray = []
while playing:

    pathpack = loginit(currentdir,version,lognum,runs,playcount,setpath,randseed)
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
    hr()
    log.write (f"There are {players} players.\n")
    log.write (f"Their personalities are: ")
    for playpersonality in range (players):
        playerstring = 'player' + str(playpersonality+1) + 'p'
        log.write (f"{eval(playerstring)}")
        if playpersonality < players - 1:
            log.write(', ')
        else:
            log.write('.\n')
    hr()
    playerinfo = personality(players,player1p,player2p,player3p,player4p,player5p)
    playerinfo = leaderpick(players,playerinfo,leaderdeck)
    for n in range (int(players)):
        log.write(f"Player {n+1} has {playerinfo[n].recklessness} recklessness, {playerinfo[n].malice} "
                  f"malice and {playerinfo[n].greed} greed, is {playerinfo[n].height}cm tall and has picked "
                  f"{mastercards[playerinfo[n].party[0]].name}.\n")

    # DELVE 1

    hr()
    log.write ('Delve 1 Begins\n')
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
    firstout, expeditiondeck, playerinfo, roundcounter = delvepack[0], delvepack[1], delvepack[2], delvepack[3]
    resolvestats = resolve(playerinfo,delveindicator,deaths,totaltreasure,roundcounter,roundarray)
    deaths,totaltreasure,roundarray = resolvestats[0],resolvestats[1],resolvestats[2]
    expeditiondeck = list(expeditioncards.keys())

    # DELVE 2

    log.write ('Delve 2 Begins\n')
    bl(1)
    delveindicator += 1
    expeditiondeck = shuffle(expeditiondeck)
    artefactdeck = shuffle(artefactdeck)
    for x in range (1,4):
        artefactadd = artefactdeck.pop(0)
    expeditiondeck.append(artefactadd)
    expeditiondeck = shuffle(expeditiondeck)
    peondeck = shuffle(peondeck)
    basicdeck = shuffle(basicdeck)
    advanceddeck = shuffle(advanceddeck)
    tavernpack = tavern(players,playerinfo,peondeck,basicdeck,advanceddeck,delveindicator)
    playerinfo, peondeck, basicdeck, advanceddeck = tavernpack[0], tavernpack[1], tavernpack[2], tavernpack[3]
    delvepack = expedition(players,playerinfo,expeditiondeck,delveindicator,firstout)
    firstout, expeditiondeck, playerinfo, roundcounter = delvepack[0], delvepack[1], delvepack[2], delvepack[3]
    resolvestats = resolve(playerinfo,delveindicator,deaths,totaltreasure,roundcounter,roundarray)
    deaths,totaltreasure,roundarray = resolvestats[0],resolvestats[1],resolvestats[2]
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
    firstout, expeditiondeck, playerinfo, roundcounter = delvepack[0], delvepack[1], delvepack[2], delvepack[3]
    resolvestats = resolve(playerinfo,delveindicator,deaths,totaltreasure,roundcounter,roundarray)
    deaths,totaltreasure,roundarray = resolvestats[0],resolvestats[1],resolvestats[2]
    log.close()
    if runs > 1: #handles tidying up the loop in -m mode
        roundaverage = sum(roundarray)/len(roundarray) # gets the mean of the number of rounds played
        roundaverage2sf = "{:.2f}".format(roundaverage) # rounds the mean to two decimal places
        gamediff = len(str(runs)) - len(str(playcount))
        gamepad = '0' * gamediff
        summary = (f"Game {gamepad}{playcount}/{runs}: {players} players. {deaths} adventurer deaths. "
                   f"{totaltreasure} items of loot recovered. Average rounds per delve: {roundaverage2sf}")
        summaryarray.append(summary)
        deaths,totaltreasure = 0,0
        roundarray.clear()
    if playcount == runs: #ends the loop in -m mode
        playing = False

# WRITE MASS LOG

if runs > 1:
    masslog = open(f"{currentdir}{pathmod}Summary {today} - {padstring}{logincrement}.txt", "w")
    for x in range (len(summaryarray)):
        masslog.write(f"{summaryarray[x]}\n")
    masslog.close()