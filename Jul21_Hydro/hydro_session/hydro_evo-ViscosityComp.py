#!/usr/bin/env python3

from numpy import *
from os import path
home = path.expanduser("~")

import matplotlib.pyplot as plt

# define plot style
width = 0.05
plotMarkerSize = 8
labelfontsize = 15
import matplotlib as mpl
mpl.rcParams['figure.figsize'] = [6., 4.5]
mpl.rcParams['lines.linewidth'] = 2
mpl.rcParams['xtick.top'] = True
mpl.rcParams['xtick.labelsize'] = 15
mpl.rcParams['xtick.major.width'] = 1.0
mpl.rcParams['xtick.minor.width'] = 0.8
mpl.rcParams['xtick.minor.visible'] = True
mpl.rcParams['xtick.direction'] = "in"
mpl.rcParams['ytick.right'] = True
mpl.rcParams['ytick.labelsize'] = 15
mpl.rcParams['ytick.major.width'] = 1.0
mpl.rcParams['ytick.minor.width'] = 0.8
mpl.rcParams['ytick.minor.visible'] = True
mpl.rcParams['ytick.direction'] = "in"
mpl.rcParams['legend.fontsize'] = 15
mpl.rcParams['legend.numpoints'] = 1
mpl.rcParams['font.size'] = 15
mpl.rcParams['savefig.format'] = "pdf"

working_path = path.join(home, "JETSCAPE/build")


# change the following line to your result folder(s)
RunFolder1 = "Run_shear_only"
RunFolder2 = "Run_shear_and_bulk"

# label our calculations
labels=[r"$\eta/s = 0.15$", r"$\eta/s = 0.15 + \zeta/s(T)$"]


# load the data table(s)
data1 = loadtxt(path.join(working_path, RunFolder1,
                          "momentum_anisotropy_eta_-0.5_0.5.dat"))
data2 = loadtxt(path.join(working_path, RunFolder2,
                          "momentum_anisotropy_eta_-0.5_0.5.dat"))
ecc_data1 = loadtxt(path.join(working_path, RunFolder1,
                              "eccentricities_evo_eta_-0.5_0.5.dat"))
ecc_data2 = loadtxt(path.join(working_path, RunFolder2,
                              "eccentricities_evo_eta_-0.5_0.5.dat"))


# averaged Temperature evolution
fig = plt.figure()
plt.plot(data1[:, 0], data1[:, -1], '-k', label=labels[0])
plt.plot(data2[:, 0], data2[:, -1], '--r', label=labels[1])
plt.legend(loc=0)
plt.xlabel(r"$\tau$ [fm]")
plt.ylabel(r"$\langle T \rangle$ [GeV]")
plt.tight_layout()
plt.savefig("RunViscosityComp_avgT_evo")


# compute the average transverse velocity
gamma = data1[:, -2]
v_avg1 = sqrt(1. - 1./gamma**2.)
gamma = data2[:, -2]
v_avg2 = sqrt(1. - 1./gamma**2.)
fig = plt.figure()
plt.plot(data1[:, 0], v_avg1, '-k', label=labels[0])
plt.plot(data2[:, 0], v_avg2, '--r', label=labels[1])
plt.legend(loc=0)
plt.xlabel(r"$\tau$ [fm]")
plt.ylabel(r"$\langle v \rangle$")
plt.tight_layout()
plt.savefig("RunViscosityComp_avgv_evo")


# evolution of spatial eccentricity
n = 2 # n defines which order of ecc_n we want to see
fig = plt.figure()
plt.plot(ecc_data1[:, 0], ecc_data1[:, n], '-k', label=labels[0])
plt.plot(ecc_data2[:, 0], ecc_data2[:, n], '--r', label=labels[1])
plt.legend(loc=0)
plt.xlabel(r"$\tau$ [fm]")
plt.ylabel(r"$\epsilon_{}$".format(n))
plt.tight_layout()
plt.savefig("RunViscosityComp_ecc{}_evo".format(n))



# evolution of momentum anisotropy
fig = plt.figure()
plt.plot(data1[:, 0], data1[:, 2], '-k', label=labels[0])
plt.plot(data2[:, 0], data2[:, 2], '--r', label=labels[1])
plt.legend(loc=0)
plt.xlabel(r"$\tau$ [fm]")
plt.ylabel(r"$\langle \epsilon_p \rangle$")
plt.tight_layout()
plt.savefig("RunViscosityComp_momentumaniso_evo")
