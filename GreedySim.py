import os
import csv
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

# CARDS

currentdir = os.getcwd()
tabledata = readcsv(currentdir) # reads the CSV file
processeddata = []
counter = 0
for x in tabledata: # processes the data
    counter += 1
    padding = len(str(len(tabledata))) - len(str(counter))
    procstring = (f"{padding * '0'}{counter} {x[0]},{x[1]},{x[2]},{x[3]},{x[4]},{x[5]},{x[6]},{x[7]},{x[8]},{x[10]}")
    processeddata.append(procstring)
tuplelist = []
expeditioncards,artefactcards,leadercards,basiccards,advancedcards = {},{},{},{},{}
for n in processeddata:
    newkey = n[0:3]
    newentry = n[4:].split(",")
    if newentry[9] == 'Null' or newentry[9] == 'Treasure' or newentry[9] == 'Item' or newentry[9] == 'Hazard':
        expeditioncards.update({newkey : newentry})
    if newentry[9] == 'Artefact':
        artefactcards.update({newkey : newentry})
print (expeditioncards['009'][2])



