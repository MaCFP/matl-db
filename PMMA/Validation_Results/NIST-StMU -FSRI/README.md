### Contributor
Name:  Jason Floyd, Isaac Leventon, Morgan Brun

Institution:  FSRI,NIST,St. Mary's University,

Country: USA

------------------

### Test case
Gassification tests: R3-R5 - 50 kW/m2 mas loss
------------------

### CFD package
Code: FDS

Version: 6.8

------------------

### Resolution


### Initial conditions
Comments: Simulations T1-T5 (50 kW/m2) and 25R1-R3 (25 kW/m2) used the experimentally measured temperature at t=0 for the initial condition. All other simulations used 20.9 C.

------------------

### Boundary conditions
Comments:
SOLID_PHASE_ONLY = T
Based on sensitivity analysis performed using https://github.com/MaCFP/matl-db/blob/master/PMMA/Material_Properties/2021/MaCFP_PMMA_NIST.json, simulations used a single, constant flux (i.e., no accounting for time dependence due to shutter or spatial dependence across the sample)
Epoxy mass was treated as PMMA. Output processed to tare initial mass to the reported PMMA sample mass)

------------------

### Pyrolysis Models (include parameters)
Solver: FDS

Radiation absorption model:FDS two-flux model

Material property set:
https://github.com/MaCFP/matl-db/blob/master/PMMA/Material_Properties/2023/MaCFP_PMMA_NIST-StMU.json

Comments:
json file density was used in simulation. Sample thickness was set to preserve the reported sample mass using the json density and the reported sample diameter.
------------------

### Discretization methods
Time: 0.01 s time steps

------------------

### Computational Cost (hh:mm:ss)
Wall clock time:  7 - 10 s for 25 kW/m2, 4-7 s for 50 kW/m2

Simulation time: 500 s for 50 kW/m2, 800 s for 25 kW/m2

Number of CPUs (MPI Processes): 1

CPU cost (Number of CPUs * Wall clock time / Simulation time / Total cells):

------------------

