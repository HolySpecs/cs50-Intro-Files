#Modules
import csv
from cs50 import SQL
from sys import argv, exit
from os.path import exists
#Initialize the database
db = SQL("sqlite:///students.db")

#Check if two arguments are present
if len(argv) != 2:
    print("Usage: python import.py data.csv")
    exit(1)

#check if file exists
if exists(argv[1]) != True:
    print(argv[1], " doesn't exist, try again")
    exit(2)

#clear the data if there is existing data (for testing purposes)
db.execute("DELETE FROM students")

#opening the file
with open(argv[1], "r") as characters:
    #splitting each item through commas
    reader = csv.DictReader(characters, delimiter = ",")
    for row in reader:
        fullName = row["name"]
        #splits the name if it has spaces
        names = fullName.split(" ")
        #gets the other data
        house = row["house"]
        birth = row["birth"]
        #checks the name length
        if len(names) == 2:
            firstName = names[0]
            middleName = None
            lastName = names[1]
        elif len(names) == 3:
            firstName = names[0]
            middleName = names[1]
            lastName = names[2]
        
        #adds the data to the database (the triple quotes are there for formating)
        db.execute("""
        INSERT INTO students (first, middle, last, house, birth)
        VALUES(?,?,?,?,?)""", firstName, middleName, lastName, house, birth)
        
exit(0)