import os
import sys

if len(sys.argv) < 3:
    print("Usage: python QMAtoms.py <active_file> <main_file>")
    sys.exit(1)

directory = './'
active = sys.argv[1]
main = sys.argv[2]

active_site_pdb = os.path.join(directory, active)
main_pdb = os.path.join(directory, main)

def find_corresponding_lines(active_site_pdb_file, main_pdb_file):
    active_site_coordinates = set()
    corresponding_lines = []

    # Read the active-site PDB file and extract the coordinates
    with open(active_site_pdb_file, 'r') as active_site_file:
        for line in active_site_file:
            if line.startswith('ATOM'):
                x, y, z = float(line[30:38]), float(line[38:46]), float(line[46:54])
                active_site_coordinates.add((x, y, z))

    # Read the main protein PDB file and compare coordinates with active-site coordinates
    with open(main_pdb_file, 'r') as main_file:
        for index, line in enumerate(main_file, start=0):
            if line.startswith('ATOM'):
                x, y, z = float(line[30:38]), float(line[38:46]), float(line[46:54])
                if (x, y, z) in active_site_coordinates:
                    corresponding_lines.append(index)

    return corresponding_lines

corresponding_lines = find_corresponding_lines(active_site_pdb, main_pdb)
#print("Corresponding lines in the main PDB file:")
#print(corresponding_lines)

def get_consecutive_ranges(numbers):
    ranges = []
    start = numbers[0]
    end = numbers[0]

    for i in range(1, len(numbers)):
        if numbers[i] == end + 1:
            end = numbers[i]
        else:
            ranges.append((start, end))
            start = numbers[i]
            end = numbers[i]

    ranges.append((start, end))
    return ranges

numbers_list = corresponding_lines
consecutive_ranges = get_consecutive_ranges(numbers_list)
#print(consecutive_ranges)

def modify_tuples(tuples_list):
    modified_list = []

    for tup in tuples_list:
        modified_tup = str(tup).replace(', ', ':').replace('(', '').replace(')', '')
        modified_list.append(modified_tup)

    return (modified_list)

tuples_list = consecutive_ranges
modified_tuples_list = modify_tuples(tuples_list)

# Open the file for writing
output_file = open("QMAtoms.txt", "w")

output_file.write('{')

for modified_tup in modified_tuples_list:
    output_file.write(str(modified_tup) + " ")

output_file.write('} END END')

# Close the file
output_file.close()
