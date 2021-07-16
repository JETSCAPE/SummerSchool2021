# SMASH hadronic transport hands-on session

### Our goals
 - Learn to use SMASH as a hadronic afterburner
 - Understand SMASH inputs: resonances and their decays, switching on and off different reactions
 - Understand SMASH outputs: particles and collision history
 - Physics project: Life and death of rho-resonance

To begin add your name to the [table](https://docs.google.com/spreadsheets/d/e/2PACX-1vTo_TeWIkXPCh4PBpLBNZac_pkB6pao6ynenWf2RNMZDHjeT4O1Mg3xBPx6nkitxthQq7GRothvNjCC/pubhtml) to mark your progress.
Then follow the steps below.

It would be great if you perform step 1. in advance,
because compilation of SMASH library takes around 5 minutes, compilation
of JetScape with SMASH takes around 7 minutes, running and getting 10 events takes
around 7 minutes = around 20 minutes total.


<details><summary> My personal docker cheat sheet </summary>
<p>

I'm not an active docker user, so here I assemble commands that were useful for me:

```bash
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

```bash
ls ~/jetscape-docker
```

You need to make sure the following folders are present,

* JETSCAPE
* SummerSchool2021

Try the following command to make sure you are ready

```bash
    docker start -ai myJetscape
```

<details><summary><b> 1. Compiling JetScape with SMASH in docker environment </b></summary>
<p>

Go to the docker environment. If you didn't start it yet, start by

```bash
  docker start -ai myJetscape
```

Compiling JetScape with MUSIC + iSS + SMASH:

```bash
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

```bash
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
 <img src="pics/jetscape-config-SMASH.png" alt="1" width="500"/>

 From the JetScape configuration one can only set the end time of the simulation
 and switch off all collisions. Detailed SMASH configuration is in the
 SMASH config files. They are described in detail in [SMASH user guide](http://theory.gsi.de/~smash/userguide/1.8/).
 In this tutorial we look at some of the options.

 Let's look at the SMASH config file:
 <img src="pics/smash_config.png" alt="1" width="500"/>

 Focusing on the Output section:

  ```yaml
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

  ```yaml
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

  ```bash
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

</p>
</details>



<details><summary><b> 4. Exploring chemical and kinetic freeze-out </b></summary>
<p>

What can you conclude from this study? Let's discuss it in the chat.

1. How much does the hadronic rescattering change the spectra?
2. What can you say about chemical freeze-out?
3. What can you say about kinetic freeze-out?

----

Now let us look at the reactions. When do the elastic and inelastic reactions stop?
Do inelastic reactions cease earlier than elastic ones? Are reactions equilibrated
at some point, i.e. do they occur at the same rate in forward and backward directions?


#### Discussion

1. What did you learn about chemical and kinetic freeze-out?
2. Were we able to pinpoint them in a transport simulation? If yes then how? If no then why?
3. How would you proceed to study it further?

</p>
</details>
