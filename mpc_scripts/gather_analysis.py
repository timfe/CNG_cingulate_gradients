import os
import glob

pial_files = [
    "lh.pial", "rh.pial"
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
    #os.makedirs("/data/group/cng/Projects/cingulate/" + subject + "_tim", exist_ok=True)
    #os.makedirs("/data/group/cng/Projects/cingulate/" + subject + "_tim" + "/myelinMap", exist_ok=True)
    #os.makedirs("/data/group/cng/Projects/cingulate/" + subject + "_tim" + "/surfaces", exist_ok=True)
    for filename in surfs:
        os.chdir(projectDir + subject + "/surfaces/equivSurfs")
        for file in glob.glob("**/*"+filename, recursive=True):
            #os.chdir(projectDir + subject + "/surfaces/")
            src = projectDir + subject + "/surfaces/equivSurfs/" + file 
            print(src)
    for filename in myelin_files:
        os.chdir(projectDir + subject + "/tmpProcessingMyelin")
        for file in glob.glob("**/*"+filename, recursive=True):
            #os.chdir(projectDir + subject + "/surfaces/")
            src = projectDir + subject + "/tmpProcessingMyelin" + file 
            print(src)
    for filename in annot_files:
        os.chdir(projectDir + subject + "/surfaces/" + subject)
        for file in glob.glob("**/*"+filename, recursive=True):
            #os.chdir(projectDir + subject + "/surfaces/")
            src = projectDir + subject + "/surfaces/" + subject + "/" + file 
            print(src)
    for filename in pial_files:
        os.chdir(projectDir + subject + "/surfaces/" + subject + "/surf/")
        for file in glob.glob("**/*"+filename, recursive=True):
            #os.chdir(projectDir + subject + "/surfaces/")
            src = projectDir + subject + "/surfaces/" + subject + "/surf/" + file 
            print(src)