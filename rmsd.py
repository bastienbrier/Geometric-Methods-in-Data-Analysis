"""
Compute the RMSD distance matrix and write it in a file
"""

import csv
import numpy as np
import random
import sys

# Command-line arguments
if len(sys.argv) != 3 :
    print "Usage: rmsd.py 'nb of inputs' 'nb of reference points'" # if too much or not enough arguments
    sys.exit(1)
if (sys.argv[1].isdigit() == False) or (isinstance(int(sys.argv[1]), int) == False) or (int(sys.argv[1]) > 1420738) or (int(sys.argv[1]) < 5000):
    print "Please provide an number of inputs between 5000 and 1420738 (14207 for instance)" 
    sys.exit(1)
if (sys.argv[2].isdigit() == False) or (isinstance(int(sys.argv[2]), int) == False) or (int(sys.argv[2]) > 1420738) or (int(sys.argv[2]) < 1000):
    print "Please provide a number of reference points between 1000 and 1420738 (1000 for instance)" 
    sys.exit(1)
if (int(sys.argv[2]) > int(sys.argv[1])):
    print 'Please provide as many inputs as reference points (same or more)'
    sys.exit(1)

# Take the input numbers from the arguments
inputs_number = int(sys.argv[1])
reference_number = int(sys.argv[2])

print 'Reading files...'
# Open and read the file
with open('data/aladip_implicit.xyz','r') as f:
    aladip_file = csv.reader(f, delimiter=' ')
    x = []
    y = []
    z = []
    for row in aladip_file:
        x.append(row[0])
        y.append(row[1])
        z.append(row[2])

# Read 2d projection file
with open('data/dihedral.xyz','r') as f:
    dihedral_file = csv.reader(f, delimiter=' ')
    x1 = []
    y1 = []
    for l in f:
        row=l.split()
        x1.append(row[0])
        y1.append(row[1])

print 'Files read!'

# Create the batches
x1 = map(float,x1)
y1 = map(float,y1)

batch1 = [i for i,v in enumerate(x1) if v < 0]
batch2 = [i for i,v in enumerate(x1) if v > 0 and v < 2]
batch3 = [i for i,v in enumerate(x1) if v > 2]
batch4 = [i for i,v in enumerate(y1) if v < -2]
batch5 = [i for i,v in enumerate(y1) if v > -2  and v < 1]
batch6 = [i for i,v in enumerate(y1) if v > 1]
batch7 = list(set(batch1).intersection(batch4))
batch8 = list(set(batch1).intersection(batch5))
batch9 = list(set(batch1).intersection(batch6))

del batch1
del batch4
del batch5
del batch6

# Shuffle to ensure again representativity
random.seed(123)
random.shuffle(batch2)
random.seed(123)
random.shuffle(batch3)
random.seed(123)
random.shuffle(batch7)
random.seed(123)
random.shuffle(batch8)
random.seed(123)
random.shuffle(batch9)

# Reference points
ratio_ref = float(reference_number) / float(1420738)
ref_batch2 = int(round(len(batch2)*ratio_ref))
ref_batch3 = int(round(len(batch3)*ratio_ref))
ref_batch7 = int(round(len(batch7)*ratio_ref))
ref_batch9 = int(round(len(batch9)*ratio_ref))
ref_batch8 = reference_number - ref_batch2 - ref_batch3 - ref_batch7 - ref_batch9
random.seed(123)
idx = batch2[:ref_batch2] + batch3[:ref_batch3] + batch7[:ref_batch7] + batch8[:ref_batch8] + batch9[:ref_batch9]

# Calculate the ratio represented by inputs_number
ratio = float(inputs_number) / float(1420738)
# To have a sum perfectly equal to inputs_number
nb_batch2 = int(round(len(batch2)*ratio))
nb_batch3 = int(round(len(batch3)*ratio))
nb_batch7 = int(round(len(batch7)*ratio))
nb_batch9 = int(round(len(batch9)*ratio))
nb_batch8 = inputs_number - nb_batch2 - nb_batch3 - nb_batch7 - nb_batch9

# Take points in the 5 subspaces
random.seed(123)
idx_full = batch2[:nb_batch2] + batch3[:nb_batch3] + batch7[:nb_batch7] + batch8[:nb_batch8] + batch9[:nb_batch9]

# Reorganize the data as a 3D matrix with 'axis' shape
aladip = np.zeros((len(x)/10,3,10))
print 'Aladip calculation...'
for i in range(len(x)/10):
    for j in range(10):
        aladip[i][0][j] = float(x[10*i + j])
        aladip[i][1][j] = float(y[10*i + j])
        aladip[i][2][j] = float(z[10*i + j])
print 'Aladip ready!'

# Free up some memory
del z
del row
del i
del j

# Submatrices
aladip_trunc = aladip[idx][:][:]
aladip_full_sample = aladip[idx_full][:][:]

print 'Conformation object calculation...'
# RMSD - Create the conformation object
from IRMSD import align_array
from IRMSD import Conformations
aladip_trunc = align_array(aladip_trunc, 'axis') # pad the matrix
conf_obj = Conformations(aladip_trunc, 'axis', 10) # create the conformation object
aladip_full_sample = align_array(aladip_full_sample, 'axis')
conf_full = Conformations(aladip_full_sample, 'axis', 10) 

# Free up some memory
del aladip
del aladip_trunc
del aladip_full_sample

# Final matrix    
rmsds_matrix = np.zeros((inputs_number,reference_number))
print 'Object created!'

# Calculate the RMSD matrix    
for i in range(inputs_number):
    rmsds = conf_obj.rmsds_to_reference(conf_full, i) # compute RMSD with first conf as reference
    rmsds_matrix[i] = rmsds
    del rmsds
    if i % 1000 == 0:
        print 'Step: ' + str(i)

# Save the file
print 'Saving file...'
np.savetxt('ToMATo/inputs/rmsd_matrix.txt', rmsds_matrix, delimiter= ' ')