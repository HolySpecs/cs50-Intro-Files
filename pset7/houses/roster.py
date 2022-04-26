#Modules
from cs50 import SQL
from sys import argv, exit
#Initialize the database
db = SQL("sqlite:///students.db")

#Check if two arguments are present
if len(argv) != 2:
    print("Usage: python roster.py HouseName")
    exit(1)

#gets the data from the database
result = db.execute("""
SELECT first, middle, last, birth
FROM students
WHERE house = ?
ORDER BY last ASC, first ASC 
    """, argv[1])
#this only comes up when the result returns a blank array ie: the house wasn't located
if result == []:
    print(argv[1], "is not a house!")
    exit(2)

for row in result:
    #gets the first name, last name and birth
    firstName = row["first"]
    lastName = row["last"]
    year = row["birth"]
    
    #changes the name string variable depending if there is a middle name or not
    if row["middle"] == None:
        name = firstName + " " + lastName
    else:
        name = firstName + " " + row["middle"] + " " + lastName
    #prints in the following format
    print("{}, born {}".format(name, year))
exit(0)