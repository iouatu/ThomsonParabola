import numpy as np

class Species:
    """ Class used to represent 1 "particle". This is usually an ion, but can be anything as long as its name is in the list. 

    Attributes
    ----------
    _name : str
    _mass : float (in SI, units of Kg)
    _charge : float (in SI, units of Columb C)
    _qonm : float (in SI, units of Coulomb/Kg)
    x : float (where the particle is along the x-axis)
    y : float (where the particle is along the y-axis)
    z : float (where the particle is along the z-axis)
    ux : float (velocity of particle along x-axis)
    uy : flaot (velocity of particle along y-axis)
    uz : float (velocity of particle along z-axis)

    Methods
    -------
    Species_get_xyz():
        Returns a np array shape (3,) with current spatial coordinates of the particle. Position indexed 0 of that array is x-coord, indexed 1 is y-coord.
    
    Species_get_uxuyuz():
        Returns a np array shape (3,) with current velocities along x,y,z of the particle. Position indexed 0 of that array is x-velocity, ...
    
    Species_push_from_origin_to_endoffields():
        Performs integration in time of EOM's via adaptive step-size RK45 Felhberg method, given initial conditions for x,y,z, ux,uy,uz, and an initial step-size.
        Calls RK45integrator() from the Species class.
        Returns a np array shape (6,): [x,y,z, ux,uy,uz] , with conditions at the end of E/B fields region.

    @staticmethod
    Species_push_from_endoffields_to_detector(conds, z_det):
        Given initial conditions (conds), propagates (balistically) the particle from the end of E/B fields region to the detector screen (placed at z_det)
        Returns a np array size (2,) with the x,y coordinates of the particle when it reaches the detector screen. 
        arguments:
            conds: np.array of shape (6,) which represent the x,y,z,ux,uy,uz at end of RK45 integration
            z_det: float, represents where the detector (screen) is placed along z-axis, in SI (meters)
    """

    def __init__(self, name, mass, charge, r, velo):
        # r is a np array of shape (3,) , velo is a np array of shape (3,)
        self._name = name # for identification purposes
        self._mass = mass # underscore means the attribute is protected
        self._charge = charge
        self._qonm = charge / mass
        x, y, z = r # unpack the input argument to __init__()
        self.x = x
        self.y = y
        self.z = z
        #mean, sigma = distr # unpack distr (a list of 2 floats)
        #self._mean = mean
        #self._sigma = sigma
        # self._no_of_parts = uzs_at_t0.shape[0]
        #self._uzs_at_t0 = self.draw_from_Gaussian()
        ux, uy, uz = velo # velo is an input argument to the CTOR
        #self.ux = np.zeros( (self._no_of_parts, ) ) # at t0
        self.ux = ux
        self.uy = uy
        self.uz = uz
        #self.uy = np.zeros( (self._no_of_parts, ) ) # at t0
        #self.uz = uzs_at_t0 # at t0

    def __str__(self):
        return "A {} species with mass={} , charge={}, no_of_parts={},".format(self._name, self._mass, self._charge, self._no_of_parts)
    def __repr__(self):
        return f'Species(name={self._name}, mass={self._mass}, charge={self._charge}, r=[{self.x, self.y, self.z}], distr=[{self._mean, self._sigma}], no_of_parts={self._no_of_parts})'
    
    def Species_get_xyz(self):
        return np.array([self.x, self.y, self.z]) # shape (3,)

    def Species_get_uxuyuz(self):
        return np.array([self.ux, self.uy, self.uz]) # shape (3,)

    # def RK45integrator(self, yscal, l_B, y_bottom_elec): # member function of the Species() class
    #     counter = 0
    #     nmax = 10**4
    #     steps_accepted = 0
    #     epsilon_0 = 10**(-20)
    #     t = 0
    #     dt = 10**(-50) # initial try for the timestep dt
    #     ts = []
    #     beta = 0.9
    #     vec = np.array([self.x,self.y,self.z,  self.ux,self.uy,self.uz])
    #     #vec = conds # conds is a np.array [x, y, z, ux, uy, uz], shape (6,)
    #     z_to_compare = 0.0 # initial z-value for the comparison used to see if we need to stop RK45 routine or not
    #     y_to_compare = 0.0  # initial y-value for the comparison used to see if we need to stop RK45 routine or not
    #     results = []
    #     ERRCON = (beta/5.)**(5) # cryptic value taken and used as from Press and Teukolsky, 1992, Adaptive Stepsize RK Integration paper
    #     global no_of_particles_which_haveexitB
    #     global no_of_particles_which_havehitelectrode
    #     while(counter <= nmax):
    #         counter += 1 # we performed 1 iteration of the while-loop!
    #         if (z_to_compare >= l_B): # free particle - flight
    #             no_of_particles_which_exitB += 1
    #             break
    #         if (y_to_compare >= y_bottom_elec):
    #             no_of_particles_which_hitelectrode += 1
    #             break
    #         container_from_RKF4method = get_RKF4_approx(t, vec, dt, self._qonm)
    #         RKF4 = container_from_RKF4method[0] # RKF4 method's approximation for the 6 odes' solutions at t_{n+1}. returns a np array of 6 floats because we have x,y,z,ux,uy,uz
    #         Ks =  container_from_RKF4method[1:] # a list of 5 np arrays (K1--->K5), each np array containing 6 floats
    #         RKF5 = get_RKF5_approx_efficiently(t, vec, dt, Ks, self._qonm) # a np.array with 6 floats in it
    #         y_to_compare = RKF4[1]
    #         z_to_compare = RKF4[2]
    #         scaled_errors_at_this_step = [ abs( (RKF5[i] - RKF4[i]) / yscal[i] ) for i in range(3) ] # i runs from 0-->2 (including 2), only care about error on x,y,z and not on ux,uy,uz 
    #         max_from_scalederrors_at_this_step = np.max(scaled_errors_at_this_step)
    #         if (max_from_scalederrors_at_this_step < epsilon_0 and max_from_scalederrors_at_this_step != 0.0): # good!
    #             # yes, step accepted! need optimal timestep (can increase it!)
    #             steps_accepted += 1
    #             ts.append(t)
    #             dt_new = beta * dt * (epsilon_0/max_from_scalederrors_at_this_step)**(0.25) 
    #             if (max_from_scalederrors_at_this_step <= (ERRCON * epsilon_0)): # fractional error is not that small, can increase timestep according to the found optimal value
    #                 dt_new = 5 * dt
    #             dt = dt_new
    #             results.append(RKF4)
    #             vec = RKF4 # for next iteration of the while-loop
    #         else:
    #             if (max_from_scalederrors_at_this_step == 0.0): # it's perfect!
    #                 steps_accepted += 1
    #                 ts.append(t)
    #                 t += dt
    #                 dt_new = 10 * dt # artificially increase the timestep, but not as dt_new dictates (that increase would dictate dt_new = inf for when errors = 0)
    #                 dt = dt_new
    #                 results.append(RKF4)
    #                 vec = RKF4
    #             else: # means that max_from_scalederrors_at_this_step > epsilon_0 and max_from_scalederrors_at_this_step != 0
    #                 # no, step not accepted. reiterate step using a lower timestep
    #                 dt_new = beta * dt * (epsilon_0/max_from_scalederrors_at_this_step)**(0.2)
    #                 if (dt_new < 0.01 * dt): # dt_new is really really small
    #                     dt_new = 0.01 * dt
    #                 dt = dt_new
    #     print("we exited the while-loop!")
    #     ts = np.array(ts)
    #     results = np.array(results) # all the integration timesteps laid down vertically. x,y,z, ux,uy,uz laid down horizontally across each line (across each integration timestep)
    #     return results[-1, :] # these results are from when: 1) particle has just hit bottom detector OR 2) particle has just exited the fields region at z = l_B
    #     # results[-1, :] is shape (6,)


    def Species_push_from_origin_to_endoffields(self):
        # use the RK45 integrator designed for l_E = l_B
        # initial_conds = np.array([self.x, self.y, self.z, self.ux, self.uy, self.uz])
        results_at_endoffields = self.RK45integrator(yscal_maxvalues, l_B, y_bottom_elec) # kinda useless? why not use the RKF45integrator() method directly?
        return results_at_endoffields # a numpy array shape (6,): [x,y,z, ux,uy,uz] , at end of E and B fields/

    @staticmethod # doesn't have self as an argument. only logically connected to this class, otherwise is unrelated to it in any way. 
    def Species_push_from_endoffields_to_detector(conds, z_det): # returns the x,y coords on the detection screen placed at z = z_det
        # conds is a np.array of shape (6,) which represent the x,y,z,ux,uy,uz at end of RK45 integration
        r_at_exit = conds[0:3] # get x,y,z coords at end of RK45 integration 
        us_at_exit = conds[3:6] # get ux, uy, uz at end of RK45 integration

        # find the drifting time drift_time in no E and B fields, E = B = 0. 
        # after how much time does the particle (now moving in free space) hits the detector?
        # z_exit = r_at_exit[2] # exit means exit from the E and B fields
        z_difference = z_det - r_at_exit[2] # z_end is where the detector is placed along z
        drift_time = z_difference / us_at_exit[2] # a float.  us_at_exit[2] is uz at exit, i.e. the velocity along z at exit

        # find the r-coords at the end of the drift time (so when z = z_end = where the detector is placed)
        r_at_end = r_at_exit + (us_at_exit * drift_time)
        return r_at_end[0:2] # x and y coords returned only


class Source:
    """A class which is an interface to a method which gives the initial particles' velocity distribution when they enter the aperture.

    Attributes
    ----------

    _name: str, just an identifier
    _mean: float, the mean (in SI units, m/s) of the Gaussian distribution from which velocities will be drawn. 
    _sigma: float, the sigma (in SI units, m/s) from the Gaussian distribution from which velocities will be drawn.
    _no_of_parts: float, how many draws from the above mentioned distribution will be drawn.

    Methods
    -------
    draw_from_Gaussian():
        Returns a np array shape (_no_of_parts, ) containing floats representing the initial velocities along z of the particles entering the aperture.
    """

    def __init__(self, name, distr, no_of_parts):
        # distr is a np.array of shape (2,): first entry is mean, second entry is sigma
        self._name = name
        mean, sigma = distr 
        self._mean = mean
        self._sigma = sigma
        self._no_of_parts = no_of_parts

    def __str__(self):
        pass
    def __repr__(self):
        pass

    def draw_from_Gaussian(self):
        uzs_at_t0 = np.random.normal(self._mean, self._sigma, self._no_of_parts) # returns shape (self._no_of_parts,)
        return uzs_at_t0 # a numpy array shape (self._no_of_parts, )
