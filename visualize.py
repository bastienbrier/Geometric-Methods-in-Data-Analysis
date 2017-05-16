"""
Visualization tool to help visualize ToMATo results
"""

import csv
import matplotlib.pyplot as plt
import random
import sys

# Command-line arguments
if len(sys.argv) != 2 :
    print "Usage: visualize.py 'final or partial'" # if too much or not enough arguments
    sys.exit(1)
if (str(sys.argv[1]) != 'final') and (str(sys.argv[1]) != 'partial'):
    print "Please tell if you want the final result or your partial one" 
    sys.exit(1)

# Take the input numbers from the arguments
decision = str(sys.argv[1])

print 'Reading files...'

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

if decision == 'final':

	# Read file
    with open('data/clusters_final.txt','r') as f:
        clusters_file = csv.reader(f, delimiter=' ')
        clusters_final = []
        for l in f:
            row = l.split()
            clusters_final.append(str(row[0]))

    # Create the batches
	x1 = map(float,x1)
	y1 = map(float,y1)
    
    print 'Plotting...'
    # Plot the figure
    fig1 = plt.figure()
    og = fig1.add_subplot(111)
    og.plot([x1[i] for i in range(len(x1))], [y1[i] for i in range(len(y1))],'o', markersize=0.5, color='black')
    
    fig2 = plt.figure()
    ax = fig2.add_subplot(111)
    scatter = ax.scatter([x1[i] for i in range(len(x1))], [y1[i] for i in range(len(y1))], c=clusters_final, s=1)
    plt.show(block=True)
    sys.exit()

else:

    with open('ToMATo/clusters.txt','r') as f:
        clusters_file = csv.reader(f, delimiter=' ')
        clusters = []
        for l in f:
            row = l.split()
            clusters.append(str(row[0]))
    
    inputs_number = len(clusters) # take the number of inputs
    	
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
    random.seed(123)
    idx = random.sample(batch2,150) + random.sample(batch3,40) + random.sample(batch7,130) + random.sample(batch8,500) + random.sample(batch9,180)

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
    
    print 'Plotting...'
    # Plot the figure
    fig1 = plt.figure()
    og = fig1.add_subplot(111)
    og.plot([x1[i] for i in idx_full], [y1[i] for i in idx_full],'o', markersize=0.5, color='black')
    
    fig2 = plt.figure()
    ax = fig2.add_subplot(111)
    scatter = ax.scatter([x1[i] for i in idx_full], [y1[i] for i in idx_full], c=clusters, s=1)
    plt.show(block=True)
    sys.exit()