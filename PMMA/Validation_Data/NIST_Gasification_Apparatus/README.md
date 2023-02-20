# NIST Gasification Apparatus
## Disclaimers

The test description and measurement data presented here is made available as preliminary results, for the purposes of pyrolysis model validation by the MaCFP Working Group. This summary has been analyzed by subject matter experts within the research team and is believed to be scientifically sound and consistent with the integrity expected of NIST research. A NIST Technical Note [1], currently in preparation, will be published shortly along with final experimental results and analysis.

#### This dataset can be cited as:
Leventon, I.T., De Lannoye, K.(2023), Experimental Measurements for Pyrolysis Model Validation - Anaerobic Gasification of PMMA Under External Thermal Radiation, National Institute of Standards and Technology, https://doi.org/10.18434/mds2-2940 (Accessed [PROVIDE DATE])

Note: The identification of any commercial product or trade name does not imply endorsement or recommendation by NIST (or any other contributing institution).

## Test Overview

A set of  16 anaerobic gasification experiments was conducted on the poly(methyl methacrylate), PMMA, that was made available to participants in the MaCFP-2 Workshop [2]. In each test, samples (i.e., PMMA discs of approximate dimensions: 7 cm diameter, 5.8 mm thickness) were exposed to radiant heating (nominally 25 kW m-2 or 50 kW m-2 across their top surface) in an anaerobic environment. Samples were insulated at their back surface and continuously heated until complete decomposition was observed. Test boundary conditions (e.g., time- and spatially-resolved measurements of incident radiant heat flux; chamber wall temperatures) were carefully characterized, as described below.

During experiments, measurements were acquired and recorded using National Instruments (NI) data acquisition (DAQ) modules and using a custom program called MIDAS (Modular In-situ Data Acquisition System), which was developed in LabVIEW. Mean values from each channel were recorded at 1 Hz. Ultimately, the uncertainties from the DAQ system were orders of magnitude lower than those of the measurement devices and/or systems used in these experiments. 

Measurement data obtained in this test series includes:
1. Time-resolved measurements of PMMA sample mass [g];
2. Time-resolved measurements of PMMA back surface temperature [K];
3. Photographs and video of PMMMA decomposition behavior;
4. Time-resolved measurements of temperature rise [K] of inert materials (Copper, Kaowool PM insulation board);


## The NIST Gasification Apparatus
### Description
The NIST Gasification Apparatus was originally designed and built in the late 1990s to expose solid or liquid samples to a uniform heat flux in a non-oxidizing or partially oxidizing atmosphere [3]. Between Summer 2021 and Summer 2022, this instrument was refurbished (multiple system components were upgraded or replaced), recalibrated, and brought back online to enable the study of MaCFP-PMMA gasification in a well-characterized anaerobic environment. 

As seen in Figure 1, the NIST Gasification Apparatus is similar to a cone calorimeter; however, radiant exposure of samples takes place in a sealed, water-cooled, cylindrical chamber (1.70 m tall, 0.61 m inner diameter) that is continuously purged with nitrogen. The cone heater (30 cm diameter) is approximately three times the size of a typical cone calorimeter heater, which enables a more uniform heat flux distribution across the sample’s surface. 

The gasification apparatus is equipped with a retractable, water-cooled shutter that is inserted directly beneath the heater while the sample is loaded into the chamber and the system is purged of oxygen. This shutter is removed at the start of each test and can be inserted or removed as needed without affecting heater operations or the flow of nitrogen or cooling water to the system. 

A steady supply of nitrogen (20 SCFM; 566 L/min) is introduced into the chamber through an annulus at is base that contains a layer of glass beads (this design ensures flow uniformity). The temperature of this nitrogen supply (at the inlet of the chamber) is continuously recorded throughout the duration of tests; chamber wall temperature (at two locations) and average heater temperature are continuously recorded as well.

The base of the chamber is connected to a hydraulic lifting mechanism that allows it to be raised (thus sealing the chamber) or lowered at the start or completion of each test. A Sartorius WZA8202-N load cell (protected by its own water-cooled plate) rests atop this moveable platform (i.e., the chamber base). An elevated support structure connects at its base to the load cell weighing platform; at the top of this sample stand rests a circular platform (7.5 cm diameter, 6.35 mm thick aluminum disc) that is used to hold prepared samples (i.e., PMMA discs resting on layers of Kaowool PM Insulation) at the correct height for testing. A terminal strip at the base of the chamber, near the load cell, provides connections for up to five thermocouples (for sample temperature measurements). Sample temperature and mass loss rate measurements are obtained in separate experiments. 

<img src="https://github.com/MaCFP/matl-db/blob/master/PMMA/Validation_Data/NIST_Gasification_Apparatus/Gasification_Apparatus_Schematic_w-sample.png" width="450">
Figure 1. Schematic of the NIST gasification apparatus. The insert at the bottom right of this figure highlights sample / insulation assembly.

### System Calibration (i.e., Measured Boundary Conditions)
Chamber wall and gas temperature was continously measured throughout the duration of experiments. After an initial rise (from 9C to between 14C to 18C) when the heater shutter was removed, measured temperatures at each location maintained steady values throuhgout the duration of experiments.
Chamber Wall Temperature: 14 C to 18 C (test/location/day dependent)
Chamber Gas Tempeature (at sample height): 16C to 18C
Heater Set Point Temperature: 807 C to 808 C

Incident heat flux from the cone heater was measured (using a water-cooled Gardon-type heat flux gauge) at 21 locations at a height corresponding to the original height of the top of the sample's surface. Immediately prior to this heat flux mapping excercise, the gasification apparatus heat flux gauge was calibrated against a secondary standard gauge that was calibrated by NIST Radiation Physics in December 2022. The report of calibration indicated a relative combined standard uncertainty for the calibration of this secondary standard gauge as 1.5%; calibration of the gasification apparatus heat flux gauge in comaprison to this secondary standard incorporates (root sum of squares) an additional uncertaintly component of 0.5% (repeatability of calibration). Thus, the relative expanded uncertainty (coverage factor = 2; 95 % confidence interval) for the calibration of the gasification apparatus heat flux gauge is reported as 3.2%

At all 21 locations, and at both target incident heat fluxes (nominally, 25 kW m-2 and 50 kW m-2), measured heat flux was found to increase quickly (and repeatably) after shutter removal, following the time response curves shown in Fig. 2. In this figure, heat fluxes are plotted as time-averaged values (60 s intervals) that are normalized by the local 'steady state' value of heat flux measured between 240s to 300s (i.e., q\*=q”/q"{240s-300s}).  The mean value of q\*=q"/q"{240s-300s} measured at each of the 21 locations of interest is reported at each time interval of interest in Table 1. Here, error bars represent one standard deviation of all 21 values of q\* calculated at that time interval. 

|<img src="https://github.com/MaCFP/matl-db/blob/master/PMMA/Validation_Data/NIST_Gasification_Apparatus/q25_normalized.png" width="300">|  <img src="https://github.com/MaCFP/matl-db/blob/master/PMMA/Validation_Data/NIST_Gasification_Apparatus/q50_normalized.png" width="300">| 
|-----|-----|
|(a)|(b)|

Figure 2. Time-averaged, normalized incident heat flux (i.e., q*=q"/q"{240s-300s}) at r = 0, 2.5, 5.0 and 7.1 cm (21 locations)

Table 1. Measured mean normalized heat flux, q*=q"/q"{240s-300s}, at 21 locations of interest (0 < r < 7.1 cm) for tests conducted at (a) 25 kW m-2 and (b) 50 kW m-2.
|Time Range (s)|Target heat flux: 25 kW m-2|Target heat flux: 50 kW m-2|
|---------------------|-----------------|-----------------|
|1-10  	    |0.9326 +/- 0.0057| 0.9401 +/- 0.0064|
|10-60   	|0.9521 +/- 0.0037| 0.9598 +/- 0.0040|
|60-120  	|0.9770 +/- 0.0026| 0.9831 +/- 0.0024|
|120-180 	|0.9916 +/- 0.0018| 0.9946 +/- 0.0012|
|180-240	|0.9977 +/- 0.0009| 0.9987 +/- 0.0006|
|240-300	|1.0000 +/- 0.0000| 1.0000 +/- 0.0000|
|300-600	|1.0008 +/- 0.0010| 1.0004 +/- 0.0007|

Figure 3 plots a representative image of q"{240s-300s}, as measured across the sample's surface (to obtain the smooth shading shown here, plotted values are linearly interpolated between each measurement location reported in Table 2). As seen here, incident heat flux across the top of the sample's surface is highly uniform. Specifically, with a target heat flux of 25 kW m-2, average q"{240s-300s} within  r < 3.5 cm (i.e., inside the black ring in Fig. 3, which corresponds to the sample’s perimeter) measures 24.7 kW m-2 and, at this time interval, 90% of the sample's surface is exposed to an incident heat flux >97.25% of the target value of 25. kW m-2 (at r=0). With a target heat flux of 50 kW m-w, average q"{240s-300s} within  r < 3.5 cm measures 49.3 kW m-2 and, at this time interval, 90% of the sample's surface is exposed to an incident heat flux >97.5% of the target value of 50 kW m-2 (at r=0). Absolute values of q"{240s-300s} measured at r = 0cm, 2.5cm, 5.0cm and 7.1cm are reported (at both target heat fluxes) in Tables 2a and 2b.

|<img src="https://github.com/MaCFP/matl-db/blob/master/PMMA/Validation_Data/NIST_Gasification_Apparatus/q25_hfmap.png" width="300"> |  <img src="https://github.com/MaCFP/matl-db/blob/master/PMMA/Validation_Data/NIST_Gasification_Apparatus/q50_hfmap.png" width="300">| 
|-----|-----|
|(a)|(b)|

Figure 3. Measured steady state heat flux profile across the sample's surface for tests conducted at (a) 25 kW m-2 and (b) 50 kW m-2.

Table 2a. Target heat flux: 25 kW m-2. Steady state heat flux (i.e., mean(q"(240s < t < 300s)) at r = 0cm, 2.5cm, 5.0cm and 7.1cm
| Radial Distance, r (cm) | # of Measurements | Average heat flux, q"{240s-300s} (kW m-2) |
|---------------------|-----------------|-----------------|
| 0 | 5 | 25.0** +/- 0.1** |
| 2.5 | 8 | 24.8 +/- 0.0 |
| 5.0 | 8 | 23.6 +/- 0.1 |
| 7.1 | 4 | 22.4 +/- 0.3 |

Table 2b. Target heat flux: 50 kW m-2. Steady state heat flux (i.e., mean(q"(240s < t < 300s)) at r = 0cm, 2.5cm, 5.0cm and 7.1cm
| Radial Distance, r (cm) | # of Measurements | Average heat flux, q"{240s-300s} (kW m-2) |
|---------------------|-----------------|-----------------|
| 0 | 6 | 50.0 +/- 0.2 |
| 2.5 | 8 | 49.5 +/- 0.1 |
| 5.0 | 8 | 47.6 +/- 0.3 |
| 7.1 | 4 | 44.6 +/- 0.9 |

In Tables 2a and 2b, tabulated values of q"{240s-300s} represent the mean of repeated measurements (4 to 8 measurements) recorded at the same radial distance, r; reported uncertainties represent two standard deviations of the mean of each of these measurements.

Convection heat transfer at the top and bottom surfaces of the sample can be estimated as per empirical correlations for convection heat transfer (e.g., Nusselt number correlations] or based on recent DNS simulations of heat flow in a similar configuration [4]. To support model validation of these boundary conditions, measurement data is provided in the [Experimental Data Section](https://github.com/MaCFP/matl-db/blob/master/PMMA/Validation_Data/NIST_Gasification_Apparatus/) (Black-Copper\_Temp.csv and Black-Insulation\_Temp.csv) that describes in depth-temperature rise (inert samples, with known thermophsyical properties) in response to this heater application. Each of these files presents mean temperature measurements (i.e., average temperature recorded at the same location(s) in three repeated experiments); at each time step, reported uncertainties represent two standard deviations of the mean of values recorded across repeat experiments in a +/- 1 s time interval.


## Experimental Procedure and Results
### Sample Information
All PMMA samples (discs) studied in this test series were weighed, measured, and firmly attached to a 5.72 mm thick layer (8.25 cm diameter disc) of Kaowool PM Insulation board (Thermophysical Properties [5] of this insulation material are provided in Table 4) using a small amount (1.5g to 2.5g) of a high temperature epoxy (Loctite 9017). Preliminary tests identified that this epoxy layer was needed to prevent sample deformation caused by either (a) thermally induced strain/bending due to the temperature gradient across the thickness of the sample [hot at its top surface, cool below] or (b) the formation of a bubble (trapped gaseous pyrolyzates) at the back surface of samples during testing. A thin ring (approximately 6 mm wide) of Kaowool PM insulation was fitted around the outer edge of the sample to protect it from radiant heat exposure during tests. When temperature measurements were recorded in a given test, two or three thermocouples (k-type, bare bead, wire diameter = 0.125 mm or 0.25 mm) were positioned in the epoxy layer, within 0.6cm of the midpoint (i.e., at r < 0.6cm) of the back surface of samples. Across all tests (five total repetitions) temperature measurements showed no dependence on thermocouple wire diameter (0.125 mm or 0.25 mm). Prepared sample/insulation assemblies were stored in a desiccator in the presence of Drierite for a minimum of 24 hours prior to testing. Sample size and mass information are provided in Table 3.

Table 3. Sample size, mass, and [name] information
|Experimental Data File Name |  Sample Mass (g)| Epoxy Mass (g)| Sample Diameter (cm)| Sample Thickness (mm)|
|-----|-----|-----|-----|-----|
|MaCFP-PMMA\_q50\_Mass\_R3|26.689|1.565|NR|5.9|
|MaCFP-PMMA\_q50\_Mass\_R4|25.643|2.549|NR|5.65|
|MaCFP-PMMA\_q50\_Mass\_R5|28.113|2.176|6.99|6.20|
|MaCFP-PMMA\_q50\_Temp\_R1|24.303|NR|6.99|5.35|
|MaCFP-PMMA\_q50\_Temp\_R2|25.136|NR|6.99|5.52|
|MaCFP-PMMA\_q50\_Temp\_R3|27.877|NR|6.99|6.12|
|MaCFP-PMMA\_q50\_Temp\_R4|27.499|1.876|6.98|6.10|
|MaCFP-PMMA\_q50\_Temp\_R5|28.187|2.217|6.98|6.25|

NR = Not Recorded

### Test Procedure
At the start of each day of testing, incident heat flux at a location corresponding to the center of the top surface of samples is measured using a water-cooled heat flux gauge. During this heater calibration, cooling water and nitrogen are both provided to the system at the same flow rates as used during actual experiments. Test-to-test, heat flux measured at this location is highly repeatable; however, minor adjustments (1 C difference in heater set point) may be made to ensure steady heat flux readings are within 0.1 kW m-2 of the target value, 50 kW m-2. After this heater calibration, the water-cooled shutter is inserted beneath the cone heater, nitrogen flow to the system is turned off, the chamber base plate is lowered, and the heat flux gauge (and holder) is removed and replaced by the sample stand. 

Four layers of Kaowool PM insulation are positioned at the top of the sample stand and a prepared sample-insulation assembly is then placed above (see insert at bottom right of Fig. 1).  Each of these insulation discs (8.25 cm diameter, average total thickness of four discs = 2.28 cm) is stored in a desiccator in the presence of Drierite for a minimum of 24 hours prior to testing. If temperature measurements are recorded in a given test, thermocouples are now connected to the data acquisition system. The sample and chamber base platform are centered beneath the cone heater and then a hydraulic lifting mechanism is actuated to lift the base plate such that (a) the chamber is sealed and (b) the top surface of the sample is positioned at the sample location as the heat flux gauge during calibration. The chamber is then purged with nitrogen (566 L/min) and the data acquisition system is turned on to monitor system conditions (and to begin recording sample mass or back surface temperature). After approximately ten minutes, once the measured oxygen concentration maintains 0.00% and heater temperature reaches a steady value (+/-0.1 C), video recording is started, and the water-cooled shutter is removed thus exposing the sample's surface to a nominal heat flux of 50 kW m-2. The sample is continuously exposed to this radiant heat flux until complete gasification is observed. Approximately 30 s later, the water-cooled shutter is re-inserted beneath the heater, nitrogen flow to the system is turned off, and data acquisition is terminated. 

### Measurements
#### PMMA Gasification 
Time-resolved measurements of PMMA sample mass and back surface temperature rise when exposed to a nominal incident heat flux of 50 kW m-2 are provided (as .csv files) in the [Validation Data Section](https://github.com/MaCFP/matl-db/blob/master/PMMA/Validation_Data/NIST_Gasification_Apparatus/); Table 3 provides key information about each of these tests.  Note: Measurement data from Tests q50\_Mass\_R1 and q50\_Mass\_R2 are not provided in this repository due to observed sample deformation (i.e., separation of the back surface of these samples from the backing insulation, when the two were not bonded together by an epoxy layer). Measurement data from PMMA samples exposed to a nominal incident heat flux of 25 kW m-2 is currently under internal review and will be posted shortly.

Figure 4 plots time-resolved measurements of PMMA Mass and Mass Loss Rate when exposed to an incident radiant heat flux of 50 kW m-2. In this figure (and in the associated .csv files) initial mass equals initial sample mass; negative masses recorded toward the end of each experiment (see Fig. 4a) correspond to mass loss of the epoxy layer at the back surface of the sample (relevant sample and epoxy mass information is provided in Table 3, above). As seen in Fig. 4, strong agreement is observed between the onset of decomposition time, initial, rate of rise, and peak MLR, and test duration. Slight differences in measured MLR behavior can be observed between [Tests q50\_Mass\_R3 and q50\_Mass\_R4] and [q50\_Test Mass\_R5]: specifically, the sample in Test R5 (which was approximately 7.5% thicker and heavier) supported a slightly lower MLR and longer test duration (Fig. 4b).

|<img src="https://github.com/MaCFP/matl-db/blob/master/PMMA/Validation_Data/NIST_Gasification_Apparatus/MaCFP-PMMA_q50_Mass.png" width="300"> |  <img src="https://github.com/MaCFP/matl-db/blob/master/PMMA/Validation_Data/NIST_Gasification_Apparatus/MaCFP-PMMA_q50_MLR.pdf" width="300">| 
|-----|-----|
|(a)|(b)|

Figure 4. Time-resolved measurements of PMMA Mass and Mass Loss Rate when exposed to an incident radiant heat flux of 50 kW m-2.

Figure 5 plots time-resolved measurements of back surface temperature rise recorded in 5 repeated tests on MaCFP-PMMA exposed to an incident radiant heat flux of 50 kW m-2. Measured Ttemperatures are highly repeatable; however, a notable dependence in the rate of rise of back surface temperature is observed with thicker samples (i.e., Tests R3, R4, and R5) showing delayed increases in measured back surface temperature.

<img src="https://github.com/MaCFP/matl-db/blob/master/PMMA/Validation_Data/NIST_Gasification_Apparatus/MaCFP-PMMA_q50_Back-Temp.png" width="400">
Figure 5. Time-resolved measurements of PMMA back surface temperature when exposed to an incident radiant heat flux of 50 kW m-2.


#### Heating of Inert Materials
Also included in the [Validation Data Section](https://github.com/MaCFP/matl-db/blob/master/PMMA/Validation_Data/NIST_Gasification_Apparatus/) are measurements of temperature rise of inert materials (Copper and Kaowool PM Insulation) exposed to the same conditions (i.e., Nitrogen flow rate + incident radiant heat flux) as used during tests on PMMA samples. Experiments in both of these test configurations were repeated three times each; thus, each of these files presents mean temperature measurements (i.e., average temperature recorded at the same location(s) in three repeated experiments). At each time step, reported uncertainties (Uc) represent two standard deviations of the mean of values recorded across repeat experiments in a +/- 1 s time interval. These test results may be used to validate material thermophysical properties and boundary conditions (e.g., convection heat transfer) controlling heat transfer in this system.

In ['Black Insulation' Tests](https://github.com/MaCFP/matl-db/blob/master/PMMA/Validation_Data/NIST_Gasification_Apparatus/Black-Insulation_q50.csv), five discs of Kaowool PM Insulation (8.25 cm diameter, average thickness of each disc = 0.572 cm) are stacked on top of one another, pinned together (3-5 pins were pushed through the thickness of each disc to hold them together while heated), and exposed to the radiant heater at 50 kW m-2. The top surface of the upper layer of this insulation was coated with an optical black paint of emissivity 0.95. In-depth temperature rise is measured near the center (i.e., r<0.6cm) of discs, between the top four layers of insulation (i.e., at 5.72 mm, 11.44 mm, and 17.16 mm from the top surface of the sample).

In ['Black Copper' Tests](https://github.com/MaCFP/matl-db/blob/master/PMMA/Validation_Data/NIST_Gasification_Apparatus/Black-Copper_q50.csv), a 0.3175 mm thick (i.e., 1/8 in. thick) copper disc coated with a high temperature optical black coating (emissivity = 0.92) is placed on top of five discs of Kaowool PM Insulation (8.25 cm diameter, average thickness of each of the top four discs = 0.572 cm; the bottom Kaowool PM disc was just 0.3175 mm thick) that are stacked on top of one another and pinned together (3-5 pins were pushed through the thickness of each disc to hold them together while heated). The copper plate was then exposed to the radiant heater at 50 kW m-2 and its temperature is recorded by a thermocouple embedded at the center (r=0) of its back surface.

## Notes
Table 4. Thermophysical Properties of Kaowool PM Insulation Board [5]
|Temperature ( C)|  Thermal conductivity (W/m-K)| 
|---------------------|-----------------|
|260  	| 0.0576|
|538   	| 0.085|
|816  	| 0.125|
|1093		| 0.183|
Density:		256 kg/m3 [5,7]
Heat Capacity:	1070 J/kg-K (at 980 C) [6 via 7]


## References
1. Leventon, I.T., De Lannoye, K., Anaerobic Gasification of Poly(methyl methacrylate) Under External Thermal Radiation, NIST Technical Note 23xx, National Institute of Standards and Technology, Gaithersburg, MD, _(In Preparation)_. 
2. Leventon, I.T., Batiot, B., Bruns, M.C., Hostikka, S., Nakamura, Y., Reszka, P., Rogaume, T., Stoliarov, S.I., “The MaCFP Condensed Phase Working Group: A Structured, Global Effort Towards Pyrolysis Model Development,” ASTM Selected Technical Papers, 2022. (Accepted, ASTM STP 1642)
3. Austin, P.J., Buch, R.R., Kashiwagi, T., "Gasification of Silicone Fluids Under External Thermal Radiation", NISTIR 6041, National Institute of Standards and Technology, Gaithersburg, MD, 1997. 
4. Swann, J.D., Ding, Y., McKinnon, M.B., Stoliarov, S.I., "Controlled atmosphere pyrolysis apparatus II (CAPA II): A new tool for analysis of pyrolysis of charring and intumescent polymers." Fire Safety Journal 91 (2017): 130-139.
5. Thermal Ceramics, Kaowool Low Temperature Boards, \url{https://www.fabricationspecialties.com/pdf/lowtemp.pdf}, accessed Feb. 1, 2023
6. Organic RCF Vacuum Formed Products, \url{http://www.morganthermalceramics.com/files/datasheets/kaowoolpmvacuumformed514-700.pdf}, accessed Dec. 21, 2012.
7. McKinnon, M.B., Stoliarov, S.I., & Witkowski, A., "Development of a pyrolysis model for corrugated cardboard," Combustion and Flame  160 (2013): 2595-2607.