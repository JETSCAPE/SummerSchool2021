# July 27 Bayesian Overview

## Relevent Notebook

### Bayesian-Inference-Pendulum.ipynb

1. Make sure the docker container has been built according to the main instructions.

Navigate to the day's directory and `git pull` to ensure everything is up to date.

2. Launch Jupyter Notebook

`jupyter-notebook --ip 0.0.0.0 --no-browser`

There will be some printouts, and at the end there will be a URL like

`http://127.0.0.1:8888/?token=....`
Copy the full address (including the token) into a web browser, and verify that you can see a jupyter notebook page with directories.

If you are working on a remote machine, we need to forward the correct port, for example

`ssh -L 8888:127.0.0.1:8888 XXX@XXX.XX`

3. Open the notebook for the day.

In this example, we will see how Bayesian tools are used in practice within a Bayesian modeling workflow. Exercises do not require writing new code, but instead require going back, modifying existing code, and investigating directed questions. 

Bonus information at the end of the notebook demonstrates the calculation of the KL divergence as well as the Bayes evidence.

4. After the session, review the homework exercises.

Exercises 1-3 require some coding, but are mostly about getting familiar with Gaussian Processes and Latin Hypercube Sampling. This will be key information to be familiar with before the next two days' sessions.

