#!/bin/bash
set -e # exit if any of the following commands fails
source ~/myenv/bin/activate
module load freesurfer/7.1
python get_data.py
bash ~/project/CNG_cingulate_gradients/mpc_scripts/01_constructSurfaces.sh
bash ~/project/CNG_cingulate_gradients/mpc_scripts/02_myelinMaptoSurf.sh
python gather_analysis.py