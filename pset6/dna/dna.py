# Identify a person based on their DNA

import csv
import sys

# Prompt user for command line arguments
if not len(sys.argv) == 3:
    sys.exit("Usage: python dna.py databases/file.csv sequences/file.txt")


# Open database file
with open(sys.argv[1], "r") as f1:
    reader = csv.DictReader(f1)
    people = list(reader)
    
# Open sequence file
with open(sys.argv[2], "r") as f2:
    seq = f2.read().strip("\n")

# Create a list of dna sequences from database
with open(sys.argv[1], "r") as f1:
    dna = f1.readline().strip("\n")
    # Seperate the string into a list of dna sequences
    dna = dna.split(",")
    # Remove the name element in the list
    dna.remove('name')

# Count max repeating dna sequence
max_count = [0] * len(dna)

# Loop through for each type of dna sequence
for i in range(len(dna)):
    
    # Loop through sequence to find matching dna
    for j in range(len(seq)):
        dna_counter = 0
        
        # Find the start of any repeats
        if dna[i] == (seq[j: j + len(dna[i])]):
            k = 0
            
            # Count repeats
            while seq[j + k: j + k + len(dna[i])] == dna[i]:
                dna_counter += 1
                k += len(dna[i])
                
            # If new count is higher replace old max
            if dna_counter > max_count[i]:
                max_count[i] = dna_counter
           
# Compare agaisnt database, loop through all the people
for i in range(len(people)):
    counter = 0
    
    # Loop through people's dna
    for j in range(len(dna)):
        if int(people[i][dna[j]]) == max_count[j]:
            counter += 1
        if counter == len(dna):
            sys.exit(people[i]['name'])
print("No match")