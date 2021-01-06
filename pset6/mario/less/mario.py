# Prints a half pyramid leaning right
from cs50 import get_int

# Keep prompting user for input between 1 to 8
while True:
    num = get_int("Height (1 to 8): ")
    if num > 0 and num <= 8:
        break

# Print out triangle
for i in range(1, num + 1):
    # Print spaces
    for j in range(num - i, 0, -1):
        print(" ", end="")
    # Print #'s
    for k in range(i):
        print("#", end="")
    print()
  
