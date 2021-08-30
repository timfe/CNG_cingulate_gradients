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
source = "///hcp-openaccess/HCP1200/" ## https://github.com/datalad-datasets/human-connectome-project-openaccess

# Create Subject list
os.chdir(analysisDir)


####[
#    "100206", "100307", "100408", "100610", "101006", "101107", "101309", "101410"
#    "101915", "102008", "102109", "102311", "102513",
#    "102614", "102715", "102816", "103010", "103111", "103212",
#    ]

###["103414", "103515", "103818", "104012", "104416", "104820", "105014", "105115", "105216"]



subjects = []
with open("fulllist.txt", 'r') as file:
        subject = file.readlines()
        for i in range(len(subject)):
            subjects.append(subject[i].replace("\n", ""))


print("Chosen subjects: " + str(subjects))

# define files to download with datalad get
nec_files = {
            "anat": ["T1wDividedByT2w.nii.gz"],
            "surf": ["lh.pial", "rh.pial", "lh.area.pial", "rh.area.pial", "lh.area", "rh.area", "lh.white", "rh.white", "lh.sphere.reg", "rh.sphere.reg", "lh.thickness", "rh.thickness"],
            "mri": ["orig.mgz", "brainmask.mgz"],
            "label": ["lh.cortex.label", "rh.cortex.label"]
            }

def unique(list1):
     
    # insert the list to the set
    list_set = set(list1)
    # convert the set to the list
    unique_list = (list(list_set))
    return unique_list

# In[ ]:


for subject in subjects:
    subjectDir = dataDir + "/" + subject    
    os.chdir(subjectDir)
    file_list = []
    files_downloaded = []
    for key, files in nec_files.items():
        for filename in files:
            file_list.append(filename)
            for i in glob.glob("**/*"+filename, recursive=True):
                files_downloaded.append(os.path.basename(i))
    files_downloaded = unique(files_downloaded)
    for file in files_downloaded:
        if file in file_list and file in files_downloaded:
            file_list.remove(file)
    
    if len(file_list) == 0:
        print("All data for " + subject + " already exist in " + subjectDir)        
    else:
        print("Files need to be downloaded. Doing now...")
        # make subject specific subfolders
        os.makedirs(subjectDir, exist_ok=True)
        os.makedirs(subjectDir + "/anat/", exist_ok=True)
        os.makedirs(subjectDir + "/func/", exist_ok=True)
        os.makedirs(subjectDir + "/surfaces/" + subject, exist_ok=True)
        os.makedirs(subjectDir + "/surfaces/" + subject + "/mri/", exist_ok=True)
        os.makedirs(subjectDir + "/surfaces/" + subject + "/surf/", exist_ok=True)
        os.makedirs(subjectDir + "/surfaces/" + subject + "/label/", exist_ok=True)

        os.chdir(tmpDir)
        dl.install(source= source + subject, path=subject, recursive=True) 

        # get files still left in file_list
        for filename in file_list:
            for i in glob.glob("**/*"+filename, recursive=True):
                dl.get(tmpDir + i, dataset=subject)
                print(i + " was downloaded.")
                if os.path.basename(os.path.normpath(i)) == "anat":
                    src= tmpDir + i
                    dst = subjectDir + "/anat/" + os.path.basename(i)
                    shutil.copyfile(src, dst)
                    #print(i + " was copied to " + dst)
                elif os.path.basename(os.path.normpath(i)) == "surf":
                    src= tmpDir + i
                    dst = subjectDir + "/surfaces/" + subject + "/surf/" + os.path.basename(i)
                    shutil.copyfile(src, dst)
                    #print(i + " was copied to " + dst)
                elif os.path.basename(os.path.normpath(i)) == "mri":
                    src= tmpDir + i
                    dst = subjectDir + "/surfaces/" + subject + "/mri/" + os.path.basename(i)
                    shutil.copyfile(src, dst)
                    #print(i + " was copied to " + dst)
                elif os.path.basename(os.path.normpath(i)) == "label":
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
        


# In[ ]:


# Download necessary scripts for further analysis

os.chdir(analysisDir)
if "surface_tools" not in os.listdir(analysisDir):
    installDir = analysisDir + "/surface_tools"
    os.system("git clone https://github.com/timfe/surface_tools ${installDir}")
else:
    os.chdir(analysisDir + "/surface_tools")
    os.system("git pull")
    print("surface_tools already downloaded. Performed 'git pull'")
