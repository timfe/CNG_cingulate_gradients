#!/bin/bash
#
# This script takes a volumetric myelin sensitive image, and evaluates
# the intensity values along precreated intracortical surfaces. Additionally,
# it will map a annotation file to the individual subject space.
#
#
# Set up variables
# subject directory within BIDS structure

baseDir=$HOME/project/hcp/data
input=$HOME/project/hcp/analysis/fulllist.txt
while IFS= read -r subject; do
	
	gunzip -k $HOME/project/hcp/data/"$subject"/anat/T1wDividedByT2w.nii.gz 
	myeImage=$HOME/project/hcp/data/"$subject"/anat/T1wDividedByT2w.nii

	lhAnnot=$HOME/project/CNG_cingulate_gradients/lh.aparc.a2009s.annot
	rhAnnot=$HOME/project/CNG_cingulate_gradients/rh.aparc.a2009s.annot

	# set up and make necessary subfolders


	tmpDir="$baseDir"/"$subject"/tmpProcessingMyelin
	warpDir="$baseDir"/"$subject"/xfms
	for thisDir in $tmpDir $warpDir ; do
			[[ ! -d "$thisDir" ]] && mkdir "$thisDir"
	done


	myeImage=$HOME/project/hcp/data/$subject/anat/T1wDividedByT2w.nii

	export SUBJECTS_DIR="$baseDir"/$subject/surfaces

	#cd $HOME/project/hcp
	# Register to Freesurfer space
	bbregister --s "$subject" --mov "$myeImage" --reg "$warpDir"/"$subject"_mye2fs_bbr.lta --init-fsl --t1

	# Register to surface
	for ((num_surfs = 14; num_surfs <= 14; num_surfs++)); do

		for hemi in l r; do

			rm -f "$SUBJECTS_DIR"/equivSurfs/"$num_surfs"surfs/"$hemi"h_equiv_"$num_surfs"surfs1.0.pial
			rm -f "$SUBJECTS_DIR"/equivSurfs/"$num_surfs"surfs/"$hemi"h_equiv_"$num_surfs"surfs0.0.pial

			# find all equivolumetric surfaces and list by creation time
			x=$(ls -t "$SUBJECTS_DIR"/equivSurfs/"$num_surfs"surfs/${hemi}*)

			for ((n = 1; n <= 14; n++)); do

				# select a surfaces and copy to the freesurfer directory
				which_surf=$(sed -n "$n"p <<< "$x")
				cp "$which_surf" "$SUBJECTS_DIR"/"$subject"/surf/"$hemi"h."$n"by"$num_surfs"surf

				# project intensity values from volume onto the surface
				mri_vol2surf \
					--mov "$myeImage" \
					--reg "$warpDir"/"$subject"_mye2fs_bbr.lta \
					--hemi "$hemi"h \
					--out_type mgh \
					--trgsubject "$subject" \
					--out "$tmpDir"/"$hemi"h."$n".mgh \
					--surf "$n"by"$num_surfs"surf

			done

		done

	done
		#rm -rf "$tmpdir"

		# create symbolic link to fsaverage within the subject's directory
		ln -s $FREESURFER_HOME/subjects/fsaverage $SUBJECTS_DIR

		# map annotation to subject space
		mri_surf2surf --srcsubject fsaverage --trgsubject $subject --hemi lh \
			--sval-annot $lhAnnot \
			--tval       $SUBJECTS_DIR/"$subject"/label/lh.aparc.a2009s.annot
		mri_surf2surf --srcsubject fsaverage --trgsubject $subject --hemi rh \
			--sval-annot $rhAnnot \
			--tval       $SUBJECTS_DIR/"$subject"/label/rh.aparc.a2009s.annot
done < $input