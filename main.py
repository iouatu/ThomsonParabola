# import sys
# print(sys.path)
import Species, Geometry, utility_fns, databases, RKint # why not from TS_mypkg import ... ? <--- gives ERROR
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.pyplot import cm

all_possible_names = databases.all_possible_names
masses = databases.masses
charges = databases.charges
"""
# geometry explanation: initial velocity of particles along z axis.
# E and B fields parallel one to each other and oriented along positive y direction.
# Both E and B fields stop (instantly go to 0 value) at same z location, denoted by l_B below.
# Both E and B fields are constant and not influenced in any way by the passing, moving, particles.
# The code asks for geometry input from the user.

# Particles' input to this code are accepted per ''chunk'' of particles.
# A chunk of particles is a group of some particles of same species, which will be input to the aperture in a way dependent on an option chosen by the user.
# Each chunk will have this option selected for it. if you input 3 chunks, 3 (possibly different) options will have to be chosen.

# Option 1: aperture gets #_particles of the same species. particles have only u_z != 0 and their u_z's are drawn from a Gaussian with mean inputted by you and sigma = mean/10. particles have initial x,y = 0 (and z = 0 ofc)
# Option 2: aperture gets #_particles of the same species. particles have only u_z != 0 and all their u_z's are equal between them and inputted by you. particles have initial coordinate x not necessarily equal to 0 (but z = 0 ofc).
# Option 2 is suited to see the dispersion on screen due to the non-pointlike aperture (with a finite radius, Radius R != 0.0).
# Option 2 allows to interacetively select an aperture which is non-pointlike only along X or only along Y, or along both directions (thus 3 different possibilities if option 2 is chosen)
"""

def dictated_by_1(no_of_parts, input_MeVs):
    """  Method to return initial conditions for a chunk of particles inputted using option 1.

    Returns 2 things:
    1) Returns a list of len 1 containing a np.array of size (3,). Array contains the x,y,z initial coordinates of the particles from the chunk.
    2) Returns a np.array of shape (no_of_parts, ) containing the initial velocities along z axis of the particles from the chunk.
    The velocities are obtained by drawing from a Gaussian distribution with mean equal to the input argument input_MeVs of this function and sigma = mean/10.

    Parameters
    ----------
    no_of_parts : int (how many particles of a given species to deal with)
    input_MeVs : float (mean KEnergy, in MeVs)

    Returns
    -------
    list of len 1, np.array shape (no_of_parts, )
    """

    mean_uz_init = utility_fns.from_KEineV_to_uzinit(input_MeVs * (10**6))
    initial_uzs = Species.Source('Source_for_1', np.array([mean_uz_init, mean_uz_init/10.0]), no_of_parts).draw_from_Gaussian() # a numpy array shape (no_of_parts, )
    initial_coords = np.array([0.0, 0.0, 0.0]) # x, y, z
    return [initial_coords], initial_uzs

def dictated_by_2(no_of_parts, input_MeVs, Xtrue, Ytrue): # dispersion due to aperture for fixed incident MeV energy
    """  Method to return initial conditions for a chunk of particles inputted using option 2.

    Returns 2 things:
    1) Returns a list of len 2 containing 2 np.arrays of size (no_of_parts, ). Array contains the x (and y respectively in the 2nd array), initial coordinates of the particles from the chunk.
    2) Returns a np.array of shape (no_of_parts, ) containing the initial velocities along z axis of the particles from the chunk.
    Initial velocities returned array is filled with the exact same float.

    Parameters
    ----------
    no_of_parts : int (how many particles of a given species to deal with)
    input_MeVs : float (initial KEnergy, in MeV)

    Returns
    -------
    list of len 2, np.array shape (no_of_parts, )
    """

    want_aperture_notpointlike_along_x = Xtrue
    want_aperture_notpointlike_along_y = Ytrue

    uz_init = utility_fns.from_KEineV_to_uzinit(input_MeVs * (10**6))
    # print("inside dictated_by_2 uz_init is:")
    # print(uz_init)
    initial_uzs = np.empty( (no_of_parts,) ) # shape (no_of_parts, ), same float in all the no_of_parts locations of the array
    initial_uzs.fill(uz_init)
    # print("inside dictated_by_2 initial_uzs is: ")
    # print(initial_uzs)
    if (want_aperture_notpointlike_along_x == True and want_aperture_notpointlike_along_y == False):
        initial_xs = np.random.uniform(0, 1, no_of_parts) * 0.01 # aperture has radius 0.005 m = 0.5 cm. top x = 0. , bottom x = 0.01 m, center x = 0.005m
        initial_ys = np.zeros(no_of_parts)
    elif (want_aperture_notpointlike_along_x == False and want_aperture_notpointlike_along_y == True):
        initial_ys = np.random.uniform(0, 1, no_of_parts) * 0.01 # aperture has radius 0.005 m = 0.5 cm. top y = 0. , bottom y = 0.01 m, center y = 0.005m
        initial_xs = np.zeros(no_of_parts)
    elif (want_aperture_notpointlike_along_x == True and want_aperture_notpointlike_along_y == True):
        initial_xs = np.random.uniform(0, 1, no_of_parts) * 0.01 # aperture has radius 0.005 m = 0.5 cm. top coord = 0. , bottom coord = 0.01 m, center coord = 0.005m
        initial_ys = np.random.uniform(0, 1, no_of_parts) * 0.01 
    
    
    return [initial_xs, initial_ys] , initial_uzs
    #initial_coords_container = []
    #initial_coords_container.append([0.0, 0.0, initial_xs[i]] for i in range(no_of_parts))

def get_particles_init_conds(no_of_parts, input_MeV, what_you_want_to_do, Xtrue, Ytrue):
    """ This function is used to return initial x,y,z coordinates of the particles and initial velocities along z-axis of the particles from a given chunk.
    
    Given how many particles of a given species you simulate, their initial KEnergy (mean or fixed, depending on option choice), the option choice (and if option is 2, aperture type)
    it returns the particles x,y,z initial coordinates and their initial velocity along z-axis.

    If option is 1, it considers a pointlike aperture and x = y = z = 0.0 (exactly) and velocities are drawn from a Gaussian distribution with mean
    equal to the input parameter input_MeV and sigma = mean / 10.
    If option is 2, it considers a non-pointlike aperture along either x and OR y 
    (of radius R = 0.005 m when both x-y behaviour is taken into account, of length = 0.005 m when only x or y behaviour is taken into account)
    and velocities along z-axis are all the same and equal to conversion(input_MeV) m/s.

    Parameters
    ----------
    no_of_parts : int ()
    input_MeV : float ()
    what_you_want_to_do : int (either 1 or 2 at the moment)
    Xtrue : bool ()
    Ytrue : bool ()

    Returns
    -------
    list of len 1 or 2, np.array shape (no_of_parts, )
    """

    if (what_you_want_to_do == 1): # varying incident MeV energy, same species, aperture is pointlike (xinit = yinit = zinit = 0.0)
        initial_coords, initial_uzs = dictated_by_1(no_of_parts, input_MeV) # initial_coords is a list of 3 floats
        return initial_coords, initial_uzs # initial coords is a list of len 1. initial_uzs is np.array of shape (no_of_parts, )
    else:
        if (what_you_want_to_do == 2): # fixed input energy, want to see the spread on the detector screen 
            initial_coords, initial_uzs = dictated_by_2(no_of_parts, input_MeV, Xtrue, Ytrue)
            return initial_coords, initial_uzs # initial coords is a list of len 2. initial_uzs is np.array of shape (no_of_parts, )
        else:
            print("say again what you want to do?")


def create_Species_Objects(name, mass, charge, r, velo, no_of_particles, dict_to_put_in): # creates 100 protons , say
    """ This function creates no_of_particles objects of Species type, based on the species characteristics and initial conditions.

    Based on the name of the species (proton, Carbon0+, Carbon1+..., Carbon6+, Xe0+, ... Xe54+) and its mass and charge,
    together with initial x,y,z coordinates and initial ux,uy,uz velocities, creates no_of_particles objects of Species type and
    stores them in a dictionary dict_to_put_in.
    Object number 1 is stored as the value for the key = 'particle_1', object number 2 is stored at the value for the key = 'particle_2' ...
    up until the counter reaches no_of_particles and the last object is stored for the key = 'particle_%d' % (no_of_particles).
    Returns the dictionary created with these objects as its values for its keys.

    Parameters
    ----------
    name : str (name of the species you want to create no_of_particles particles of its type)
    mass : float (mass in SI of the species named name)
    charge : float (charge in SI of the species named name)
    r : list (len 1 or 2, depending on the code-option chosen (len 1 for option 1)) containing the initial coordinates of the particles you want to initiate.
    if len 1, r[0] is a np.array shape (3, ) containing the x,y,z initial coordinates of the particles
    if len 2, r[0][i] is the initial x-coordinate in SI of the particle i (i runs from 0 to no_of_particles-1), r[1][i] is the initial y-coordinate in SI of the smae particle
    velo : list len no_of_particles (contains the initial z-velocities in SI of the particles you want to be initiated)
    no_of_particles : int (how many particles you want to be initiated)
    dict_to_put_in : dictionary (returned 'container' which holds the initiated particles, i.e. the initiated Species objects)

    Returns
    -------
    dict_to_put_in : dictionary containing as its keys' values the Species objects created by this function using the input parameters.
    """

    # nonlocal Species_Objs_dict
    for i in range(no_of_particles): # for each particle out of this chunk of 100 (say) particles
        if (len(r) == 1): # it's option 1 then
            coords = r[0] # np array shape (3,)
        else:
            coords = np.empty( (3,) )
            if (len(r) == 2): # it's option 2 then
                coords[0] = r[0][i] # the x for this particle
                coords[1] = r[1][i] # the y for this particle
                coords[2] = 0.0 # the z for this particle
            else:
                print("Error at creating Species objects!")
                # raise ValueError('A very specific bad thing happened.')

        dict_to_put_in['particle_%d' %(i+1)] = Species.Species("{}_{}".format(name, (i+1)), mass, charge, coords, [0.0, 0.0, velo[i]])
    return dict_to_put_in

def main():
    E = float(input("Please enter the fields and geometry details. E = ? [V/m] \n"))
    B = float(input("B = ? [T] \n"))
    l_E = float(input("l_E = ? [m] \n"))
    l_B = l_E
    D_E = float(input("D_E = ? [m] \n"))
    D_B = D_E
    z_det = float(input("Distance at which the screen is placed from the source (distance measured across z): ? [m] \n"))
    y_electrode_bottom = float(input("Distance at which the bottom electrode is placed from the origin (distance measured along +y): ? [m] \n"))

    Efieldobj, Bfieldobj, detector_obj, electrode_bottom_obj = Geometry.create_Geometry_Objects(E, l_E, D_E, B, l_B, D_B, z_det, y_electrode_bottom)
    l_B = Bfieldobj._l #
    E = Efieldobj._strength
    B = Bfieldobj._strength
    # did you write the create_Geometry_Objects() function? yes, create_Geometry_Objects() is in Geometry.py
    z_det = detector_obj._z_det
    y_bottom_elec = electrode_bottom_obj._y_electrode
    yscal_maxvalues = np.array([10.0, 0.01, 0.2]) # max values for x, y, z of a particle during it's flight through the E and B fields

    counter_chunks_of_input = 0
    names, no_of_particles, input_MeV, whats, apsX, apsY = [], [], [], [], [], []
    while (True):
        response = input("Do you want to create another chunk of particles? [Y/N] \n")
        if (response == "Y"):
            counter_chunks_of_input += 1
            name = input("Species Name? can only choose from (careful not to introduce typos!): [proton; C0+...6+; Xe0+...54+] \n")
            if name in all_possible_names:
                print("You introduced a correct name of Species.")
                names.append(name)
            else:
                print("Error: You introduced a wrong name of Species. ABORT")
                break
            number_of_particles = int(input("How many {} ? \n".format(name)))
            no_of_particles.append(number_of_particles)
            input_energy = float(input("Initial KEnergy in MeV ? \n"))
            input_MeV.append(input_energy)
            what = float(input("What do you want to do with this chunk of particles? [1/2] \n"))
            whats.append(what)
            if (what == 2):
                aperture_nonpoint_alongX = input("Do you want the aperture to be NON-pointlike along X? [Y/N] \n")
                condX = True
                while (condX):
                    if aperture_nonpoint_alongX == 'Y':
                        aperture_nonpoint_alongX = True
                        apsX.append(aperture_nonpoint_alongX)
                        condX = False
                    elif aperture_nonpoint_alongX == 'N':
                        aperture_nonpoint_alongX = False
                        apsX.append(aperture_nonpoint_alongX)
                        condX = False
                    else:
                        print("wrong answer for X-direction aperture type")
                        aperture_nonpoint_alongX = input("Do you want the aperture to be NON-pointlike along X? [Y/N] \n")

                aperture_nonpoint_alongY = input("Do you want the aperture to be NON-pointlike along Y? [Y/N] \n")
                condY = True
                while(condY):
                    if aperture_nonpoint_alongY == 'Y':
                        aperture_nonpoint_alongY = True
                        apsY.append(aperture_nonpoint_alongY)
                        condY = False
                    elif aperture_nonpoint_alongY == 'N':
                        aperture_nonpoint_alongY = False
                        apsY.append(aperture_nonpoint_alongY)
                        condY = False
                    else:
                        print("wrong answer for Y-direction aperture type")
                        aperture_nonpoint_alongY = input("Do you want the aperture to be NON-pointlike along Y? [Y/N] \n")
            else: # what == 1
                apsX.append(False)
                apsY.append(False) 
        else:
            if(response == "N"): # user doesn't want any other chunks of particles
                break # go out of the while-loop and continue executing instructions appearing after the while-loop.
            else:
                print("invalid response! try again!")
                continue

    list_of_dicts_containing_Species_Objs = []
    for j in range(counter_chunks_of_input): # for each chunk of 1000 (say) particles
        initial_coords, initial_uzs  = get_particles_init_conds(no_of_particles[j], input_MeV[j], whats[j], apsX[j], apsY[j]) # both arguments are coming from user-input
        # initial_coords has either len = 1 or len = 2, depending on which option you selected.
        # initial_uzs is a np.array shape (no_of_particles, ). it can be populated with same float, OR with floats extracted from a Gaussian. This depends on which option you choose.
        Species_Objs_dict = dict() # for this current chunk of 1000 (say) particles
        print(initial_uzs)
        Species_Objs_dict = create_Species_Objects(names[j], masses[names[j]], charges[names[j]], initial_coords, initial_uzs, no_of_particles[j], Species_Objs_dict)
        list_of_dicts_containing_Species_Objs.append(Species_Objs_dict)

    final_coords_at_detectorscreen = []
    for k in range(len(list_of_dicts_containing_Species_Objs)): # for each chunk of particles
        name_of_particles_from_chunk = list_of_dicts_containing_Species_Objs[k]['particle_1']._name
        results = [] # for this chunk of particles
        coords_at_detector_forthischunk_all = [] # for this chunk of particles
        for j in range(len(list_of_dicts_containing_Species_Objs[k].keys())): # for each particle out of this chunk
        # push each particle
            parti_obj = list_of_dicts_containing_Species_Objs[k]['particle_%d'%(j+1)]
            exited_B, hit_E, results_for_this_part = RKint.RK45integrator(parti_obj.x, parti_obj.y, parti_obj.z, parti_obj.ux, parti_obj.uy, parti_obj.uz, yscal_maxvalues, l_B, y_bottom_elec, parti_obj._qonm, E, B )
            if (exited_B == 1 and hit_E == 0 ):
                results.append( results_for_this_part )   # results is appended with conditions (x,y,z,ux,uy,uz) from end of RK45 integration (end of E/B fields)
                coords_at_detector = Species.Species.Species_push_from_endoffields_to_detector( results[-1], z_det ) # use the values just appended to results list
            elif (exited_B == 0 or hit_E == 1):
                print("either it didn't exit the B-field region or it hit the bottom electrode")
                if(hit_E == 1):
                    print("it hit the electrode!")
                if(exited_B == 0 and hit_E == 1):
                    print("it hit the electode and it didn't exit the B-field!")
                continue # go to next j, i.e. next iteration of this for-loop, i.e. to the next particle of this chunk of particles. don't push particle to screen anymore, it's stuck in the E/B fields
            coords_at_detector_forthischunk_all.append(coords_at_detector) # coords_at_detector is a numpy array of shape (2,)
        coords_at_detector_forthischunk_all = np.array(coords_at_detector_forthischunk_all) # will be shape (no_of_particles-bad_particles, 2), where no_of_particles is for this particular chunk of particles and bad_particles is again for this particular chunk (the ones which hit the bottom electrode or did not exit B-field)
        # print(coords_at_detector_forthischunk_all.shape)
        final_coords_at_detectorscreen.append( {name_of_particles_from_chunk : coords_at_detector_forthischunk_all} )
 
    # plotting:
    colors = iter(cm.rainbow(np.linspace(0,1, len(final_coords_at_detectorscreen)))) # if you have many chunks of particles (many species), this helps select 1 DIFFERENT color to represent each chunk. 

    plt.figure()
    for j in range(len(final_coords_at_detectorscreen)): # for each chunk of particles
        c = next(colors)
        c = np.reshape(c, (1, c.shape[0]) )
        for key in final_coords_at_detectorscreen[j]: # this for-loop will only make 1 iteration as the dictionary final_coords_at_detectorscreen[j] has 1 key only
            value_from_that_key = final_coords_at_detectorscreen[j][key]
            plt.scatter(value_from_that_key[:, 0], value_from_that_key[:, 1] , s=0.2, label=key, c=c) # key is a str
    plt.title("Detector screen picture showing the captured ions.")
    plt.xlabel("deflection along x axis [meters]")
    plt.ylabel("deflection along y axis [meters]")
    plt.legend()
    plt.savefig("detector_screen.pdf", bbox_inches='tight')

if __name__ == '__main__':
    main()