# JETSCAPE Jet Session

## 0. Preparation: Event Generation [Day 1]
Here we generates hard scatterings with JETSCAPE for both pp and PbPb at 5.02 TeV.
On the second day, we will use the generated event data and do analysis for jet ovservables. 
In this example, for each of pp and PbPb, we are generating 250 hard scatterings with 100<$\hat{p}_T$<160 GeV. 

### 1. Start the Docker Container

If you use ssh to do exercises on a remote computer, you need to create your ssh session with the following command: 

```
ssh -L 8888:127.0.0.1:8888 user@server
```

Then, please start the docker container,

For MacOS
```
docker run -it -p 8888:8888 -v ~/jetscape-docker:/home/jetscape-user --name myJSJetSession jetscape/base:v1.4
```

For Linux
```
docker run -it -p 8888:8888 -v ~/jetscape-docker:/home/jetscape-user --name myJSJetSession --user $(id -u):$(id -g) jetscape/base:v1.4
```
If you get an error `permission denied` on Linux,
please try `sudo`.

The option `-p 8888:8888` is necessary to creates a port to access the jupyter notebook, which we use in this hands-on session, from your local web browser.


### 2. Get Materials


Inside the docker container, download the school material from git if you have not:

```
cd ~/
git clone https://github.com/JETSCAPE/SummerSchool2021.git
```

If you have alread downloaded the material, please update to the latest version:
```
cd ~/SummerSchool2021
git pull
```

Go to `SummerSchool2021/Jul23_Jets` directory and download hydro profile files for this session:

```
cd ~/SummerSchool2021/Jul23_Jets
source ./get_hydro_profile.sh
```

### 3. Build JETSCAPE with LBT-tables, MUSIC and iSS

Please make sure all the external code packages (LBT-tables, MUSIC and iSS) have been
downloaded in `JETSCAPE/external_packages`. You can check this by the following commands,

```
cd ~/JETSCAPE/external_packages
ls
```

Please check the folder `LBT-tables`, `music` and `iSS` are present.
If not, please get them with the following commands,

```
./get_lbtTab.sh
./get_music.sh
./get_iSS.sh
```

Setup and build JETSCAPE from inside the docker container:

```
cd ~/JETSCAPE
mkdir build
cd build
cmake .. -DUSE_MUSIC=ON -DUSE_ISS=ON
make -j4
```

### 4. Test Run and Graph Visualization

Inside `build`, execute `runJetscape` with `jetscape_user_PP_PHYS.xml` in `SummerSchool2021/Jul23_Jets/config`

```
./runJetscape ../../SummerSchool2021/Jul23_Jets/config/jetscape_user_PbPb_PHYS_TestRun.xml
```

Check whether the code finished running without any error.

Then, lets' Visualize the parton shower. First, run `readerTest` inside `build`
```
./readerTest
```

Next, go <b><u>outside the docker</u></b>, install Graphviz (if you do not have). 

For MacOS via Homebrew
```
brew install graphviz
```

For MacOS via MacPorts
```
sudo port install graphviz
```

For Ubuntu or Debian
```
sudo apt install graphviz
```

For Fedora, Redhat, or CentOS
```
sudo yum install graphviz
```

Then, go `~/jetscape-docker/JETSCAPE/build` <b><u>outside the docker</u></b> and convert `my_test.gv` to a pdf file 
```
dot my_test.gv -Tpdf -o outputPDF.pdf
```

Open `outputPDF.pdf` in `build` with your pdf viewer and find the parton shower history.

### 5. Run pp@5.02 TeV Events

In `build` directory <b><u>inside the docker</u></b>, execute `runJetscape` with `jetscape_user_PP_PHYS.xml` in `SummerSchool2021/Jul23_Jets/config`

```
./runJetscape ../../SummerSchool2021/Jul23_Jets/config/jetscape_user_PP_PHYS.xml
```

Then, extract the final state hadrons by `FinalStateHadrons`

```
./FinalStateHadrons test_out_pp.dat test_out_pp_final_hadrons.dat
```

The list of hadrons in the final states of events is stored in `test_out_pp_final_hadrons.dat`

### 6. Run PbPb@5.02 TeV Events (Homework)
In `build` directory <b><u>inside the docker</u></b>, execute `runJetscape` with `jetscape_user_PbPb_PHYS.xml` in `SummerSchool2021/Jul23_Jets/config`

```
./runJetscape ../../SummerSchool2021/Jul23_Jets/config/jetscape_user_PbPb_PHYS.xml
```
This takes <b><u>more than 30 mins</u></b>. 

Then, extract the final state hadrons by `FinalStateHadrons`

```
./FinalStateHadrons test_out_pbpb.dat test_out_pbpb_final_hadrons.dat
```

The list of hadrons in the final states of events is stored in `test_out_pbpb_final_hadrons.dat`

## 1. Jet Analysis [Day 2]

### 1. Relaunch the Docker for the session

If you use ssh to do exercises on a remote computer, you need to create your ssh session with the following command: 

```
ssh -L 8888:127.0.0.1:8888 user@server
```

Then, please restart the docker container for this session:
```
docker start -ai myJSJetSession
```

If you have already deleted the docker image, please create it again:

For MacOS
```
docker run -it -p 8888:8888 -v ~/jetscape-docker:/home/jetscape-user --name myJSJetSession jetscape/base:v1.4
```

For Linux
```
docker run -it -p 8888:8888 -v ~/jetscape-docker:/home/jetscape-user --name myJSJetSession --user $(id -u):$(id -g) jetscape/base:v1.4
```
If you get an error `permission denied` on Linux,
please try `sudo`.

The option `-p 8888:8888` is necessary to creates a port to access the jupyter notebook, which we use in this hands-on session, from your local web browser.


Go to `SummerSchool2021/Jul23_Jets` directory and execute the script `init.sh` inside `SummerSchool2021/Jul23_Jets`:

```
cd ~/SummerSchool2021/Jul23_Jets
source ./init.sh
```

### 2. Run analysis code to reconstruct jets
Here using the final state hadron list from JETSCAPE as input, we reconstruct jet by anti-kt algorithm [https://arxiv.org/abs/0802.1189] with jet cone size, R=0.4 by a python code. In the output file from the analysis code, information of jets and charged hadrons inside the jet cone (associated particles) will be stored. 

Please go to `SummerSchool2021/Jul23_Jets/analysis_scripts` directory and find the python script `jet_reconstruction.py`.
```
cd analysis_scripts
```


Then first, run `jet_reconstruction.py` for pp events:
```
python jet_reconstruction.py -i ../../../JETSCAPE/build/test_out_pp_final_hadrons.dat -o ../data/jet_pp.dat
```

Option `-i` is used to specify the input file path (final state hadron list)
and option `-o` is for the output file path 


Then please run `jet_reconstruction.py` also for PbPb events:
```
python jet_reconstruction.py -i ../../../JETSCAPE/build/test_out_pbpb_final_hadrons.dat -o ../data/jet_pbpb.dat
```

Once finish running the analysis code, you will find `jet_pp.dat` and `jet_pbpb.dat` 
in `SummerSchool2021/Jul23_Jets/data`
storing the information of reconstructed jets.

Inside those files, for each jet, the information of charged hadrons detected inside the jet cone ($\Delta r = \sqrt{(\eta_{\mathrm{ch}}-\eta_{\mathrm{jet}})^2+(\phi_{\mathrm{ch}}-\phi_{\mathrm{jet}})^2} < R =0.4$) is stored in csv format:

<img src="img/jet_file.png" alt="1" width="1000"/>

