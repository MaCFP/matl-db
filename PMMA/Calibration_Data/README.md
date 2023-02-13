## How to interpret and use measurement data in this repository for pyrolysis model calibration and validation
#
### Key factors influencing material response during tests
In this directory, experimental measurements from both mg- and g-scale tests (conducted by 16 unique fire safety science institutions around the world) are available. Every effort was made to remove variability between results due to potential differences in material composition by sharing samples of the same exact PMMA, prepared for mg- and g-scale experiments: that is, all tests were performed on the exact same material, from the same source, and prepared in the same form (excluding minor variations, ~5%, in sample slab thickness, as produced by the manufacturer).

In many cases, data from the same test type under the same nominal test conditions that was provided by different institutions showed qualitative agreement; in others, variations are apparent. Some variations between datasets are simply stochastic (i.e., random, unavoidable noise in repeated tests). However, others may result from systematic causes such as calibration differences in mg-scale experiments or sample holder, insulation type, and/or heater temperature in g-scale experiments. When such measurement data is used as a reference for comparison with the results of numerical simulations, it is the responsibility of users of this data to be aware factors that can can affect this smaterial flammability response. A short summary of these factors is provided below. For further detail, the user of this data is referred to the [Preliminary Summary of Experimental Measurements Document](https://github.com/MaCFP/matl-db/releases/tag/v1.0.0)

#### Milligram-scale experiments
- Heating Rate
- Gaseous Environment
- Crucible Type
- Apparatus Calibration (should be performed for idential test conditions: heating rate, gaseous environment, crucible type)
- Baseline Correction (especially for DSC measurements)
- Initial Sample Mass (and geometry)

#### Gram-scale experiments
- Incident Heat Flux (and uniformity across sample's surface)
- Gaseous Environment (and flow rate, which can affect convective heat transfer at the sample's surface prior to gasification or burning)
- Backing Material (e.g., the presence or absence of an insulating substrate, and its thermal properties)
- Heater Temperature
- Exposed Sample Surface Area
- Sample Holder Characteristics (including the use/non-use of a retainer frame)
- Baseline Correction (especially for HRR measurements)
- Temperature Measurement Instrumentation and Location (e.g., IR camera vs. thermocouple; thermal contact)
#
#
### Outlier Criteria: Identification of clearly incorrect behavior in measurement data
With the help of the experimentalists who performed these experiments and shared their data, significant effort has been made to provide consistent formatting of measurement results and to identify and correct small errors that may have arised either during testing, submission, or compilation and standardization of formating. Despite these efforts, clear outliers can sometimes be identified. Criteria defining these clear outliers are defined below; it is suggested that, for further analysis, users omit data sets that do not meet these criteria.

#### Milligram-scale experiments
For all mg-scale tests, average steady state heating rate must match nominal conditions.
##### Thermogravimetric Analysis (TGA)
In anaerobic conditions, a single reaction peak should be observed at the following temperatures (T_max):
- dT/dt = 5 K/min:	T_max = 625 K +/- 7.5 K
- dT/dt = 10 K/min:	T_max = 640 K +/- 7.5 K
- dT/dt = 20 K/min:	T_max = 650 K +/- 7.5 K

In oxygenated environments (21 vol. % O2) for tests conducted at dT/dt = 10 K/min, two reaction peaks should be observed at the following temperatures (T_max):
- T_max1 = 580 K +/- 7.5 K 
- T_max2 = 605 K +/- 7.5 K 

##### Differential Scanning Calorimetry (DSC)
- At all heating rates, _integral_ heat flow must be positive for all times/temperatures
##### Microscale Combustion Calorimetry (MCC)
- Heat of combustion, Hc=24 kJ/g +/- 1.5 kJ/g

#### Gram-scale experiments
##### Cone Calorimetry
1. Heat Release Rate Measurements (HRR)
Heat of combustion, Hc=23.5 kJ/g +/- 2.5 kJ/g 
2. Back Surface Temperature Measurements 
 Prior to sample burnout (which occurs at approximately 400 s, 250s, and 200 s with incident heat fluxes of 25, 50, and 65 kW/m^2, respectively), temperature, T, should increase monotonically. That is, mean dT/dt > 0 (across any 20 s interval).
##### Gasification Experiments (CAPA, FPA, Controlled Atmosphere Cone )
1. Back Surface Temperature Measurements 
 Prior to sample burnout, back surface temperature should increase monotonically. That is, mean dT/dt > 0 (across any 20 s interval).
2. Front Surface Temperature Measurements 
 Prior to sample burnout, front surface temperature should increase rapidly before reaching a relatively constant value equal to the pyrolysis temperature of this PMMA (~650 K +/- 10K)