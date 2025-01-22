
### Contributor
Name: Kossigan Bernard DEDEY, Serge BOURBIGOT

Institution: UMET (Centrale Lille Institut)

Country: France

------------------

### Test case
[NIST Gasification Apparatus](https://github.com/MaCFP/matl-db/tree/master/PMMA/Validation_Data/NIST_Gasification_Apparatus)
------------------

### CFD package
Code:COMSOL Multiphysics

Version: 6.1

------------------

### Resolution

#### Computational domain discretization (flow solver)
Domain: 3D

Cell size: 0.1867 

Cell type:tetrahedra 

Total cells:3248

Comments: The complete model mesh comprised of 3248 tetrahedra elements (PMMA and Kaowool) and a minimum element size of 0.1867 mm (fine size).

![image](https://github.com/MaCFP/macfp-db/assets/53606808/81f4be21-1656-4136-8adb-ff9b31347820)

#### Angular space discretization (radiation solver)
Number of solid angles:

Comments:

------------------

### Initial conditions
Comments: Can be found the model description in the Abstract file.


------------------

### Boundary conditions
At x0 (surface exposed to the heat flux): the total heat on the exposed surface is a sum of the incident radiative flux (50 kW m-2), the heat lost by radiation and convection (Convective heat transfer coefficient - 10 W m-2 K-1 on the top boundary). Perfect contact is assumed at x1, y1 and y2 interfaces (ie., at polymer and kaowool interface). The outer boundary of the kaowool is considered as thermally insulated.

Comments: Can be found the model description in the Abstract file.

------------------

### Models (include parameters)
Turbulence model (include Sc_t and Pr_t):

Combustion model:

Radiation model:

Radiative fraction: (predicted or prescribed; if prescribed, what value)

Soot model:

Comments: Can be found the model description in the Abstract file.

------------------

### Pyrolysis Models (include parameters)
Solver (e.g., GPyro, FDS, ThermaKin; include version):

Radiation absorption model:

Material property set: [Developed by Literature Review, Refs[1,2]]](https://github.com/dushyant-fire/matl-db/blob/master/PMMA/Material_Properties/2023/UMET-2023.json)

(developed by [institution]; calibration data; calibration method used [e.g., manual iteration, monte carlo sampling, optimization algorithm, PROPTI, Gpyro])


Comments:

------------------

### Discretization methods
Time:

CFL:

Advection:

Diffusion:

Pressure-velocity coupling:

------------------

### Computational Cost (hh:mm:ss)
Wall clock time:

Simulation time: 1 minute, 15 seconds

Number of CPUs (MPI Processes):

CPU cost (Number of CPUs * Wall clock time / Simulation time / Total cells):

![image](https://github.com/MaCFP/macfp-db/assets/53606808/f86b4fc9-998e-4525-8022-f89a2f0b4ff8)
------------------

### Averaging period

------------------

### Special issues/problems

------------------

### Relevant publications
1. Li, J., et al. (2014). "Gasification experiments for pyrolysis model parameterization and validation." International Journal of Heat and Mass Transfer 77: 738-744.
2. Li, J. and S. I. Stoliarov (2013). "Measurement of kinetics and thermodynamics of the thermal degradation for non-charring polymers." Combustion and flame 160(7): 1287-1297.
3. Riccio, A., et al. (2014). "Simulating the response of composite plates to fire." Applied Composite Materials 21: 511-524.

