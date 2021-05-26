# Philosophy

This simulates a simple **Thomson Ion Parabola Spectrometer** by means of an **adaptive stepsize RK45 Fehlberg integration method** and **OOP design**.

# Geometry
The simulated geometry is as following:

![Image of ThomsonSpectrometer_MyGeometry](https://github.com/iouatu/ThomsonSpectrometer/blob/main/My_Geometry_picture.png)

This design of the spectrometer can be found in "**D. Jung et al., Development of a high resolution and high dispersion Thomson parabola, Review of Scientific Instruments, 2011**", online at: https://aip.scitation.org/doi/10.1063/1.3523428.

Thus the **E** and **B** fields are parallel and both oriented along **y** axis, in the positive direction. The fields are a top-hat shape as a function of the z-coordinate, so no fringe-fields effects are considered.

The defining lengths are:

* the lengths over which the E and B fields are non-zero, ```l_E``` and ```l_B```, equal to each other. User asked for input for ```l_E``` only.
* the free-particle flight lengths (drift lengths) ```D_E``` and ```D_B```. These measure the distance along the z-axis from the end of the E and B fields respectively, to the detector screen position. ```D_E``` and ```D_B``` are equal to each other and the user is asked for input for ```D_E``` only.
* the z-coordinate of the detector screen ```z_det```, relative to the origin of coordinates (i.e. the aperture z-coordinate). User is asked for input for ```z_det```.
* the y-coordinate of the bottom electrode ```y_bottom_elec```, relative to the origin of coordinates (i.e. the aperture y-coordinate). User is asked for input for ```y_bottom_elec```.


# Aperture
The incident particles come towards an aperture with initial velocity oriented along **z** axis only (positive initial velocities). 

The aperture can be either pointlike or non-pointlike.

If selected to be non-pointlike, it can extend along **x** axis only, along **y** axis only, or along both **x** and **y** axes (so it becomes a circle).

The extension in any of the above cases is input from the user from keyboard, in SI units (meters). 

This translates to the fact that particles' initial x and y coordinates at the aperture location will vary between 0.0 m and ```Rx``` for x axis, and between 0.0 m and ```Ry``` for y axis, respectively (instead of being equal to 0.0 and 0.0, for all particles) and these coordinates values (x and y initial values) will be drawn at random, with uniform probability, from the range spanning their own two extreme values (0.0 and ```Rx```, 0.0 and ```Ry```, respectively), independently of each other (x draws don't influence y draws and vice-versa).


# Particles
The incident particles are input by the user in an interactive fashion.
They are contained in chunks. A chunk is composed of particles of the same species and can be of any size (integer number of particles in a chunk).
A chunk is input by the user by specifying its name, its input Kinetic Energy in MeV, the number of particles wanting to be simulated in this chunk, and the option for the aperture.

#### Option 1

If the ***option is chosen to be 1***, then the particles are shot towards a purely pointlike aperture (initial x, y, z coordinates of all the particles will be identically 0.0 m), with their velocities drawn according to the sub-option chose.

* If suboption is chosen to be 1: in this chunk, all particles' velocities are set equal to the velocity value resulted from the conversion ```from_KEineV_to_uzinit(input_KE_expressed_in_eV)```

* If suboption is chosen to be 2: in this chunk, particles' velocities are drawn from a Gaussian distribution with mean given by the input initial Kinetic Energy and sigma = mean / 10.

* If suboption is chosen to be 3 (**not supported yet**): particles' input velocities are read from an input file provided by the user.

#### Option 2
If the ***option is chosen to be 2***, then the particles are shot towards a non-pointlike aperture and their initial x and y coordinates will be set according to whether the aperture extends along x or along  y or along both axes (see above).

* If suboption is chosen to be 1: in this chunk, all particles' velocities are set equal to the velocity value resulted from the conversion ```from_KEineV_to_uzinit(input_KE_expressed_in_eV)```

* If suboption is chosen to be 2: in this chunk, particles' velocities are drawn from a Gaussian distribution with mean given by the input initial Kinetic Energy and sigma = mean / 10.

* If suboption is chosen to be 3 (**not supported yet**): particles' input velocities are read from an input file provided by the user.


#### Species types

Chunks can be of the following types (at the moment):
```diff
- [proton, C0+, C1+, ... , C6+, Xe0+, Xe1+, ... , Xe54+]
```

# Integration
### RKF45 adaptive stepsize
The code performs RK45 Fehlberg integration for all the input chunks, for all the particles from each chunk, in inputted `E` and `B` fields both of length `l_B`. Not-so-technical details about this integration method and sample pseudocode in Fortran can be found in "**W. Press, S. Teukolsy, Adaptive Stepsize Runge-Kutta Integration, Computers in Physics 6, 188 (1992)**" online at: https://doi.org/10.1063/1.4823060.


The integration, for each particle, finishes when:
1) The particle has exited the B-field region (has `z` > `l_B`)
2) The particle has hit the bottom electrode (see geometry diagram) (has `y` > `y_bottom_elec`)
3) The number of iterations of the integration while-loop has reached nmax (usually a large number which is not attained in practice if the Physics is chosen in a sensible way).


### Ballistic translation
The code then performs ballistic translation in 3D space towards the detector screen, from the end of the fields to the z-location of the detector screen, denoted by `z_det`.
When `z_det` is reached, the **x** and **y** coordinates of the particles are recorded and scattered on a x-y scatter plot. 
In that plot, each color represents a different chunk of particles.


# Results and plotting
The end of `main()` inside `main.py` can be changed as needed in order to perform the plotting the user wants.

# Examples of usage of the code
The usage of the code is straightforward and the input requested from the user is self-explanatory if the geometry picture is kept in mind (at hand up until becoming familiarized with the notation).

# Dependencies
The code has been tested on **Python 3.8.5** with the following dependencies:

* numpy 1.20.2

* scipy 1.6.2

Code is run via `$ cd /dir/in/which/code_is_extracted` followed by `$ python3 main.py`. By default, graphs are saved in `/dir/in/which/code_is_extracted`.
