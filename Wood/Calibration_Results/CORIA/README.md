### Contributor
Name: Coppalle Alexis
Institution: CORIA INSA Rouen
Country: France

------------------ Calibration of the thermal degradation of pine wood

with experimental dataset  ‘Test case : UMET_Wood_TGA_N2_10K_R3’

Optimisation sofware : DAKOTA, Version: 18
Optimisation algorithm : NL2SOL
(Dennis J.E., Gay M., ACM Transactions on Mathematical Software (ACM), Algorithm 573: NL2SOL—An Adaptive Nonlinear Least-Squares, 1981)

kinetic mechanism of wood decomposition
- Dry wood
-Three reactions in parallel , corresponding of the three pseudo-components hemicellulose, cellulose and lignin.
-For each reaction (i=1 hemicellulose, i=2 cellulose, i=3 lignin)
	component i===> ni char + (1-ni) gaz
ni stoechiometric coefficient od reaction

-Proportions, in %weight in virgin wood,  for hemicellulose, cellulose and lignin
(Márquez‑Montesino, Reaction Kinetics, Mechanisms and Catalysis Reaction Kinetics, Mechanisms and Catalysis (2021) 132:1057–1074, https://doi.org/10.1007/s11144-021-01954-5)
P1=0.163
P2=0.544
P3=0.293

-With the nomenclature of eq. 1 of the document ‘Guidelines_for_Particpation_MaCFP-4.pdf’




i=3, j=1
ns,i,j =1 for i=1-3 (reaction order 1)
nt,i,j = 0 (no explicit temperature dependence)

===> Application of the NL2SOL algorithm
For each progress variable  ai  of the 3 decomposition reactions
		dai dt = Ai,1 (1- ai ) exp(- Ei / Rts)
and
		d(m/m0)cal/dt = S Pi (1- ni )  dai dt

with m the total mass of the solid, and m0 the initial value

The fitness function F is calculated by the following sommation over time (0-1500s)

		F=   Somme [(m/m0)cal - (m/m0)exp]2

### Results E (J/mole), A (1/s), n (-)
E1=9.3268E+04	A1= 5.3243e6	n1= 0.281
E2= 1.004E+05	A2= 1.3981E6	n2= 0.001
E3= 2.768E+04	A3= 1.2942E-1	n3=0.164

------------------ material properties of pine wood

-with experimental dataset ‘TIFP+UCT_Wood_Gasification_30kW_hor_parallel_R1’

-Simulation of the degradation and pyrolysis under N2: PATOx
(J. Lachaud et al: A generic local thermal equilibrium model for porous reactive materials
submitted to high temperatures, International Journal of Heat and Mass Transfer 108 (2017) 1406–1417)

- radiation exhnage at the top
- gradient(T)=0 at the bottom
- no convection at the top and bottom

see attached picture: 1Dcalculation-geometrie.png




Optimisation sofware: DAKOTA, Version: 18
Optimisation algorithm: NL2SOL
(Dennis J.E., Gay M., ACM Transactions on Mathematical Software (ACM), Algorithm 573: NL2SOL—An Adaptive Nonlinear Least-Squares, 1981)

The fitness function F is calculated by the following sommation over time (0-1500s)

		F=   S [(m/m0)cal – (m/m0)exp]2

with m the total mass of the solid, and m0 the initial value

kinetic mechanism of wood decomposition
The one obtained by optimsation on ATG dataset.
- Dry wood
-Three reactions in parallel , corresponding of the three pseudo-components hemicellulose, cellulose and lignin.

Optimised parameters : assumed to be constant
heat capacity (K/kg/K): virgin-wood (cpv), char (cpc)
thermal conductivity (W/m/K) : virgin-wood (kv), char (kc)
convective coefficient at the top (w/m²) : hTop

known parameters  for wood: from litterature
emissivity : 0.75 for virgin wood, 0.9 for char
absorptivity : 0.9 for virgin wood, 0.9 for char
Rq : the emissivity and absorptivity of virgin wood have a low influence on the 1D calculation results under 30kw/m2

known parameters  for isolant: from litterature
heat capacity (K/kg/K): 840
thermal conductivity (W/m/K) : 0,05
emissivity: 0.9
absorptivity: 0.9
convective coefficient at the bottom  (w/m²): hbottom= 10kw/m2
=======
-kinetic mechanism of wood decomposition
The one obtained by the above optimsation on ATG dataset.
- Dry wood
-Three reactions in parallel , corresponding of the three pseudo-components hemicellulose, cellulose and lignin.

parameters : assumed to be constant, extracted from litterature
(mainly: DINH Duy Cuong, PhD, ENSMA (France), 2024)
heat capacity (J/kg/K):
   virgin-wood: 2250.
   char:        1250. 
thermal conductivity (W/m/K) :
   virgin-wood: 0.35
   char :       0.08
emissivity :
   virgine wood: 0.75
    char:    0.75
absorptivity :
   virgin wood: 0.9
   char:     0.9

### Results for the optimased parameters

0.4421	5795,0916789687	0,75	0,9	0,167728677728907	6537,9920207607	0,75	0,9	10,582566861517

heat capacity (K/kg/K):
5795.1 for virgin-wood (cpv), 6538.0 for char (cpc)
thermal conductivity (W/m/K) :
0.4421 for virgin-wood (kv), 0.1677 char (kc)
convective coefficient at the top (w/m²) :
10.58 for hTop
