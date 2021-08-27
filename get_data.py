#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import datalad.api as dl
import os
import glob
import shutil
from git import Repo


# In[ ]:


# Build folder structure (according to BIDS)
projectDir = os.path.expanduser('~') + "/project/hcp"
dataDir = projectDir + "/data"
analysisDir = projectDir + "/analysis"
tmpDir = projectDir + "/tmp/"
scriptsDir = analysisDir + "/scripts"

os.makedirs(dataDir, exist_ok=True)
os.makedirs(analysisDir, exist_ok=True)
os.makedirs(tmpDir, exist_ok=True)
os.makedirs(scriptsDir, exist_ok=True)

# Define dataset in datalad
source = "///hcp-openaccess/HCP1200/"

# Create Subject list
os.chdir(analysisDir)
subjects = ["100206", "100307", "100408", "100610", "101006", "101107", "101309"]
with open("fulllist.txt", 'w') as file:
        for row in subjects:
            s = "".join(map(str, row))
            file.write(s+'\n')

# define files to download with datalad get
nec_files = {
            "anat": ["MyelinMap_MSMAll.32k_fs_LR.dscalar.nii", "T1wDividedByT2w.nii.gz"],
            "surf": ["lh.pial", "rh.pial", "lh.area.pial", "rh.area.pial", "lh.area", "rh.area", "lh.white", "rh.white", "lh.sphere.reg", "rh.sphere.reg", "lh.thickness", "rh.thickness"],
            "mri": ["orig.mgz", "brainmask.mgz"],
            "label": ["lh.cortex.label", "rh.cortex.label"]
            }


# In[ ]:


for subject in subjects:
    subjectDir = dataDir + "/" + subject
    if subject not in os.listdir(dataDir):
        # make subject specific subfolders
        os.makedirs(subjectDir, exist_ok=True)
        os.makedirs(subjectDir + "/anat/", exist_ok=True)
        os.makedirs(subjectDir + "/surfaces/" + subject, exist_ok=True)
        os.makedirs(subjectDir + "/surfaces/" + subject + "/mri/", exist_ok=True)
        os.makedirs(subjectDir + "/surfaces/" + subject + "/surf/", exist_ok=True)
        os.makedirs(subjectDir + "/surfaces/" + subject + "/label/", exist_ok=True)

        os.chdir(tmpDir)
        dl.install(source= source + subject, path=subject, recursive=True) ## https://github.com/datalad-datasets/human-connectome-project-openaccess

        # get files defined in nec_files
        for key, files in nec_files.items():
            for filename in files:
                for i in glob.glob("**/*"+filename, recursive=True):
                    dl.get(tmpDir + i, dataset=subject)
                    print(i + " was downloaded.")
                    if key == "anat":
                        src= tmpDir + i
                        dst = subjectDir + "/anat/" + os.path.basename(i)
                        shutil.copyfile(src, dst)
                        #print(i + " was copied to " + dst)
                    elif key == "surf":
                        src= tmpDir + i
                        dst = subjectDir + "/surfaces/" + subject + "/surf/" + os.path.basename(i)
                        shutil.copyfile(src, dst)
                        #print(i + " was copied to " + dst)
                    elif key == "mri":
                        src= tmpDir + i
                        dst = subjectDir + "/surfaces/" + subject + "/mri/" + os.path.basename(i)
                        shutil.copyfile(src, dst)
                        #print(i + " was copied to " + dst)
                    elif key == "label":
                        src= tmpDir + i
                        dst = subjectDir + "/surfaces/" + subject + "/label/" + os.path.basename(i)
                        shutil.copyfile(src, dst)
                    else:
                        print(i + " was not copied!")
        print("Files for subject: " + subject + " were successfully downloaded and transfered into BIDS structure.")
        # remove installed datasets in tmp folder
        os.chdir(tmpDir)   
        dl.remove(dataset=subject, recursive=True)
        print("tmp files for subject " + subject + " deleted. Datalad dataset removed. Files can be found in: " + subjectDir)
    else:
        print("Data for " + subject + " already exist in " + subjectDir)


# In[ ]:


# Download necessary scripts for further analysis

os.chdir(analysisDir)
if "surface_tools" not in os.listdir(analysisDir):
    Repo.clone_from("https://github.com/timfe/surface_tools", analysisDir + "/surface_tools")
else:
    os.chdir(analysisDir + "/surface_tools")
    os.system("git pull")
    print("surface_tools already downloaded. Performed 'git pull'")
