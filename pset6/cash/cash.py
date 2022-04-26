from cs50 import get_float

def changeToReturn(money):
    coins = 0
    quarters = 0
    dimes = 0
    nickels = 0
    memory = 0

    cents = round(money * 100)
    if cents >= 25:
        quarters = cents // 25
        cents = cents - (25 * quarters)
    if cents >= 10:
        dimes = cents // 10
        cents = cents - (10 * dimes)
    if cents >= 5:
        nickels = cents // 5
        cents = cents - (5 * nickels)
    coins = quarters + dimes + nickels + cents
    return coins



cash = float(0)
while True:
    cash = get_float("Change owed: ")
    if cash >= 0:
        break
print(changeToReturn(cash))