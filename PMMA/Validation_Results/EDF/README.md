### Contributor
Name: Abdenour Amokrane

Institution: EDF (Electricite de France)

Country:France

------------------

### Test case
 NIST Gasification 0.0058 m qe = 25 kW/m² and 50 kW/m²
------------------

### CFD package
Code: Gpyro

Version: 0.8186

------------------

### Resolution

#### Computational domain discretization (flow solver)
Domain: 1D, thickness 0.0058 m

Cell size: 5 E-5 m

Cell type: cartesian

Total cells: 120

Comments: the domain is 1D


------------------

### Initial conditions: 
Tamb = 300 K
P = Patm
Comments:

------------------

### Boundary conditions
Imposed heat flux on the top surface : qe = 25 or 50 kW/m²
Insulated for the back surface
Comments: The insulation material is not needed for Gpyro. the adiabatic condition could be set directly bu the code.


------------------

### Pyrolysis Models (include parameters)
Solver:GPyro

Radiation absorption model: by default

Material property set: 
[Developed by UMET (UMET_GP, 2021)](https://github.com/dushyant-fire/matl-db/blob/master/PMMA/Material_Properties/2021/MaCFP_PMMA_UMET_GP.json)

Measured by the insitution UMET: 
TGA from 1K/min to 100K/min (UMET)
-DSC (UMET)
-Hot Disk thermal constant analyzer (UMET)
-Heat of reaction measured at 10K/min by different laboratories reported in the guide
-New measurement of heat of reaction by UMET

Some very few additional data from the litterature : density, absorption coefficient and emissivity.

Comments:

------------------

### Computational Cost (hh:mm:ss)
Wall clock time: less than a minute

Simulation time: less than a minute

------------------


