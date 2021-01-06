# Provides minimum number of coins needed to provide change

from cs50 import get_float

# Promt user for change amount greater than 0
while True:
    owe = get_float("Change Owed: ")
    if owe > 0:
        break

# Convert dollar amount into cents
amount = owe * 100
p = 0
q =0
d =0
n = 0

# Calculate how many quaters are needed
if amount >= 25:
    q = int(amount / 25)
    amount -= q * 25
    print("Quaters: " + str(q))
# Calculate how many dimes are needed
if amount >= 10:
    d = int(amount / 10)
    amount -= d * 10
    print("Dimes: " + str(d))
# Calculate how many nickels are needed
if amount >= 5:
    n = int(amount / 5)
    amount -= n * 5
    print("Nickels: " + str(n))

# Calculate how many pennies are needed
if amount >= 1:
    p = int(amount / 1)
    amount -= p * 1
    print("Pennies: " + str(p))

print("Total coins: " + str(q + d + n + p))