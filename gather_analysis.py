import os
import glob
import shutil

num_surfs = 14

pial_files = [
    "lh.pial", "rh.pial",
    ]

lst =[
    ".1by14surf", ".2by14surf", ".3by14surf", ".4by14surf", ".5by14surf", ".6by14surf",
    ".7by14surf", ".8by14surf", ".9by14surf", ".10by14surf", ".11by14surf", ".12by14surf",
    ".13by14surf", ".14by14surf"
    ]

annot_files = [
    "lh.aparc.a2009s.annot", "rh.aparc.a2009s.annot"
    ]

surfs = [".pial"]

myelin_files = [
    "1.mgh", "2.mgh", "3.mgh", "4.mgh", "5.mgh", "6.mgh", "7.mgh", 
    "8.mgh", "9.mgh", "10.mgh", "11.mgh", "12.mgh", "13.mgh", "14.mgh"
    ]

        
projectDir = os.path.expanduser('~') + "/project/hcp/data/"
for subject in os.listdir(projectDir):
    os.makedirs("/data/group/cng/Projects/cingulate/" + subject + "_tim" + "/surfaces/equivSurfs/" + str(num_surfs) + "surfs" + "/surfs_out", exist_ok=True)
    os.makedirs("/data/group/cng/Projects/cingulate/" + subject + "_tim" + "/surfaces/" + subject + "/surf", exist_ok=True)
    os.makedirs("/data/group/cng/Projects/cingulate/" + subject + "_tim" + "/surfaces/" + subject + "/label", exist_ok=True)
    for filename in surfs:
        os.chdir(projectDir + subject + "/surfaces/equivSurfs")
        for file in glob.glob("**/*"+filename, recursive=True):
            src = projectDir + subject + "/surfaces/equivSurfs/" + file 
            dst = "/data/group/cng/Projects/cingulate/" + subject + "_tim" + "/surfaces/equivSurfs/" + file
            shutil.copyfile(src, dst)
    for filename in myelin_files:
        os.chdir(projectDir + subject + "/tmpProcessingMyelin")
        for file in glob.glob("**/*"+filename, recursive=True):
            src = projectDir + subject + "/tmpProcessingMyelin/" + file 
            dst = "/data/group/cng/Projects/cingulate/" + subject + "_tim" + "/surfaces/equivSurfs/" + str(num_surfs) + "surfs" + "/surfs_out/" + file
            shutil.copyfile(src, dst)
    for filename in annot_files:
        os.chdir(projectDir + subject + "/surfaces/" + subject)
        for file in glob.glob("**/*"+filename, recursive=True):
            src = projectDir + subject + "/surfaces/" + subject + "/" + file 
            dst = "/data/group/cng/Projects/cingulate/" + subject + "_tim" + "/surfaces/" + subject + "/" + file 
            shutil.copyfile(src, dst)
    for filename in pial_files:
        os.chdir(projectDir + subject + "/surfaces/" + subject + "/surf/")
        for file in glob.glob("**/*"+filename, recursive=True):
            src = projectDir + subject + "/surfaces/" + subject + "/surf/" + file 
            dst = "/data/group/cng/Projects/cingulate/" + subject + "_tim" + "/surfaces/" + subject + "/surf/" + file
            shutil.copyfile(src, dst)