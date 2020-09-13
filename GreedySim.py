import os
import csv
import configparser
from random import seed
from random import randint


class player:
    def __init__(self,recklessness,malice,greed,height,gold,party,health,treasures,items):
        self.recklessness = recklessness
        self.malice = malice
        self.greed = greed
        self.height = height
        self.gold = gold
        self.party = party
        self.health = health
        self.treasures = treasures
        self.items = items

class card:
    def __init__(self,name,type,gamesize,delve1,delve2,delve3,cost,deck):
        self.name = name
        self.type = type
        self.gamesize = gamesize
        self.delve1 = delve1
        self.delve2 = delve2
        self.delve3 = delve3
        self.cost = cost
        self.deck = deck

# FUNCTIONS

def readcsv(currentdir): #reads the csv file
    os.chdir(currentdir) #moves to the main directory
    tabledata = [] #initialises the 'tabledata' list
    csv.register_dialect('card',delimiter=",", escapechar="*",  quoting=csv.QUOTE_NONE) #creates a csv dialect that seperates files on commas and uses * as an escape character
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
    player1 = player(player1person[0],player1person[1],player1person[2],player1person[3],0,[],[],[],[])
    player2person = eval((player2p))
    player2 = player(player2person[0],player2person[1],player2person[2],player2person[3],0,[],[],[],[])
    player3person = eval((player3p))
    player3 = player(player3person[0],player3person[1],player3person[2],player3person[3],0,[],[],[],[])
    player4person = eval((player4p))
    player4 = player(player4person[0],player4person[1],player4person[2],player4person[3],0,[],[],[],[])
    player5person = eval((player5p))
    player5 = player(player5person[0],player5person[1],player5person[2],player5person[3],0,[],[],[],[])
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
    playerchoice = ['000'] * players
    for x in range(players):
        if playerinfo[x].greed > 60 and playerinfo[x].recklessness > 50 and '122' in leaderdeck:
            playerinfo[x].party.append(leaderdeck.pop(leaderdeck.index('122')))
        elif playerinfo[x].greed > 50 and '125' in leaderdeck:
            playerinfo[x].party.append(leaderdeck.pop(leaderdeck.index('125')))
        elif playerinfo[x].malice > 40 and '121' in leaderdeck:
            playerinfo[x].party.append(leaderdeck.pop(leaderdeck.index('121')))
        else:
            playerinfo[x].party.append(leaderdeck.pop(0))
        if playerchoice[x] == '122':
            playerinfo[x].gold = 40
        else:
            playerinfo[x].gold = 30
    return playerinfo

def tavern(players,playerinfo,peondeck,basicdeck,advanceddeck,delveindicator): # controls the hiring phase
    print (f"Hiring phase, delve {delveindicator}.")
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
            tavernspread.append(advanceddeck.pop(-1))
    print ('Tavern contains:')
    for z in tavernspread:
        print(f"{mastercards[z].name} ",end='')
    print('')
    goldlist = []
    for n in range (players):
        goldlist.append(playerinfo[n].gold)
    position = goldlist.index(max(goldlist))
    picklist = [True] * players
    while True in picklist:
        for p in range (len(tavernspread)):
            try:
                cost = int(mastercards[tavernspread[p-1]].cost) # retrieves the cost of the card
                if cost < playerinfo[position].gold: #checks the cost of the card against the goldreserve of the player
                    playerinfo[position].party.append(tavernspread.pop(p-1)) #removes the listing from the tavern spread and adds to player info
                    playerinfo[position].gold -= cost #decreases the player's gold
                    print(f"player {position+1} buys {mastercards[playerinfo[position].party[-1]].name}")
                    break
                elif cost == playerinfo[position].gold:
                    diceroll = randint (1,100)
                    if diceroll <= playerinfo[position].recklessness:
                        playerinfo[position].party.append(tavernspread.pop(p - 1))  # removes the listing from the tavern spread and adds to player info
                        playerinfo[position].gold -= cost  # decreases the player's gold
                        print(f"player {position + 1} buys {mastercards[playerinfo[position].party[-1]].name}")
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
    print('Hiring phase concludes')
    for j in range (players):
        print(f"Player {j+1}'s party consists of:")
        for k in range (len(playerinfo[j].party)):
            print(f"{mastercards[playerinfo[j].party[k]].name}",end='')
            if k < len(playerinfo[j].party)-1:
                print(', ',end='')
            else:
                print('.',end='')
        print(f"\nThey have {playerinfo[j].gold} gold remaining")
        print('')

    pass

def expedition(players,playerinfo,expeditiondeck):
    pass

currentdir = os.getcwd()
config = configparser.ConfigParser()  # the following lines extract the settings from the config file
config.read('Settings/config.ini')
players = int(config['DEFAULT']['players'])
player1p = config['DEFAULT']['player1']
player2p = config['DEFAULT']['player2']
player3p = config['DEFAULT']['player3']
player4p = config['DEFAULT']['player4']
player5p = config['DEFAULT']['player5']

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
    newentry = card(n[0],n[1],n[2],n[5],n[6],n[7],n[8][:-1],n[10])
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
expeditiondeck = list(expeditioncards.keys())
artefactdeck = list(artefactcards.keys())
missiondeck = list(missioncards.keys())
leaderdeck = list(leadercards.keys())
peondeck = list(peoncards.keys())
basicdeck = list(basiccards.keys())
advanceddeck = list(advancedcards.keys())
print(artefactdeck)

#PREGAME
delveindicator = 1
playerinfo = personality(players,player1p,player2p,player3p,player4p,player5p)
print (f"There are {players} players.")
playerinfo = leaderpick(players,playerinfo,leaderdeck)
for n in range (int(players)):
    print(f"Player {n+1} has {playerinfo[n].recklessness} recklessness, {playerinfo[n].malice} malice and {playerinfo[n].greed} greed, is {playerinfo[n].height}cm tall and has picked {mastercards[playerinfo[n].party[0]].name}.")
#DELVE1
print ('Delve 1 Begins')
expeditiondeck = shuffle(expeditiondeck)
artefactdeck = shuffle(artefactdeck)
artefactadd = artefactdeck.pop(0)
expeditiondeck.append(artefactadd)
expeditiondeck = shuffle(expeditiondeck)
peondeck = shuffle(peondeck)
basicdeck = shuffle(basicdeck)
partylist = tavern(players,playerinfo,peondeck,basicdeck,advanceddeck,delveindicator)
delvelist = expedition(players,playerinfo,expeditiondeck)



