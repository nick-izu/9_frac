from pydfnworks import *

DFN = create_dfn()

##dfnGen
DFN.make_working_directory()
DFN.check_input()
DFN.create_network()
DFN.mesh_network(visual_mode=False)

porosity = 1.0
tortuosity= 1.0

#Layer = 1
variable = "transmissivity"
function = "correlated"
params = {"alpha":2.2*10**-9, "beta":0.8}
b1,perm1,T1 = DFN.generate_hydraulic_values(variable,function,params,family_id=1)

function = "correlated"
params = {"alpha":3.5*10**-9, "beta":0.9}
b1,perm2,T2 = DFN.generate_hydraulic_values(variable,function,params,family_id=2)

# Then we combine them.
T = T1 + T2 + T3  
b = b1 + b2 + b3 
perm = perm1 + perm2 + perm3 

# Entires 0-3, should be zero here. 
print(b[0:3])

# JDH- now assigne each of those values for aperture
b[0] = 1*10**-3 
b[1] = 1*10**-3 
b[2] = 1*10**-3
b[3] = 1*10**-3 


# convert perm using the cubic law
perm[0] = b[0]**2/12
perm[1] = b[1]**2/12
perm[2] = b[2]**2/12
perm[3] = b[3]**2/12



# determine values of Transmissivity for determinsitc fractures
mu = 8.9e-4  #dynamic viscosity of water at 20 degrees C, Pa*s
g = 9.8  #gravity acceleration
rho = 1000  # water density

T[0] = (b[0]**3 * rho * g) / (12 * mu)
T[1] = (b[1]**3 * rho * g) / (12 * mu)
T[2] = (b[2]**3 * rho * g) / (12 * mu)
T[3] = (b[3]**3 * rho * g) / (12 * mu)

DFN.dump_hydraulic_values(b,perm,T)

# Add transmissivity values to the mesh for visualization
DFN.add_variable_to_mesh("trans,", "transmissivity.dat", "full_mesh.inp")

## JDH I added an exit here for you to look at the files before you run the simulation.
#exit()

#dfnFlow
DFN.dfn_flow()


#dfntrans
DFN.dfn_trans()
