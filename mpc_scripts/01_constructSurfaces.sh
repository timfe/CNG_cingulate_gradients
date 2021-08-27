#!/bin/bash

# add path to surface_tools
export projectDir = $HOME/project/hcp
export PATH=$PATH:$HOME/analysis/surface_tools/equivolumetric_surfaces/

module load freesurfer/7.1

# set up as overearching bids directory
dataDir=projectDir/data

# change to your subject list
$HOME/analysis/fulllist.txt | while IFS= read -r sub ; do

    # Set up SUBJECTS_DIR for freesurfer based functions 
    # In this setup the freesurfer output is nested within 'surfaces' 
    # subdirectory of the subject's BIDS folder
    export SUBJECTS_DIR=${dataDir}/${sub}/surfaces/
    
		# setup output directory
		outDir=${dataDir}/${sub}/surfaces/equivSurfs
		
		# checks whether the output directory exists and makes it if it doesn't
		[[ ! -d "$outDir" ]] && mkdir -p "$outDir"

		# best practice to construct multiple sets of surfaces, with a range of surface numbers for optimisation
		
		for num_surfs in 14; do

			# set output directory and create directory if necessary
			[[ ! -d "$outDir"/"$num_surfs"surfs ]] && mkdir -p "$outDir"/"$num_surfs"surfs

			for hemi in lh rh ; do

				python generate_equivolumetric_surfaces.py \
				"$dataDir"/"$sub"/surfaces/"$sub"/surf/"$hemi".pial \
				"$dataDir"/"$sub"/surfaces/"$sub"/surf/"$hemi".white \
				"$num_surfs" \
				"$outDir"/"$num_surfs"surfs/"$hemi"_equiv_"$num_surfs"surfs \
				--software freesurfer \
				--subject "$sub"
				
			done

		done

done