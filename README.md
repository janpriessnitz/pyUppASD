# pyUppASD
A python wrapper for UppASD atomistic spin dynamics package

pyUppASD is a wrapper library which simplifies working with UppASD software.
Users can programatically define experiment configuration, launch simulations,
manipulate and plot the resulting data, all in the Python language in a simple way.

### Prerequisites

- Python3
- compiled UppASD: environment variable SD_PATH must be defined and must point to UppASD executable (e. g. `export SD_PATH=/home/jp/UppASD/bin/sd.gfortran`)
- numpy, matplotlib
- pyUppASD package in Python path: can be done through appending pyUppASD package path to PYTHONPATH environment variable (e. g. `export PYTHONPATH=$PYTHONPATH:/home/jp/pyUppASD`)

### How to run a simulation

A specific experiment simulation is run by writing the experiment Python script and then executing it.

The experiment script should do the following:
1. Define `pyUppASD.config.InpsdFile` object, which represents UppASD `inpsd.dat` file and all other possible configuration files.
2. Launch UppASD using `pyUppASD.launcher.SDLauncher` object.
3. Process the simulation result, stored in `pyUppASD.launcher.Result` object.
4. (Plotting): provide data from `Result` object to one of the plotting functions in `pyUppASD.vis` file, such as `vis.anim_mag()`, which creates an animation file of the simulated lattice throughout time. 

### Examples

Example experiment scripts are located in directory `examples/`