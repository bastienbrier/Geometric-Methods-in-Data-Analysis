----------------------------------------------------------------------------------
Project7 - Mode-seeking for detecting metastable states in protein conformations
Authors  - Bastien BRIER & Andrei CONSTANTINESCU
Date 	 - February 26, 2017
----------------------------------------------------------------------------------


1. MAKE FILES


You first have to make all the programs required for this project. They come all with make files.
Here are the three programs to make in the right order:
 - ann_1.1.2
 - IRMSD
 - ToMATo


2. PROGRAM DESCRIPTION


There are two options : you want to see the final results, or you want to experiment a whole process on a small subset.
If you want to visualize the final result with all input points :
 - type on your terminal : python visualize.py final
 - close the windows to close the program

If you want to experiment, we will describe on next part.


3. PROGRAM EXPERIMENTATION


In order to experiment the full process, you will have to first create an RMSD matrix:
 - type python rmsd.py 'nb of input points' 'nb of reference points'
 - you will have here to specify on how many points you want to compute the RMSD matrix and how many reference you want
 - this is an example, we recommend using around 14,207 input points (1%) and 1,000 reference points

Then, you will have to use ToMATo on this matrix:
 - go to the Project7/ToMATo folder with your terminal
 - first type ./main_w_density inputs/rmsd_matrix.txt 20 0.3 1e20 (we used 20 and 0.3 as hyperparameters, but you can experiment others)
 - the program will output 0 clusters
 
Find the right hyperparameter tau:
 - you will obtain a diagram called diagram.m
 - open Matlab
 - type: load 'diagram.txt'
 - then: display_diagram(diagram)
 - then: experiment different values for tau by typing: display_diagram(diagram, 90). (here we tried 90)
 - if you see 5 points under the threshold that appeared, the hyperparameter value is right.

 Run ToMATo with the new hyperparameters:
 - type: ./main_w_density inputs/rmsd_matrix.txt 20 0.3 'tau parameter selected' (in our case, ./main_w_density inputs/rmsd_matrix.txt 20 0.3 90)
 - hopefully, the program will output 5 clusters

 Now visualize your results:
 - go back in the main folder Project7
 - type: python visualize.py partial
 - you will then see your original input space and its clustering
 - close the windows to close the program
