
### Contributor
Name: Farid Alinejad and Simo Hostikka

Institution: Aalto University

Country: Finland

------------------

### Test case

NIST gasification apparatus

------------------

### CFD package
Code: FDS

Version: 6.8.0-0-g886e009-release

------------------

### Resolution

#### Computational domain discretization (flow solver)
Domain: Width = height = length = 0.186 m. The simulated solid material is the size of a single grid cell face and assigned to the center of the domain bottom, rest of the bottom is inert solid boundary. Side and top boundaries are open.

Cell size: 0.0058 m

Cell type: Cubic.

Total cells: 27 (3 in each direction)

Comments: Simulations of NIST gasification apparatus carried out without gaseous phase.

#### Angular space discretization (radiation solver)
Number of solid angles:

Comments: Radiation outside the specimen not considered.

------------------

### Initial conditions
Comments: Ambient temperature.

------------------

### Boundary conditions
Comments: On the exposed side incident heat flux equal to the nominal value from the heater (25 or 50 kW/m2). On the unexposed side, a Kaowool insulation layer of 2.85 cm as in experiments modelled as the boundary condition.

------------------

### Models (include parameters)
Turbulence model (include Sc_t and Pr_t):

Combustion model:

Radiation model:

Radiative fraction: (predicted or prescribed; if prescribed, what value)

Soot model:

Comments: Simulations of NIST gasification apparatus carried out without gaseous phase.

------------------

### Pyrolysis Models (include parameters)
Solver (e.g., GPyro, FDS, ThermaKin; include version): FDS 6.8.0-0-g886e009-release

Radiation absorption model: Effective absorption coefficient.

Material property set: developed by Aalto University; calibration data: University of Lille (TGA for chemical kinetics estimation), Aalto University, DBI and University of Lund (gasification for material properties estimation); calibration method used: Gpyro (chemical kinetics), PROPTI (material properties).


Comments: The accompanying numerical results are obtained using the pyrolysis model developed at Aalto University during MaCFP Phase II.

------------------

### Discretization methods
Time: Explicit Euler

CFL: This and below not applicable as simulations are carried out without gaseous phase.

Advection:

Diffusion:

Pressure-velocity coupling:

------------------

### Computational Cost (hh:mm:ss)
Wall clock time: 36.8 s (25 kW/m2), 4.03 s (50 kW/m2)

Simulation time: 5000 s (25 kW/m2), 600 s (50 kW/m2)

Number of CPUs (OpenMP Processes): 10 (both 25 and 50 kW/m2)

CPU cost (Number of CPUs * Wall clock time / Simulation time / Total cells): 0.00263 (25 kW/m2), 0.00249 (50 kW/m2)

------------------

### Averaging period

------------------

### Special issues/problems

------------------

### Relevant publications

Alinejad, F., Bordbar, H., & Hostikka, S. (2023). On the importance and modeling of in-depth spectral radiation absorption in the pyrolysis of black PMMA. Fire Safety Journal, 135, 103706.
