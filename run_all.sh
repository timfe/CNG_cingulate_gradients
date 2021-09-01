#!/bin/bash
source myenv/bin/activate
python get_data.py
bash /mpc_scripts/01_construcSurfaces.sh
bash /mpc_scripts/02_myelinMaptoSurf.sh
python gather_analysis.py