import os
import csv
import configparser
from random import seed
from random import randint

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

def personality(players,player1,player2,player3,player4,player5):
    # player personalities : [0] is 'recklnessness', [1] is 'malice', [2] is 'greed', [3] is 'height'
    player1 += '()';player2 += '()';player3 += '()';player4 += '()';player5 += '()'
    player1person = eval((player1))
    player2person = eval((player2))
    player3person = eval((player3))
    player4person = eval((player4))
    player5person = eval((player5))
    playerinfo = [player1person,player2person,player3person,player4person,player5person]
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
    #leaders are stored in playerinfo [5], gold in playerinfo [4]
    playerchoice = ['000'] * players
    for x in range(players):
        if playerinfo[players-1][2] > 60 and playerinfo[players-1][0] > 50 and '122' in leaderdeck:
            playerchoice[x] = leaderdeck.pop(leaderdeck.index('122'))
        elif playerinfo[players-1][2] > 50 and '125' in leaderdeck:
            playerchoice[x] = leaderdeck.pop(leaderdeck.index('125'))
        elif playerinfo[players-1][1] > 40 and '121' in leaderdeck:
            playerchoice[x] = leaderdeck.pop(leaderdeck.index('121'))
        else:
            playerchoice[x] = leaderdeck.pop(0)
        if playerchoice[x] == '122':
            playerinfo[x].append(40)
        else:
            playerinfo[x].append(30)
        playerinfo[x].append(playerchoice[x])
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
        print(f"{mastercards[z][0]} ",end='')
    print('')
    goldlist = []
    for n in range (players):
        goldlist.append(playerinfo[n][3])
    position = goldlist.index(max(goldlist))
    picklist = [True] * players
    while True in picklist:
        for p in range (len(tavernspread)):
            try:
                cost = int(mastercards[tavernspread[p-1]][8][:-1]) # retrieves the cost of the card
                if cost < playerinfo[position][4]: #checks the cost of the card against the goldreserve of the player
                    playerinfo[position].append(tavernspread.pop(p-1)) #removes the listing from the tavern spread and adds to player info
                    playerinfo[position][4] -= cost #decreases the player's gold
                    print(f"player {position+1} buys {mastercards[playerinfo[position][-1]][0]}")
                    break
                else:
                    picklist[position] = False
            except IndexError:
                if len(playerinfo[position]) > 5:
                    picklist[position] = False
        position += 1
        if position > players-1:
            position = 0
    print('Hiring phase concludes')
    pass

def expedition(players,playerinfo,expeditiondeck):
    pass

currentdir = os.getcwd()
config = configparser.ConfigParser()  # the following lines extract the settings from the config file
config.read('Settings/config.ini')
players = int(config['DEFAULT']['players'])
player1 = config['DEFAULT']['player1']
player2 = config['DEFAULT']['player2']
player3 = config['DEFAULT']['player3']
player4 = config['DEFAULT']['player4']
player5 = config['DEFAULT']['player5']

# This section of the program extracts information about the cards from the csv file and creates dictionaries and arrays for use by the rest of the program
tabledata = readcsv(currentdir) # reads the CSV file
processeddata = []
counter = 0
for x in tabledata: # processes the data
    counter += 1
    padding = len(str(len(tabledata))) - len(str(counter))
    procstring = (f"{padding * '0'}{counter} {x[0]},{x[1]},{x[2]},{x[3]},{x[4]},{x[5]},{x[6]},{x[7]},{x[8]},{x[10]}")
    processeddata.append(procstring)
tuplelist = []
expeditioncards,artefactcards,missioncards,leadercards,peoncards,basiccards,advancedcards,mastercards = {},{},{},{},{},{},{},{}
for n in processeddata:
    newkey = n[0:3]
    newentry = n[4:].split(",")
    if newentry[9] == 'Null' or newentry[9] == 'Treasure' or newentry[9] == 'Item' or newentry[9] == 'Hazard':
        expeditioncards.update({newkey : newentry})
    elif newentry[9] == 'Artefact':
        artefactcards.update({newkey : newentry})
    elif newentry[9] == 'Mission':
        missioncards.update({newkey : newentry})
    elif newentry[1] == 'Expedition Leader':
        leadercards.update({newkey : newentry})
    elif newentry[1] == 'Peon':
        peoncards.update({newkey : newentry})
    elif newentry[1] == 'Basic Adventurer':
        basiccards.update({newkey: newentry})
    elif newentry[1] == 'Advanced Adventurer':
        advancedcards.update({newkey: newentry})
    mastercards.update({newkey : newentry})
expeditiondeck = list(expeditioncards.keys())
artefactdeck = list(artefactcards.keys())
missiondeck = list(missioncards.keys())
leaderdeck = list(leadercards.keys())
peondeck = list(peoncards.keys())
basicdeck = list(basiccards.keys())
advanceddeck = list(advancedcards.keys())

#PREGAME
delveindicator = 1
playerinfo = personality(players,player1,player2,player3,player4,player5)
print (f"There are {players} players.")
playerinfo = leaderpick(players,playerinfo,leaderdeck)
for n in range (int(players)):
    print(f"Player {n+1} has {playerinfo[n][0]} recklessness, {playerinfo[n][1]} malice and {playerinfo[n][2]} greed, is {playerinfo[n][3]}cm tall and has picked {mastercards[playerinfo[n][5]][0]}")
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



