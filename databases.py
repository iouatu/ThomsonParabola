from scipy.constants import e as e_charge, m_p
XenonA = 131.29
CarbonA = 12.0

## --------------------------------------------
all_possible_names = ['proton'] # list of strings which will be populated
for i in range(55): # 54 is the last
    all_possible_names.append('Xe%d+' % i)
for i in range(7): # 6 is the last
    all_possible_names.append('C%d+' % i)



## -------------------------------------------
charges = dict()
charges['proton'] = e_charge
for i in range(55): # 54 is the last
    charges['Xe%d+' % i] = i * e_charge
for i in range(7):
    charges['C%d+' % i] = i * e_charge



## ------------------------------------------
masses = dict()
masses['proton'] = 1.0 * m_p
contor = 0 # for what???
for element in all_possible_names[1:56]:
    masses[element] = XenonA * m_p #
for element in all_possible_names[56:]:
    masses[element] = CarbonA * m_p #
