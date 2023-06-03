### Contributor
Name: Dushyant M. Chaudhari, Stanislav I. Stoliarov

Institution: Fire Safety Research Institute (FSRI), University of Maryland College Park (UMD)

Country: U.S.A

------------------

### Test case

[NIST Gasification Apparatus](https://github.com/MaCFP/matl-db/tree/master/PMMA/Validation_Data/NIST_Gasification_Apparatus)

------------------

### CFD package
Code: ThermaKin2Ds

Version: 7

------------------

### Resolution

#### Computational domain discretization (flow solver)
Domain: 

|File Name|Sample Mass (g)|Sample Thickness (mm)|Kaowool Thickness (mm)|Initial Temperature (K)|
|:------------------------------------|:----:|:----:|:----:|:----:|
|UMD-FSRI_Gasification_q50_Temp_Copper|-|3.175|26.055|292|
|UMD-FSRI_Gasification_q50_Temp_Kaowool|-|28.6|0|292|
|UMD-FSRI_Gasification_q25_Temp_R1|28.093|6.26|22.8|295|
|UMD-FSRI_Gasification_q25_Temp_R2|27.75|6.15|22.8|295|
|UMD-FSRI_Gasification_q25_Temp_R3|26.077|5.8|22.8|295|
|UMD-FSRI_Gasification_q50_Mass_R3|26.689|5.74|22.8|292|
|UMD-FSRI_Gasification_q50_Mass_R4|25.643|5.51|22.8|292|
|UMD-FSRI_Gasification_q50_Mass_R5|28.113|6.04|22.8|292|
|UMD-FSRI_Gasification_q50_Temp_R1|24.303|5.35|22.8|292|
|UMD-FSRI_Gasification_q50_Temp_R2|25.136|5.52|22.8|293|
|UMD-FSRI_Gasification_q50_Temp_R3|27.877|6.12|22.8|293|
|UMD-FSRI_Gasification_q50_Temp_R4|27.499|6.1|22.8|294|
|UMD-FSRI_Gasification_q50_Temp_R5|28.187|6.25|22.8|294|

Cell size: 

|File Name|Element size (m)|Total Initial cells (-)|
|:----|:----:|:----:|
|UMD-FSRI_Gasification_q50_Temp_Copper|1.5875E-04|184|
|UMD-FSRI_Gasification_q50_Temp_Kaowool|2.8600E-04|100|
|UMD-FSRI_Gasification_q25_Temp_R1|1.1400E-04|256|
|UMD-FSRI_Gasification_q25_Temp_R2|1.1400E-04|255|
|UMD-FSRI_Gasification_q25_Temp_R3|1.1400E-04|252|
|UMD-FSRI_Gasification_q50_Mass_R3|1.1400E-04|250|
|UMD-FSRI_Gasification_q50_Mass_R4|1.1400E-04|248|
|UMD-FSRI_Gasification_q50_Mass_R5|1.1400E-04|253|
|UMD-FSRI_Gasification_q50_Temp_R1|1.1400E-04|248|
|UMD-FSRI_Gasification_q50_Temp_R2|1.1400E-04|249|
|UMD-FSRI_Gasification_q50_Temp_R3|1.1400E-04|255|
|UMD-FSRI_Gasification_q50_Temp_R4|1.1400E-04|255|
|UMD-FSRI_Gasification_q50_Temp_R5|1.1400E-04|256|

Cell type: 1D

Total cells: See `Total Initial cells (-)` column in the above table. Total number of cells change due to thickness change.

Comments: 
- Sample thicknesses for q50_Mass_R3, q50_Mass_R4, and q50_Mass_R5 simulations were adjusted using the density of black PMMA (1210 kg m<sup>3</sup> used in the pyrolysis model) such that sample mass exactly matched to those reported in the NIST gasification experiments. 
- Epoxy layer and its degradation not considered in any simulations

#### Angular space discretization (radiation solver)
Number of solid angles: N/A

Comments:

------------------

### Initial conditions
Comments: See `Initial Temperature (K)` column in the above table

------------------

### Boundary conditions
Comments: 

- Convective heat transfer coefficient - 8 W m<sup>-2</sup> K<sup>-1</sup> on the top boundary obtained by simulating Kaowool and Copper experiments. The Heat transfer coefficient was varied until the predicted temperatures matched corresponding experimental data.

- Time dependent external heat flux boundary conditions:

	- External radiative heat flux adjusted for contribution from background radiation (~ 0.5 kW m<sup>-2</sup>), defined by the temperature of the gauge cooling water, assumed to be 300 K. 

	- For 25 kW m<sup>-2</sup> external heat flux, linear rise from 23.5 kW m<sup>-2</sup> to 25.5 kW m<sup>-2</sup> in 160 seconds.

	- For 50 kW m<sup>-2</sup> external heat flux, linear rise from 47.5 kW m<sup>-2</sup> to 50.5 kW m<sup>-2</sup> in 150 seconds.

------------------

### Models (include parameters)
Turbulence model (include Sc_t and Pr_t): N/A

Combustion model: N/A

Radiation model: N/A

Radiative fraction: (predicted or prescribed; if prescribed, what value) N/A

Soot model: N/A

Comments:

------------------

### Pyrolysis Models (include parameters)
Solver (e.g., GPyro, FDS, ThermaKin; include version): ThermaKin2Ds, 1D object type

Radiation absorption model: Random absorption algorithm, a Monte-Carlo approach

Material property set: [Developed by UMD](https://github.com/dushyant-fire/matl-db/blob/master/PMMA/Material_Properties/MaCFP_PMMA_UMD.json), Hill-climbing optimization using ThermaKin2Ds [1]

Comments:

------------------

### Discretization methods
Time: 0.01 s time step, Crank–Nicolson scheme for 1D object

CFL: N/A

Advection: N/A

Diffusion: N/A

Pressure-velocity coupling: N/A

------------------

### Computational Cost (hh:mm:ss)
Wall clock time: Based only on initial cells

|Cmp File Name |Wall clock time (s)|Simulation time (s)|CPU|Cost|
|--------|:-------:|:-----:|:---:|:-----:|
|UMD-FSRI_Gasification_q50_Temp_Copper |108.0|100|4|0.0235|
|UMD-FSRI_Gasification_q50_Temp_Kaowool|708.0|1200 |4|0.0236|
|UMD-FSRI_Gasification_q25_Temp_R1 |1104.0 |750|4|0.0230|
|UMD-FSRI_Gasification_q25_Temp_R2 |1108.2 |750|4|0.0232|
|UMD-FSRI_Gasification_q25_Temp_R3 |1078.2 |750|4|0.0228|
|UMD-FSRI_Gasification_q50_Mass_R3 |608.0|450|4|0.0216|
|UMD-FSRI_Gasification_q50_Mass_R4 |602.0|450|4|0.0216|
|UMD-FSRI_Gasification_q50_Mass_R5 |601.8|450|4|0.0211|
|UMD-FSRI_Gasification_q50_Temp_R1 |600.0|450|4|0.0215|
|UMD-FSRI_Gasification_q50_Temp_R2 |601.8|450|4|0.0215|
|UMD-FSRI_Gasification_q50_Temp_R3 |615.6|450|4|0.0215|
|UMD-FSRI_Gasification_q50_Temp_R4 |576.0|450|4|0.0201|
|UMD-FSRI_Gasification_q50_Temp_R5 |565.2|450|4|0.0196|

Simulation time: See table above

Number of CPUs (MPI Processes): See table above

CPU cost (Number of CPUs * Wall clock time / Simulation time / Total cells): See table above

------------------

### Averaging period

------------------

### Special issues/problems

------------------

### Relevant publications
1. Fiola, G. J., Chaudhari, D. M., & Stoliarov, S. I. (2021). Comparison of Pyrolysis Properties of Extruded and Cast Poly(methyl methacrylate). Fire Safety Journal, 120(May 2020), 103083. https://doi.org/10.1016/j.firesaf.2020.103083
