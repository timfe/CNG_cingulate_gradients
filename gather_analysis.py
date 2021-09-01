import os
import glob
import shutil

projectDir = os.path.expanduser('~') + "/project/hcp"
dataDir = projectDir + "/data"
analysisDir = projectDir + "/analysis"
tmpDir = projectDir + "/tmp/"
scriptsDir = analysisDir + "/scripts"

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
    "lh.economo.annot", "rh.economo.annot", 
    "lh.Schaefer2018_1000Parcels_7Networks_order-2.annot", "rh.Schaefer2018_1000Parcels_7Networks_order-2.annot"
    ]

surfs = [".pial"]

myelin_files = [
    "1.mgh", "2.mgh", "3.mgh", "4.mgh", "5.mgh", "6.mgh", "7.mgh", 
    "8.mgh", "9.mgh", "10.mgh", "11.mgh", "12.mgh", "13.mgh", "14.mgh"
    ]

os.chdir(analysisDir)

sub_list = [] # optional

#["100206", "100307", "100408", "100610", "101006", "101107", "101309", "101410",
#  "101915", "102008", "102109", "102311", "102513",
#  "102614", "102715", "102816", "103010", "103111", "103212",
#  "103414", "103515", "103818", "104012", "104416", "104820", "105014", "105115", "105216"]

if len(sub_list) > 0:
    with open("fulllist.txt", 'w') as file:
        for row in sub_list:
            s = "".join(map(str, row))
            file.write(s+'\n')

subjects = []
with open("fulllist.txt", 'r') as file:
        subject = file.readlines()
        for i in range(len(subject)):
            subjects.append(subject[i].replace("\n", ""))


print("Chosen subjects: " + str(subjects))
print("Copying to /data/group/cng/Projects/cingulate/ now...")

projectDir = os.path.expanduser('~') + "/project/hcp/data/"
os.chdir(projectDir)
for subject in subjects:
    os.makedirs("/data/group/cng/Projects/cingulate/" + subject + "/surfaces/equivSurfs/" + str(num_surfs) + "surfs" + "/surfs_out", exist_ok=True)
    os.makedirs("/data/group/cng/Projects/cingulate/" + subject + "/surfaces/" + subject + "/surf", exist_ok=True)
    os.makedirs("/data/group/cng/Projects/cingulate/" + subject + "/surfaces/" + subject + "/label", exist_ok=True)
    for filename in surfs:
        os.chdir(projectDir + subject + "/surfaces/equivSurfs")
        for file in glob.glob("**/*"+filename, recursive=True):
            src = projectDir + subject + "/surfaces/equivSurfs/" + file 
            dst = "/data/group/cng/Projects/cingulate/" + subject + "/surfaces/equivSurfs/" + file
            shutil.copyfile(src, dst)
    for filename in myelin_files:
        os.chdir(projectDir + subject + "/tmpProcessingMyelin")
        for file in glob.glob("**/*"+filename, recursive=True):
            src = projectDir + subject + "/tmpProcessingMyelin/" + file 
            dst = "/data/group/cng/Projects/cingulate/" + subject + "/surfaces/equivSurfs/" + str(num_surfs) + "surfs" + "/surfs_out/" + file
            shutil.copyfile(src, dst)
    for filename in annot_files:
        os.chdir(projectDir + subject + "/surfaces/" + subject)
        for file in glob.glob("**/*"+filename, recursive=True):
            src = projectDir + subject + "/surfaces/" + subject + "/" + file 
            dst = "/data/group/cng/Projects/cingulate/" + subject + "/surfaces/" + subject + "/" + file 
            shutil.copyfile(src, dst)
    for filename in pial_files:
        os.chdir(projectDir + subject + "/surfaces/" + subject + "/surf/")
        for file in glob.glob("**/*"+filename, recursive=True):
            src = projectDir + subject + "/surfaces/" + subject + "/surf/" + file 
            dst = "/data/group/cng/Projects/cingulate/" + subject + "/surfaces/" + subject + "/surf/" + file
            shutil.copyfile(src, dst)
    print(f"{subject} successfully copied to /data/group/cng/Projects/cingulate/.")