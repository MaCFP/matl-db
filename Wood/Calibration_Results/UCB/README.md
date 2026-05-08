# UCB Calibration Results

This folder holds results of University of Colorado Boulder efforts on modeling the Wood gasification tests.

## Notes on Modeling

* We chose to represent the anaerobic pyrolysis of pine wood via the parallel reaction mechanism of generalized components: cellulose, hemicellulose, and lignin. While this reaction scheme does generally produce a better-fitting model than a single exponential, it does require that we have knowledge of the component mass fractions for our specific wood, as these values can vary widely. While initial species mass fractions can be determined via optimization, doing so while simultaneously estimating their kinetic parameters is not guaranteed to produce physically meaningful results. In order to determine the initial specie compositions prior to estimating reaction parameters, we fit a linear combination of TGA mass loss curves for cellulose, hemicellulose, and lignin at 10K/min [[1]](#1) to the overall mass loss curve of the pine wood. Assuming no moisture, we perform this fit using the Constrained Optimization By Linear Approximation (COBYLA) Method, applying the constraint $Y_C + Y_H + Y_L = 1$.

* As a part of this modeling effort, several different reaction schemes are explored. The first is a single-stage, parallel reaction mechanism whereby individual components are each converted to char through one of three parallel reactions. Here, we track 6 total species, as each reaction produces a different char residue. These individual char species may be lumped together by giving them identical material properties. The second reaction scheme is a multi-stage, parallel reaction mechanism whereby individual components are likewise converted to intermediate solid species, which are then converted to char residue through another set of parallel reactions. This gives a total of 6 reactions and 9 species, a number which may again be reduced by lumping together intermediate solid or char residue species. The final reaction scheme is an attempt at a more generalizable reaction scheme where each component is fit to its own individual reaction scheme, using the TGA mass loss curves for each component provided in [[1]](#1). The best reaction scheme for each component was found through trial and error: cellulose: 2-step serial, hemicellulose: 3-step serial, and lignin: 2-step parallel. These individual component reaction schemes are combined in parallel to form the overall reaction scheme for wood, consisting of 11 species and 8 reactions. Further detail is provided below.

* 0D Modeling and kinetic property estimation was performed using gpyro v0.8200 [[2]](#2). Property estimation was performed using the Shuffled Complex Evolution (SCE) Method [[3]](#3), due to its native parallelization compatibility with gpyro. Parameter values are initially bounded by a reasonable range of physical values from literature- if the optimization converges to a parameter bound, the range is extended and the optimization restarted. This process is repeated until the optimization converges to a solution entirely within the parameter bounds- thus we can be sure that the optimization has explored the relevant parameter space in its entirety. SCE was run using 5-10 complexes, each with 500-1000 individuals per complex, until the population fitness converged (1e-5 over 100 shuffling loops). 

* 1D Modeling was performed with a modified version of the OpenFOAM solver fireFoam called porousFireDyMFoam. This solver includes the ability to solve multiple regions with coupled heat and mass transfer, including reacting gas, reacting porous solid, and non-reacting solid phases. For these simulations, only the reacting porous solid was solved, using a porous biomass pyrolysis model is based on gpyro [[4]](#4). This porous biomass model was shown to produce identical results to gpyro for a tutorial case of 1D anaerobic pyrolysis. While OpenFOAM was chosen for integration with existing code and flexibility in case and boundary condition options, most model parameters are treated identically between the two codes, meaning that for the idealized 1D cases shared here, results should be reproducible in gpyro. Simulation times for a single CPU with a single thread were ~10 s for $60 \textrm{kW/m}^2$ tests (500 s simulation time) and ~20 s for $40 \textrm{kW/m}^2$ tests (1000 s simulation time).

* Property estimation for material properties (1D) was performed by coupling the OpenFOAM solver above with the optimization toolkit Dakota [[5]](#5). For this problem, the Single-Objective Genetic Algorithm (SOGA) was chosen. The initial population contained 200 individuals, and the algorithm was run until the average fitness converged to a relative tolerance of 1e-5 (300-500 generations).

* For 1D property estimation, we compare mass loss rate MLR $(\textrm{g/m}^2\textrm{/s})$, cumulative mass loss CML (g), and back face temperature T (K) to experimental values via an objective function [[4]](#4):
  
$$
f=\frac{\phi_{MLR}}{N_{\Delta t}}\sum\left( \frac{MLR_{exp}}{|MLR_{try} - MLR_{exp}| + \epsilon MLR_{exp}} \right)^\zeta + \frac{\phi_{CML}}{N_{\Delta t}}\sum\left( \frac{CML_{exp}}{|CML_{try} - CML_{exp}| + \epsilon CML_{exp}} \right)^\zeta + \frac{\phi_{T}}{N_{\Delta t}}\sum\left( \frac{T_{exp}}{|T_{try} - T_{exp}| + \epsilon T_{exp}} \right)^\zeta
$$

Here "exp" and "try" quantities represent the experimental and modeled values at each time point. $\phi$ values represent the weighting for each objective. Fitness exponent $\zeta$ is set to 2, while parameter $\epsilon=0.1$ is used to prevent division by zero.

Since the available gasification data was collected using different heating rates and back-face boundary conditions, we run multiple cases with each set of parameters, extract the individual objective values, then combine them into a single objective $\tilde{f} = \sum_{i}f_i$, so as to find the set of parameters that most closely represents all available data.

## Material Properties

### Kinetic Parameters

TGA data is used to fit kinetic parameters $(A,E,n,\nu)$ for an Arrhenius-type reaction [[4]](#4):

$$
\begin{equation}
\dot{\omega}_i = \left( \frac{\rho Y_i}{(\rho Y_i)_{\Sigma}} \right)^n(\rho Y_i) A exp (-\frac{E}{RT}), ~~
(\rho Y_i)_{\Sigma}=(\rho Y_i)|_{t=0} + \int_0^t \dot{\omega}_i(\tau)d\tau
\end{equation}
$$

Note that here the reaction order applies to the normalized specie concentration $(\rho Y_i) / (\rho Y_i)\_{\Sigma}$, where $(\rho Y_i)\_{\Sigma}$ is the total (initial + formed) specie concentration over the current simulation duration.

#### (1) Single-Step Parallel
$$
\begin{cases}
        \textrm{Cellulose} \rightarrow \nu_1~\textrm{char}_1 + (1-\nu_1)~\textrm{gas} \\
        \textrm{Hemicellulose} \rightarrow \nu_2~\textrm{char}_2 + (1-\nu_2)~\textrm{gas} \\
        \textrm{Lignin} \rightarrow \nu_3~\textrm{char}_3 + (1-\nu_3)~\textrm{gas}
    \end{cases} 
$$

#### (2) Multi-Step Parallel
$$
\begin{cases}
        \textrm{Cellulose} \rightarrow \nu_1~\textrm{intermediate solid}_1 + (1-\nu_1)~\textrm{gas} \\
        \textrm{Hemicellulose} \rightarrow \nu_2~\textrm{intermediate solid}_2 + (1-\nu_2)~\textrm{gas} \\
        \textrm{Lignin} \rightarrow \nu_3~\textrm{intermediate solid}_3 + (1-\nu_3)~\textrm{gas}
    \end{cases}
$$

$$
\begin{cases}
        \textrm{Intermediate solid}_1 \rightarrow \nu_4~\textrm{char}_1 + (1-\nu_4)~\textrm{gas} \\
        \textrm{Intermediate solid}_2 \rightarrow \nu_5~\textrm{char}_2 + (1-\nu_5)~\textrm{gas} \\
        \textrm{Intermediate solid}_3 \rightarrow \nu_6~\textrm{char}_3 + (1-\nu_6)~\textrm{gas}
    \end{cases}
$$

#### (3) Component-Wise Parallel

$$
\begin{cases}
        \textrm{Cellulose} \rightarrow \nu_1~\textrm{intermediate solid}_1 + (1-\nu_1)~\textrm{gas} \\
       \textrm{Intermediate solid}_1 \rightarrow \nu_2~\textrm{char}_1 + (1-\nu_2)~\textrm{gas}
    \end{cases}
$$

$$
\begin{cases}
        \textrm{Hemicellulose} \rightarrow \nu_3~\textrm{intermediate solid}_2 + (1-\nu_3)~\textrm{gas} \\
        \textrm{Intermediate solid}_2 \rightarrow \nu_4~\textrm{intermediate solid}_3 + (1-\nu_4)~\textrm{gas} \\
       \textrm{Intermediate solid}_3 \rightarrow \nu_5~\textrm{char}_2 + (1-\nu_5)~\textrm{gas}
    \end{cases} 
$$

$$
 \begin{cases}
        \textrm{Lignin} \rightarrow \nu_6~\textrm{char}_3  + (1-\nu_6)~\textrm{gas} \\
        \textrm{Lignin} \rightarrow \nu_7~\textrm{intermediate solid}_4 + (1-\nu_7)~\textrm{gas} \\
       \textrm{Intermediate solid}_4 \rightarrow \nu_8~\textrm{char}_4 + (1-\nu_8)~\textrm{gas}
    \end{cases} 
$$

Reaction schemes (1) and (2) use experimental TGA data averaged for each heating rate $(\beta=5,10,20,30,40,50~\textrm{K/min})$ across all participating institutions [[6]](#6). Reaction scheme (3) utilizes TGA data from [[1]](#1). 

### Gasification

For each of the estimated reaction schemes, we use the available 1D gasification data to fit the material properties of the wood samples. The material properties that we estimate in this work are the specific heat capacity, thermal conductivity, and emissivity. While we did obtain an initial specie composition for the 0D samples above, we chose to refit them here for comparison, with the constraint $Y_C + Y_H + Y_L = 1$.

Properties are either defined as constant or exponential in T:

$$
C_p(T) = C0\cdot(T/T0)^{n_c}
$$

$$
k(T) = k0\cdot(T/T0)^{n_k}
$$

Thermal conductivity is additionally treated as anisotropic, as results provided by TIFP+UCT [[8]](#8) and TUBS [[9]](#9) show a significant difference in mass loss rates between parallel-grain and perpendicular-grain orientations. Here, we optimize $k_x$ and $k_z$ as separate parameters, selecting the relevant orientation for comparison with each corresponding experimental case. 

Solid wood density is assumed constant, with an initial value of $380~\textrm{kg/m}^3$ [[4]](#4). Solid product densities are calculated via the estimated solid fractions from the kinetic schemes above. 

This modeling effort used 1D gasification data from FSRI ($40,60~\textrm{kW/m}^2$) [[7]](#7), TIFP+UCT ($30,60~\textrm{kW/m}^2$) [[8]](#8), and TUBS ($20~\textrm{kW/m}^2$) [[9]](#9).

## Folder Structure and Naming Conventions

Complete Material Property Sets are located in the .json files in the Material Property Folder. Files follow the naming convention "Wood_UCB-{i}.json", where "i" corresponds to the different reaction schemes presented above.

Calbration results using these material properties for cases of 0D and 1D anaerobic pyrolysis are available in Calibration Results/UCB. Files follow similar naming structure of "UCB-\{i\}_Wood_GASIFICATION....csv" for 1D cases and "UCB-\{i\}_Wood_TGA(...).csv" for 0D cases.  

Property sets are calculated using both constant (CONST) and temperature-dependent (TDEP) material properties- for each heating rate/radiative heat flux, results are provided for both versions. In addition, 1D results are provided for both parallel-grain (PARALLEL) and perpendicular-grain orientations (PERPENDICULAR). Tags are included in filenames to differentiate methods. 


## References
<a id="1">[1]</a> 
Hasburgh, L.E. 2020. 
Chemical and Mechanical Characterization of Pyrolysis in Wood. 
Madison, WI: University of Wisconsin-Madison. Ph.D. dissertation.

<a id="2">[2]</a> 
Gpyro:
Generalized pyrolysis model for combustible solids.
Available online at: https://github.com/lautenberger/gpyro

<a id="3">[3]</a> 
V. K. Gupta Q. Y. Duan and S. Sorooshian. 
Shuffled complex evolution approach for effective and efficient global minimization. 
Journal of Optimization Theory and Applications, 76:501–521, 1993.

<a id="4">[4]</a> 
Lautenberger, Chris and Fernandez-Pello, Carlos. 
A model for the oxidative pyrolysis of wood. 
Combustion and Flame, 156(8):1503–1513, August 2009.

<a id="5">[5]</a> 
Dakota:
A Multilevel Parallel Object-Oriented Framework for Design Optimization,
Parameter Estimation, Uncertainty Quantification, and Sensitivity Analysis.
Available online at: https://github.com/snl-dakota/dakota

<a id="6">[6]</a> 
Measurement and Computation of Fire Phenomena (MaCFP) Condensed Phase Material Database.
Available online at: https://github.com/MaCFP/matl-db

<a id="7">[7]</a> 
Joshua D. Swann, Yan Ding, Mark B. McKinnon, Stanislav I. Stoliarov,
Controlled atmosphere pyrolysis apparatus II (CAPA II): A new tool for analysis of pyrolysis of charring and intumescent polymers,
Fire Safety Journal, Volume 91, 2017.
https://doi.org/10.1016/j.firesaf.2017.03.038.

<a id="8">[8]</a> 
Technical Institute of Fire Protection, Prague (TIFP) and University of Chemistry and Technology, Prague (UCT): Contribution to the 4th Workshop of the Measurement & Computation of Fire Phenomena (MaCFP) Working Group of the International Association for Fire Safety Science: Experimental Data.

<a id="9">[9]</a> 
Armbrust, Felix ; Zehfuß, Jochen ; Riese, Olaf: Contribution to the 4th Workshop of the Measurement & Computation of Fire Phenomena (MaCFP) Working Group of the International Association for Fire Safety Science: Experimental Data.
https://doi.org/10.24355/dbbs.084-202604271326-0.
