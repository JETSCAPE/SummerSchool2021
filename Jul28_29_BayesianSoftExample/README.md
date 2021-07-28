# July 28 (2h) JETSCAPE Bayesian Example.
## Relevent Notebook

### SimpleGaussianProcess.ipynb and BayesForSimpleModel.ipynb

1. Clone the repository inside the JETSCAPE-docker folder. (You can skip this and go to the next step if you have already cloned it!)
````
git clone https://github.com/JETSCAPE/SummerSchool2021.git
````

2. Get the most recent version of the repo.
> Go inside SummerSchool2021 folder

````
git pull origin master
````

3. Start the docker container 
````
docker start -ai myJetscape
````

4. Update the seaborn package to a newer version ( If you did this already as in the instructions [here](https://github.com/JETSCAPE/SummerSchool2021/blob/master/README.md) you can skip this step]
````
pip3 install --upgrade seaborn==0.11.0
````

5. Open the jupyter notebook

````
jupyter-notebook --ip 0.0.0.0 --no-browser
````

There will be some printouts, and at the end there will be a URL like

````
http://127.0.0.1:8888/?token=....
````

Copy the full address (including the token) into a web browser, and verify that you can see a jupyter notebook page with directories.

Open *[SimpleGaussianProcess.ipynb](https://github.com/JETSCAPE/SummerSchool2021/blob/master/Jul28_29_BayesianSoftExample/SimpleGaussianProcess.ipynb)*. In this exercises, we will introduce the idea of a Gaussian Process emulator (GP). It will be an essential ingredient for the Bayesian analysis of complex model. We will spend about 30 mins on this topic.



Open *[BayesForSimpleModel.ipynb](https://github.com/JETSCAPE/SummerSchool2021/blob/master/Jul28_29_BayesianSoftExample/BayesForSimpleModel.ipynb)*. In this exercises, we will apply the emulator-assisted Bayesian analysis to a toy model of bulk physics. Assuming a simple response of anisotropy flow $v_2$ to the initial QGP eccentricity and an effective shear-viscosity, we will see the role of model sensitivity, uncertainty propagation, and parameter maginalization on the extraction of the temperature dependent shear viscosity. This example is also a warm-up for the following full example.

> Sample results: prior and posterior for temperature dependent QGP specefic Shear viscosity using a **toy model** with **peseudo experimental data**.
<p>
<img src="https://github.com/JETSCAPE/SummerSchool2021/blob/master/Jul28_29_BayesianSoftExample/SimpleBulk/plots/Posterior_validation.png" width="300" />

<img src="https://github.com/JETSCAPE/SummerSchool2021/blob/master/Jul28_29_BayesianSoftExample/SimpleBulk/plots/Posterior_of_eta_s.png" width="300"  />
 </p>

# July 29 (1.5 hour) JETSCAPE Bayesian Example.
## Relevent Notebook


### BayesianParameterEstimationCodeForRelativisticHeavyIonCollisions-JS21.ipynb

1. Clone the repository inside the JETSCAPE-docker folder. (You can skip this and go to the next step if you have already cloned it!)
````
git clone https://github.com/JETSCAPE/SummerSchool2021.git
````

2. Get the most recent version of the repo.
> Go inside SummerSchool2021 folder

````
git pull origin master
````

3. Start the docker container 
````
docker start -ai myJetscape
````

4. Update the seaborn package to a newer version ( If you did this already as in the instructions [here](https://github.com/JETSCAPE/SummerSchool2021/blob/master/README.md) you can skip this step]
````
pip3 install --upgrade seaborn==0.11.0
````

5. Open the jupyter notebook

````
jupyter-notebook --ip 0.0.0.0 --no-browser
````

There will be some printouts, and at the end there will be a URL like

````
http://127.0.0.1:8888/?token=....
````

Copy the full address (including the token) into a web browser, and verify that you can see a jupyter notebook page with directories.

Open *[BayesianParameterEstimationCodeForRelativisticHeavyIonCollisions-JS21.ipynb](https://github.com/JETSCAPE/SummerSchool2021/blob/master/Jul28_29_BayesianSoftExample/BayesianParameterEstimationForRelativisticHeavyIonPhysics-JS21.ipynb)*. In this session we will do a full Bayesian parameter extraction for one of the JETSCAPE relativistic heavy ion collision models using pre-generated simulation data and with **peseudo experimental data**. The peseudo experimental data is generated from our simulation model for known set of model parameters. We will compare the extracted model parameter values with the **true model parameters** to validate the Baysian work flow. After validation the final step would be the Bayesian parameter extraction with the real experimental data. We leave it as an exercise for the interested participants. 

#### Posteriors using the *[BayesianParameterEstimationCodeForRelativisticHeavyIonCollisions-JS21](https://github.com/JETSCAPE/SummerSchool2021/blob/master/Jul28_29_BayesianSoftExample/BayesianParameterEstimationForRelativisticHeavyIonPhysics-JS21.ipynb)*


> Posterior for temperature dependent specefic Shear viscosity.
![alt text](https://github.com/JETSCAPE/SummerSchool2021/blob/master/Jul28_29_BayesianSoftExample/Results/FigureFiles/shear_posterior.png)



> Posterior for temperature dependent specefic Bulk viscosity.
![alt text](https://github.com/JETSCAPE/SummerSchool2021/blob/master/Jul28_29_BayesianSoftExample/Results/FigureFiles/bulk_posterior.png)



> Posterior for remaining parameters in the model.
![alt text](https://github.com/JETSCAPE/SummerSchool2021/blob/master/Jul28_29_BayesianSoftExample/Results/FigureFiles/JETSCAPE_bayesWithoutViscosity.png)

