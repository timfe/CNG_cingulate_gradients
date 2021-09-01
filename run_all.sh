#!/bin/bash
set -e # exit if any of the following commands fails

# activate virtual python environment to access packages (datalad, nibabel)
source ~/myenv/bin/activate

# load freesurfer so that the following scripts can access it on the cluster
module load freesurfer/7.1

# load data from subjects that are in fulllist.txt
python get_data.py

# do the first 2 steps of MPC from the downloaded data (Originals from: https://github.com/MICA-MNI/micaopen/tree/master/MPC/scripts)
bash ~/project/CNG_cingulate_gradients/mpc_scripts/01_constructSurfaces.sh
bash ~/project/CNG_cingulate_gradients/mpc_scripts/02_myelinMaptoSurf.sh

# loading data into sofies projects folder for further analysis. Data can be found here
python gather_analysis.py