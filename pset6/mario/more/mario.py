# Prints out right and left leaning pyramids with a gap in between

from cs50 import get_int

# Keep prompting user for input between 1 to 8
while True:
    h = get_int("Enter Height (1 to 8): ")
    if h > 0 and h <= 8:
        break

# Print out triangles
for i in range(1, h + 1):
    # Print spaces
    print(" " * (h - i), end="")
        
    # Print left triangle and gap
    print("#" * i, end="  ")
    
    # Print right triangle
    print("#" * i,)

