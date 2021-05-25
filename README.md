# ThomsonSpectrometer

This simulates a simple Thomson Ion Parabola Spectrometer by means of an adaptive stepsize RK45 Fehlberg integration method and OOP design.
The geometry is as following:

![Image of ThomsonSpectrometer_MyGeometry](https://.github.com/images/TS_MyGeometry.png)

Thus the **E** and **B** fields are parallel and both oriented along **y** axis, in the positive direction.
The incident particles come towards an aperture with initial velocity oriented along **z** axis only (positive initial velocities). 
The aperture can be either pointlike or non-pointlike.
If selected to be non-pointlike, it can extend along **x** axis only, along **y** axis only, or along both **x** and **y** axes (so it becomes a circle).
The extension in any of the above cases is of radius R = 0.005 m. 
This translates to the fact that particles' initial x and y coordinates at the aperture location will vary between 0.0 m and 0.01 m (instead of being equal to 0.0 for all particles) and these coordinates values (x and y initial values) will be drawn at random, uniformly between the two extremes, independently of each other.

The incident particles are input by the user in an interactive fashion.
They are contained in chunks. A chunk is composed of particles of the same species and can be of any size (integer number of particles in a chunk).
A chunk is input by the user by specifying its name, its initial Kinetic Energy, the number of particles wanting to be simulated in this chunk, and the option for the aperture.
If the option is chosen to be 1, then the particles are shot towards a purely pointlike aperture (initial x, y, z coordinates of all the particles will be identically 0.0 m), with their velocities drawn from a Gaussian Distribution with mean given by the input Kinetic Energy and sigma = mean / 10.
If the option is chosen to be 2, then the particles are shot towards a non-pointlike aperture and their initial x and y coordinates will be set according to whether the aperture extends along x or along  y or along both axes (see above).
Chunks can be of the following types (at the moment):

[proton, C0+, C1+, ... , C6+, Xe0+, Xe1+, ... , Xe54+]

The code performs RK45 Fehlberg integration for all the input chunks, for all the particles from each chunk, in inputted E and B fields both of length l_B.
The integration, for each particle, finishes when:
1) The particle has exited the B-field region (has z > l_B)
2) The particle has hit the bottom electrode (see geometry diagram) (has y > y_bottom_elec)
3) The number of iterations of the integration while-loop has reached nmax (usually a large number which is not attained in practice if the Physics is chosen in a sensible way).

The code then performs ballistic translation in 3D space towards the detector screen, from the end of the fields to the z-location of the detector screen, denoted by z_det.
When z_det is reached, the **x** and **y** coordinates of the particles are recorded and scattered on a x-y scatter plot. 
In that plot, each color represents a different chunk of particles.

The end of main() function inside main.py can be changed as needed in order to perform the plotting you want.
