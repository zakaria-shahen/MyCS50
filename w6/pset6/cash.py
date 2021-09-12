from cs50 import get_float

# input owed and ceck input 
while True:
    owed = float(get_float("Change owed: "))
    if owed > 0:
        break

# convert to owed 
owed = round(owed * 10)


# counter of coins
coins = 0

# calc coins
# quarters (25¢), dimes (10¢), nickels (5¢), and pennies (1¢)
while True:
    if owed == 0:
        break
    elif owed >= 25:
        coins += 1
        owed -= 25
    elif owed >= 10:
        coins += 1
        owed -= 10
    elif owed >= 5:
        coins += 1
        owed -= 5
    elif owed >= 1:
        coins += 1
        owed -= 1

    

# output 
print(coins)