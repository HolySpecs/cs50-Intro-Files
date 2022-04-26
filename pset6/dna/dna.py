#imported modules
from csv import reader
from sys import argv, exit
from os.path import exists

#Check if the crrect amount of arguements are given
if len(argv) != 3:
    print("Usage: python dna.py data.csv sequence.txt")
    exit(1)

#Check if the files exist
if ((exists(argv[1])) != True or (exists(argv[2])) != True):
    print("One or both of the files can't be opened or don't exist")
    exit(2)

#import the data from the databases
with open(argv[1], "r") as inputFile:
    #use of a list to store the data, formatted as [name, str1, str2, etc]
    database = list(reader(inputFile))
    #recording the amount of STRs it has to check in the given sequence
    amountOfSTRs = len(database[0])
    
#import the sequence text file
with open(argv[2], "r") as sequence:
    data = sequence.read()

#Storing the highest values
STRs = []
#repeating the check process for each STR (starts at 1 to omit the name)
for i in range(1,amountOfSTRs): 
    STR = database[0][i]
    length = len(STR)
    #The max amount of consecutive STRs in a row
    maxCounter = 0
    counter = 0
    #the location of the 'ponter' in the sequence
    pos = 0
    lastPos = 0
    while pos < len(data):
        counter += 1
        pos = data.find(STR, pos)
        #If it couldn't find any more of the STR
        if pos == -1:
            break
        #If starting not from the beginning
        elif (pos != -1) and ((pos - length) != lastPos):
            counter = 1
        if maxCounter < counter:
            maxCounter = counter
        #changes position
        lastPos = pos
        pos += 1
    #add the maxCounter in terms of strings (cuz the data added is in string) 
    STRs.append(str(maxCounter))

#Checking if the recorded values matches the values in the database
check = False
for x in range(0, len(database)):
    #checks if the list of the person's count for STR matches the sequence array
    if database[x][1:] == STRs:
        name = database[x][0]
        check = True
        break
    else:
        check = False
if check == True:
    print(name)
else:
    print("No Match")
exit(0)