# SMASH hadronic transport hands-on session

### Our goals
 - Learn to use SMASH as a hadronic afterburner
 - Understand SMASH inputs: resonances and their decays, switching on and off different reactions
 - Understand SMASH outputs: particles and collision history
 - Physics project: ``Life and death of Delta-resonance''

*To begin* add your name to the [table](https://docs.google.com/spreadsheets/d/e/2PACX-1vTo_TeWIkXPCh4PBpLBNZac_pkB6pao6ynenWf2RNMZDHjeT4O1Mg3xBPx6nkitxthQq7GRothvNjCC/pubhtml) to mark your progress.
Then follow the steps below.

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

SMASH is a hadronic transport code. In JETSCAPE it simulates multiple hadron-hadron scatterings in the final dilute stage of the fireball evolution.
Look at the visualization at the [official SMASH webpage](https://smash-transport.github.io/). At the end of our session you might be able
to create similar visualizations, configure SMASH and analyze its output.

</p>
</details>



<details><summary><b> Making sure prequisites are ready </b></summary>
<p>

1. I assume that you have followed the [general school instructions](https://github.com/JETSCAPE/SummerSchool2021/blob/master/README.md) and have
docker installed. You really need docker to proceed.

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

# Download SMASH and compile SMASH as library
# This takes around 5 minutes on laptop
./get_smash.sh

cd jetscape-docker/JETSCAPE/build
cmake .. -DUSE_MUSIC=ON -DUSE_ISS=ON -DUSE_SMASH=ON

# Compiles JetScape+MUSIC+SMASH
# This takes around 7 minutes on laptop
make -j4
```

Now let's try to run SMASH. Starting default smash run:

```
./smash
```

Print out SMASH version:

```
./smash --version
```

Prints the list of all SMASH command line options

```
./smash --help
```

</p>
</details>



<details><summary><b> 2. Configuring SMASH </b></summary>
<p>
  What SMASH is going to simulate depends on what you ask it.
  By default it simulates a Au+Au collision at 1.23 GeV per nucleon in the lab frame.
  In the end we want to use SMASH as a hadronic afterburner, so let's learn to configure it.
  You can learn how to do it by yourself from the detailed [SMASH user guide](http://theory.gsi.de/~smash/userguide/1.8/),
  but this tutorial is intended to make your life a bit simpler. So let's go
  step by step.

  SMASH is controlled in two ways:

  - By configuration file\
    By default this file is called config.yaml. Let's copy
    it to JETSCAPE_school.yaml and make smash read configuration from it:

    ```
      cp config.yaml JETSCAPE_school.yaml
      ./smash --inputfile JETSCAPE_school.yaml
    ```

  - By command-line options\
    They can overrule the options in the file. For example,

    ```
      ./smash --inputfile JETSCAPE_school.yaml --config "General: {End_Time: 40.0}"
    ```
    will change the simulation end time from the 200 fm/c in the config to 40 fm/c.

  Now let us look inside the `JETSCAPE_school.yaml`. For now let's focus
  on the Output section:

  ```
    Output:
        Output_Interval: 10.0
        Particles:
            Format:          ["Oscar2013"]
  ```

  This means that SMASH is going to print out all the particles in
  Oscar2013 format (a simple human readable text), and if it is required to
  print out particles in the middle of the simulation, it will do so every 10.0 fm/c.
  By default SMASH will print out only particles in the end of the simulation.
  To make it actually print out particles every 10 fm/c we need to supply our config with
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

  By default SMASH output will be in the folders `data/0`, `data/1`, etc.
  Open the latest `data/?` folder and look at the files there.
  There is config.yaml there, it is just a full copy of SMASH configuration
  to keep record of what was done. And there is a `particle_lists.oscar` file. This is the one we want to look at.
  It contains the particles that SMASH generated. Open it and you should see something like this:

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

  You can analyse these results already using your favourite way to write scripts, but at this tutorial I want to show some
  convenient approaches to perform quick analysis without writing much code.
  For this we want output in a ROOT format.


*Let's generate ROOT output with more events for analysis*
----

  Create a `config_SMASH_tutorial_collider.yaml` file with the following contents:

  ```
    Version: 1.8 # minimal SMASH version to use with this config file

    Logging:
        default: INFO

    General:
        Modus:          Collider
        Time_Step_Mode: Fixed
        Delta_Time:     0.1
        End_Time:       200.0
        Randomseed:     -1
        Nevents:        50

    Output:
        Output_Interval: 10.0
        Particles:
            Format:          ["Oscar2013", "Root"]

    Modi:
        Collider:
            Projectile:
                Particles: {2212: 79, 2112: 118} #Gold197
            Target:
                Particles: {2212: 79, 2112: 118} #Gold197

            E_Kin: 1.23
            Fermi_Motion: "frozen"
  ```

  This is almost the default configuration, but we have set `Nevents:  50` and added Root output.
  Run smash with this config:

  ```
    ./smash --inputfile config_SMASH_tutorial_collider.yaml
  ```


  Next we will look at the Root output.

</p>
</details>



<details><summary><b> 3. Analysis of ROOT output, looking at rapidity distributions </b></summary>
<p>


<details><summary> If you have ROOT installed on your computer (*not* in docker enviroment) </summary>
<p>

  1. Exit the docker environment by typing `exit`.
  2. Go to the `jetscape-docker/JETSCAPE/external_packages/smash/smash_code/build` folder
  3. Start ROOT and run the TBrowser:

     ```
       root -l
       new TBrowser
     ```

    This should open a browser. Use it to open the Root file `Particles.root` you generated previously from SMASH simulation.
    Remember, that by default SMASH output is in the latest of `data/0`, `data/1`, `data/?` folders.
    In the left panel of the browser you should see a tree called `particles`. Double-click on it and you will see many
    leaves. Double-click on a leaf shows a histogram. In this way you can see a distribution of x, y, z coordinates,
    times of output, particle energies p0, and momenta px, py, pz.
  4. Enter commands in the `Command(local)` panel, for example:

     ```
       particles->Draw("0.5 * log((p0+pz)/(p0-pz))","pdgcode == 2212", "E");
     ```

     Now left-click on the histogram canvas to update it.
</p>
</details>



Suppose that you do not have ROOT installed on your laptop or something didn't work well with your TBrowser.
You still have ROOT in your docker environment, just some nice visuals are not going to work. The way to proceed is the following.

1. Make sure you are in the docker environment. If not then run `docker start -ai myJetscape` to enter it.
2. Go to the `jetscape-docker/JETSCAPE/external_packages/smash/smash_code/build` folder
3. In the docker environment run

   ```
     root -l
   ```

   This should start a ROOT shell. You will see a `root [0]` prompt.


   Let's do something practical. We have generated 50 events previously, now let's compare pion to proton rapidity distributions.
   In the ROOT environment open the file you generated. Remember, that by default SMASH output is in the latest of `data/0`, `data/1`, `data/?` folders.

   ```
     TFile *f=new TFile("data/1/Particles.root");
     TTree *particles=(TTree*)f->Get("particles");
     particles->Scan("*");
   ```

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



