# Determine what brand a credit card is from

from cs50 import get_string
import sys

# Prompt user for card number as a string (to access any digit directly)
card = get_string("Credit Number: ")
card = card.strip()
cl = len(card)

total = 0
digits = []
# Iterate over every other number starting from second last digit 
for i in range(cl - 2, -1, -2):
    # Mutiply digit by 2 and add to list
    digits.append(int(card[i]) * 2)

# Add the digits of the mutiplied value together
for i in range(len(digits)):
    if digits[i] < 10:
        total += digits[i]
    elif digits[i] > 10:
        total += 1 + (digits[i] - 10)
    else:
        total += 1
    
# Iterate over the rest of the number
for i in range(cl - 1, -1, -2):
    # Add remaining numbers
    total += int(card[i])

# If total doesn't end in a 0 than INVALID card
if not total % 10 == 0:
    sys.exit("INVALID")
# Checking for AMEX
elif cl == 15:
    if int(card[0] + card[1]) == 37 or int(card[0] + card[1]) == 34:
        sys.exit("AMEX")
    else:
        sys.exit("INVALID")
# Checking for MasterCard or Visa
elif cl == 16:
    if int(card[0] + card[1]) < 56 and int(card[0] + card[1]) > 50:
        sys.exit("MASTERCARD")
    elif int(card[0]) == 4:
        sys.exit("VISA")
    else:
        sys.exit("INVALID")
# Checking for Visa
elif cl == 13:
    if int(card[0]) == 4:
        sys.exit("VISA")
    else:
        sys.exit("INVALID")
else:
    sys.exit("INVALID")