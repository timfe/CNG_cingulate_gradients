# Cingulate Data Analysis

© Build by: Tim Fellerhoff, Gerion Michael Reimann

## Prerequisites

to run the code in INM7 cluster:

Make sure you have access to the Human Connectome Project by following the dedicated instructions [here](https://github.com/datalad-datasets/human-connectome-project-openaccess)!

```bash
# Start up your terminal and log into the INM7 cluster with your credentials:
$ ssh mmustermann@juseless.inm7.de

# Create virtual python environment to enable installation of needed Python packages:
$ virtualenv myenv
$ source myenv/bin/activate
$ pip install nibabel
$ pip install datalad
```

```bash
# Make a projectDir in your HOME directory
$ mkdir -p ~/project/hcp/analysis
$ mkdir -p ~/project/hcp/data

# Note: The exact naming is important here, 
# as following code refers to these directories.
```

```bash
# Clone necessary git repo into your project folder:

$ cd project
$ git clone [https://github.com/timfe/CNG_cingulate_gradients](https://github.com/timfe/CNG_cingulate_gradients)
```

![Bildschirmfoto 2021-09-01 um 20.20.07.png](Cingulate%20Data%20Analysis%20143b9ec95bbb434592c60f7beb19edd7/Bildschirmfoto_2021-09-01_um_20.20.07.png)

Note: If you want to make changes in the script (e.g. to change directories), it's recommended to *fork* it into your own GitHub repo.

## All in One

You can run all data processing by running the following:

```bash
# create a subjectlist:

$ printf "100206\n100307\n100408" > ~/project/hcp/analysisfulllist.txt

# Example: creates a subjectlist with 3 subjects. Note that subjects are separated by a newline \n. 
# You can add as many as you want. Just make sure that they are actually apparent in the dataset.
```

```bash
# Running data processing
bash ~/project/CNG_cingulate_gradients/run_all.sh
```

![Bildschirmfoto 2021-09-01 um 20.03.26.png](Cingulate%20Data%20Analysis%20143b9ec95bbb434592c60f7beb19edd7/Bildschirmfoto_2021-09-01_um_20.03.26.png)

More info on the scripts that are running in `run_all.sh` :

- `get_data.py` [Link to GitHub](https://github.com/timfe/CNG_cingulate_gradients/blob/main/get_data.py)

    The get_data.py takes input from a file called "fulllist.txt" to choose subjectIDs. If you have forked the GitHub repo you can insert the subjectIDs directly into the script. If you wanna use it as is, type in the following into your juseless terminal:

    ```bash
    # with subjects in fulllist.txt you can now run the python script get_data.py:
    # Make sure that your virtualenv is running (indicated by "(myenv)" in your terminal).
    # You will get asked for your **key_id** and **secret_id** for data access and retrieval of the HCP.
    # You can get these here: [Link](https://github.com/datalad-datasets/human-connectome-project-openaccess)

    $ python project/CNG_cingulate_gradients/get_data.py

    # This will take some time (depending on the amount of subjects).
    # **This script downloads & transforms the data into the necessary BIDS structure.**
    ```

- `01_constructSurfaces.sh` [Link to GitHub](https://github.com/timfe/CNG_cingulate_gradients/blob/main/mpc_scripts/01_constructSurfaces.sh)

    Constructs equivolumetric intracortical surfaces using "surface tools" ([GitHub](https://github.com/kwagstyl/surface_tools))

- `02_myelinMaptoSurf.sh` [Link to GitHub](https://github.com/timfe/CNG_cingulate_gradients/blob/main/mpc_scripts/02_myelinMaptoSurf.sh)

    Compiles intensity values 
    along intracortical surfaces from a myelin-sensitive volume, and 
    registers an annotation from fsaverage to the individual subject.

- `03_surftoMPC.m`

    Imports data to matlab and builds 
    microstructure profile covariance matrices.


Furthermore the script downloads this forked git repo https://github.com/timfe/surface_tools and the scripts for MPC calculation from https://github.com/timfe/micaopen/tree/master/MPC/scripts (commented by default. Delete "#" to enable).


