# SMASH hadronic transport hands-on session

### Our goals
 - Learn to use SMASH as a hadronic afterburner
 - Understand SMASH inputs: resonances and their decays, switching on and off different reactions
 - Understand SMASH outputs: particles and collision history
 - Physics project: Life and death of rho-resonance

*To begin* add your name to the [table](https://docs.google.com/spreadsheets/d/e/2PACX-1vTo_TeWIkXPCh4PBpLBNZac_pkB6pao6ynenWf2RNMZDHjeT4O1Mg3xBPx6nkitxthQq7GRothvNjCC/pubhtml) to mark your progress.
Then follow the steps below.

It would be great if you *perform step 1. in advance*,
because compilation of SMASH library takes around 5 minutes, compilation
of JetScape with SMASH takes around 7 minutes, running getting 10 events takes
around 7 minutes = around 20 minutes total.

  

<details><summary> My personal docker cheat sheet </summary>
<p>

I'm not an active docker user, so here I assemble commands that were useful for me:

```
  docker container ls -a        # List all containers
  docker system prune           # Remove all the stopped containers
  docker start -ai myJetscape   # Start JETSCAPE docker again after exiting

  # run JETSCAPE container on linux
  docker run -it -v ~/jetscape-docker:/home/jetscape-user --name myJetscape --user $(id -u):$(id -g) jetscape/base:v1.4

  # run JETSCAPE container on MAC
  docker run -it -v ~/jetscape-docker:/home/jetscape-user --name myJetscape jetscape/base:v1.4
```

</p>
</details>


<details><summary><b> What is SMASH </b></summary>
<p>

SMASH is a hadronic transport code. In JETSCAPE it simulates multiple hadron-hadron scatterings
in the final dilute stage of the fireball evolution. Observables affected by the afterburner
are baryon spectra and flow, as well as resonance production.

Look at the visualization at the [official SMASH webpage](https://smash-transport.github.io/).

</p>
</details>



<details><summary><b> Making sure prequisites are ready </b></summary>
<p>

1. I assume that you have followed the [general school instructions](https://github.com/JETSCAPE/SummerSchool2021/blob/master/README.md)
 and have docker installed. You really need docker to proceed.

Before we begin our session, please make sure all the code packages are already
in the correct place on your computer. You should have a `jetscape-docker`
folder under your home directory. Try to list the folder inside
`jetscape-docker` with the following command,

```
ls ~/jetscape-docker
```

You need to make sure the following folders are present,

* JETSCAPE
* SummerSchool2021

Try the following command to make sure you are ready

```
    docker start -ai myJetscape
```

<details><summary><b> 1. Compiling JetScape with SMASH in docker environment </b></summary>
<p>

Go to the docker environment. If you didn't start it yet, start by

```
  docker start -ai myJetscape
```

Compiling JetScape with MUSIC + iSS + SMASH:

```
cd jetscape-docker/JETSCAPE/external_packages

# Download MUSIC hydrodynamics, iSS particle sampler, EoS tables
./get_music.sh
./get_iSS.sh
./get_freestream-milne.sh
./get_lbtTab.sh

# Downloading SMASH and compiling SMASH as library
# This takes around 5 minutes on laptop
./get_smash.sh

cd jetscape-docker/JETSCAPE/build
cmake .. -DUSE_MUSIC=ON -DUSE_ISS=ON -DUSE_SMASH=ON

# Compiles JetScape+MUSIC+SMASH
# This takes around 7 minutes on laptop
# The number after j means number of cores, adjust according to available computing power
make -j2
```

Let us run JETSCAPE with SMASH

```
cd ~/jetscape-docker/JETSCAPE/build

# Creating output directory with this specific name is important, otherwise you get a crash
mkdir smash_output

# The argument is a JetScape configuration file
./runJetscape ~/jetscape-docker/SummerSchool2021/Jul22_Transport/jetscape_user_AuAu200.xml
```

While the code is running we explore the way SMASH is configured.

</p>
</details>



<details><summary><b> 2. Configuring SMASH </b></summary>
<p>

 Let us have a look at the JetScape configuration file:
 <img src="figs/jetscape-config-SMASH.png" alt="1" width="500"/>

 From the JetScape configuration one can only set the end time of the simulation
 and switch off all collisions. Detailed SMASH configuration is in the
 SMASH config files. They are described in detail in [SMASH user guide](http://theory.gsi.de/~smash/userguide/1.8/).
 In this tutorial we look at some of the options.

 Let's look at the SMASH config file:
 <img src="figs/smash_config.png" alt="1" width="500"/>

 Focusing on the Output section:

  ```
    Output:
        Output_Interval: 5.0
        Particles:
            Format:          ["Oscar2013"]
  ```

  This means that SMASH is going to print out all the particles in
  Oscar2013 format (a simple human readable text), and if it is required to
  print out particles in the middle of the simulation, it will do so every 5.0 fm/c.
  By default SMASH will print out only particles in the end of the simulation.
  To make it actually print out particles every 5 fm/c we need to supply our config with
  an additional `Only_Final: No` option.

  ```
    Output:
        Output_Interval: 10.0
        Particles:
            Format:          ["Oscar2013"]
            Only_Final:      No
  ```

*Let's look at the results of our simulations*
----

  The SMASH output is in the `smash_output` folder.
  If you followed previous instructions and the luck is on your side then there are 4 files in the folder:
  ```
  particles_binary.bin
  collisions_binary.bin
  particle_lists.oscar
  full_event_history.oscar
  ```

  The files (`particles_binary.bin` and `particle_lists.oscar`) as well as
  (`collisions_binary.bin` and `full_event_history.oscar`) contain the same information, but
  in different formats. Oscar files are human-readable and bin files are binary. SMASH can also
  generate outputs in ROOT, vtk, hepmc formats.
  Let's look at the contents of particle_lists.oscar, you should see something like this:

  ```
   #!OSCAR2013 particle_lists t x y z mass p0 px py pz pdg ID charge
   # Units: fm fm fm fm GeV GeV GeV GeV GeV none none e
   # SMASH-1.8
   # event 1 out 470
   200 -106.204 58.1653 -14.4014 0.938 1.26645138 -0.746754441 0.397353787 -0.092319454 2112 2364 0
   200 104.02 39.1754 98.0998 0.938 1.4867404 0.782602686 0.334508298 0.778582208 2212 907 1
   200 15.7665 -21.8512 -137.847 0.938 1.34280422 0.101448745 -0.118439561 -0.948134694 2212 2344 1
   ...
  ```

  In principle you can analyse these results using your favourite way to write scripts.
  In the last tutorial I suggested a quick and easy way to use ROOT output for analysis.
  In this tutorial, I would like to take advantage of the SMASH analysis suite, that reads in binary output.

<details><summary><b> 3. Analysis of binary output using SMASH analysis suite </b></summary>
<p>


   This will inform you about the contents of a ROOT file in a table form. You can see the columns `p0, px, py, pz`
   corresponding to particle 4-momenta. To plot rapidity distribution


   ```
     particles->Draw("0.5 * log((p0+pz)/(p0-pz))","pdgcode == 2212", "E");
   ```

 Here
 - `particles` is the name of the tree
 - `0.5 * log((p0+pz)/(p0-pz))` is the first parameter of the [Draw](https://root.cern.ch/root/html524/TTree.html#TTree:Draw) function.\
    It is the rapidity, a variable to be histogrammed. As you see, ROOT allows to put formulas there,
    which use leaves like `p0` and `pz`.
 - `pdgcode == 2212` is the second parameter of the [Draw](https://root.cern.ch/root/html524/TTree.html#TTree:Draw) function. It defines
   a cut. Here we cut on particle type, `2212` is a [PDG code](http://pdg.lbl.gov/2019/reviews/rpp2019-rev-monte-carlo-numbering.pdf) of protons.
   It is possible to combine cuts, for example `pdgcode == 2212 && sqrt(px*px + py*py) > 0.2 && t == 200.0`.
 - `E` is the third parameter of [Draw](https://root.cern.ch/root/html524/TTree.html#TTree:Draw). It is a plotting option that
   asks ROOT to show error bars.

Let's now plot a rapidity distribution for pions (plotting option `same` puts this histogram above the previous one):

```
  particles->Draw("0.5 * log((p0+pz)/(p0-pz))","pdgcode == 211 || pdgcode == 111 || pdgcode == -211", "E same");
```

Now both proton and pion histograms have the same color and you can't distinguish them. If you are in TBrowser then right-click on the points and change the color:

```
  Right-click -> SetLineAttributes
```

If you are using the ROOT inside docker without TBrowser then

```
htemp->SetLineColor(kRed);
c1->SaveAs("Rapidity_spectra_comparison.png");
```

You should be able to see the result either directly in TBrowser or by opening the file `Rapidity_spectra_comparison.png`.

<details><summary> Summary of commands to run in a ROOT environment without TBrowser </b></summary>

```
  TFile *f=new TFile("data/1/Particles.root");
  TTree *particles=(TTree*)f->Get("particles");
  particles->Scan("*");

  particles->Draw("0.5 * log((p0+pz)/(p0-pz))","pdgcode == 2212", "E");
  c1->SaveAs("Rapidity_spectrum_protons.png");

  particles->Draw("0.5 * log((p0+pz)/(p0-pz))","pdgcode == 211 || pdgcode == 111 || pdgcode == -211", "E");
  c1->SaveAs("Rapidity_spectrum_pions.png");

  particles->Draw("0.5 * log((p0+pz)/(p0-pz))","pdgcode == 2212", "E");
  particles->Draw("0.5 * log((p0+pz)/(p0-pz))","pdgcode == 211 || pdgcode == 111 || pdgcode == -211", "E same");
  htemp->SetLineColor(kRed);
  c1->SaveAs("Rapidity_spectra_comparison.png");
```
</p>
</details>


<details><summary> In TBrowser </b></summary>

```
  particles->Draw("0.5 * log((p0+pz)/(p0-pz))","pdgcode == 2212", "E");
  particles->Draw("0.5 * log((p0+pz)/(p0-pz))","pdgcode == 211 || pdgcode == 111 || pdgcode == -211", "E same");

```

</p>
</details>


Now you have a not so pretty, but very quick and functional way to analyze SMASH output. Let's look at particles in spatial coordinates.
You cannot do it in experiment, but it is easy in our case using the scatter-plots:

```
  particles->Draw("x:y:z","pdgcode == 2212");
  particles->Draw("x:y","pdgcode == 211");
```


</p>
</details>


<details><summary><b> 4. Exploring chemical and kinetic freeze-out </b></summary>
<p>

In this part we are going to discuss the chemical and kinetic freeze-out of
hadrons. First of all, do you know what chemical and kinetic freeze-outs are?
Write the definitions as you understand them in the chat.

Are hadrons frozen out immediately after the hydrodynamics is stopped
and hadronic afterburner is started? Let's try to answer this by comparing
spectra and yields from two simulations

  1. Just letting resonances decay, without any rescattering
  2. Running the full hadronic rescattering


*SMASH simulation*
----

For these simulations I have generated 100 events of particles sampled
from a hydrodynamic simulation of central Au+Au collisions at 19.6 GeV.
Download these sampled particles by [this link](https://drive.google.com/file/d/1iTLL2tjRI0f_bz8uKl5SXFLC6yMHPrM0/view?usp=sharing)
and save to `JETSCAPE/external_packages/smash/smash_code/build` folder.
We will use them as an input to SMASH.

Unpack the file:

```
  cd JETSCAPE/external_packages/smash/smash_code/build
  tar -xvf SMASH_input_particles_from_MUSIC_hydro.tar.gz
```

You should get a file `sampled_particles0`.

Next, configure SMASH to run as an afterburner. Here is the content of the SMASH config file:

```
Version: 1.8 # minimal SMASH version to use with this config file

Logging:
    default: INFO

General:
    Modus:          List
    End_Time:       100.0
    Nevents:        100
    Randomseed:     -1

Output:
    Output_Interval:  100.0
    Particles:
        Format:     ["Root"]
        Extended:   True
        Only_Final: No
    Collisions:
        Format:     ["Root"]
        Extended:   True

Modi:
    List:
        File_Directory: "."
        File_Prefix:    "sampled_particles"
        Shift_Id:       0

```

Put this into `config_SMASH_tutorial_afterburner.yaml` and run SMASH with this configuration -- it took around 5 minutes on my laptop:

```
  ./smash --inputfile config_SMASH_tutorial_afterburner.yaml
```


Now let's run SMASH starting from the same initial state, but switching
off all collisions. This is done in the SMASH config by setting option

```
Collision_Term:
    No_Collisions:  True
```

*Analysing the results of SMASH simulation*
----


Run SMASH again without collisions. Let's use ROOT TBrowser to compare the spectra.
In case you can't open it in TBrowser:

```
  TFile *f1=new TFile("data/1/Particles.root");
  TTree *particles=(TTree*)f1->Get("particles");
  particles->Scan("*");

  TFile *f2=new TFile("data/1/Collisions.root");
  TTree *collisions=(TTree*)f2->Get("collisions");
  collisions->Scan("*");
```

Let's look, for example, at pion transverse momentum spectra at midrapidity

```
  particles->Draw("sqrt(px * px + py * py)", "t == 100 && abs(0.5 * log((p0 + pz)/(p0 - pz)) < 1.0) && pdgcode == 211", "E");
```
To compare different spectra use the plotting option `same`, like we did before.
How much do pion spectra differ for the simulation with and without scattering? Repeat the same for kaons and protons.

What can you conclude from this study? Let's discuss it in the chat.

1. How much does the hadronic rescattering change the spectra?
2. What can you say about chemical freeze-out?
3. What can you say about kinetic freeze-out?

----

Now let us look at the reactions. When do the elastic and inelastic reactions stop?
Do inelastic reactions cease earlier than elastic ones? Are reactions equilibrated
at some point, i.e. do they occur at the same rate in forward and backward directions?


Looking at resonance formation and decays:

```
 collisions->Draw("t","nin == 2 && nout == 1 ");
 collisions->Draw("t","nin == 1 && nout == 2 ", "same");
```

Looking at formations and decays specifically for Delta0(1232):

```
 collisions->Draw("t","nin == 2 && nout == 1 && pdgcode[2] == 2114");
 collisions->Draw("t","nin == 1 && nout == 2 && pdgcode[0] == 2114", "same");
```

Looking at elastic and inelastic 2->2 collisions:

```
collisions->Draw("t:z","nin == 2 && nout == 2 &&  ((pdgcode[0] == pdgcode[2] && pdgcode[1] == pdgcode[3]) || (pdgcode[0] == pdgcode[3] && pdgcode[1] == pdgcode[2]))");
collisions->Draw("t:z","nin == 2 && nout == 2 && !((pdgcode[0] == pdgcode[2] && pdgcode[1] == pdgcode[3]) || (pdgcode[0] == pdgcode[3] && pdgcode[1] == pdgcode[2]))", "same");
```

#### Discussion

1. What did you learn about chemical and kinetic freeze-out?
2. Were we able to pinpoint them in a transport simulation? If yes then how? If no then why?
3. How would you proceed to study it further?

</p>
</details>


<details><summary><b> (optional) Easy SMASH results visualization: looking at VTK output with paraview </b></summary>
<p>


*Installing paraview*
----

For creating nice SMASH visualizations we will use paraview.


<details><summary> MAC  </summary>
<p>

```
brew cask install paraview
```

</p>
</details>

<details><summary> Ubuntu or other linux </summary>
<p>

```
sudo apt-get install -y paraview
```

With other linux distributives you may use *yum* instead of *apt-get*.

</p>
</details>

<details><summary> Windows </summary>
<p>

[Download](https://www.paraview.org/download/) and execute the .exe installer for Windows.

</p>
</details>

If you have some fancy operating system, then just give it up.
If you didn't manage to install paraview for more than 10 minutes, give it up
and proceed further. Paraview is nice to have, but not critical for us.


  If you didn't manage to install paraview, skip this section. It's pretty and fun, but not critical for us.


*Generating SMASH output for visualization*
----

  Let's generate the output from SMASH that paraview can read. It's called the VTK output. To switch it on
  add it to the SMASH config (config.yaml):

  ```
    Output:
        Output_Interval: 1.0
        Particles:
            Format:          ["Oscar2013", "VTK"]
            Only_Final:      No
            Extended:        True
  ```

  This is going to generate a lot of output, so let's change the time of simulation to 40 fm/c instead of 200 fm/c:

  ```
    General:
        ...
        End_Time:    40.0   # 200.0
        ...
  ```
  Run smash to get the output:

  ```
    ./smash
  ```

*Visualization*
----

  Look at the last of the `data/0`, `data/1`, `data/?` folders. Do you see a lot of `.vtk` files there?
  Let us open these vtk files. For this start `paraview`, press `File -> Open`
  and open our vtk files.

  Press a large
  ```
    Apply
  ```
  button and you should be able to see some small dots on the display. Those are our particles.
  Let's make them look bigger. Change:

  ```
    Representation: Surface -> 3D Glyphs
    Glyph Type: Arrow -> Sphere
  ```

  Now use the `Next Frame` and `Previous Frame` buttons on the top to play the movie.

  ### Challenge

  Experiment with paraview capabilities. You can change the color of spheres depending on their momenta,
  particle type, etc. You can add arrows to particles to show their momenta.

  Try to visualize a particles in a box simulation instead of collider. To run a box simulation
  change

  ```
    General:
        Modus:  Box  # previously it was Collider
  ```

  and set up the box configuration you like, see [the documentation](http://theory.gsi.de/~smash/userguide/1.8/input_modi_box_.html).
  I don't reveal all the details, you have to find them yourselves. That's why it's called *challenge*.

</p>
</details>



