# UL Fire Safety Research Institute (FSRI)

### Experimental Conditions: TGA/DSC
A NETZSCH STA 449 F3 Jupiter was used to simultaneously conduct Thermogravimetric Analysis (TGA) and Differential Scanning Calorimetry (DSC) experiments.

* Heating Rate: 10 K/min
* Temperature program
  - Initial Temperature: 323 K
  - Initial Isotherm: 600 s (hold at 323 K for 600 s)  
  - Maximum Temperature: 1073 K
  - Final Isotherm: 600 s (hold at 1098 K for 600 s)  
* Sample mass: 4.0 mg +/- 0.1 mg
* Sample geometry: Powdered
* Calibration type: Before each experiment, a baseline test was performed using an empty crucible. Temperature/Heat flow sensitivity calibration were performed every 200 temperature cycles using a set of 6 reference materials with melting temperature between 312-1081 K
* Crucible
  - Type: Pt-Rh
  - Volume: 85 uL
  - Diameter: 6.8 mm
  - Mass: See Below (Reference crucible: 256.93 mg)
  - Lid: True
  - Note: Pt-Rh crucibles (outer diameter 6.8mm / volume 85 uL) with a lid (a small hole in the lid allowed for gaseous decomposition products to escape).
* Carrier Gas
  - Type: Nitrogen
  - Flow rate: 70 ml/min (50 mL/min purge, 20 mL/min protective)
  - Note: Ultra High Purity (UHP) Nitrogen
* Instrument
  - Type: NETZSCH STA 449 F3 Jupiter
  - Furnace Type: Platinum
  - Notes: None

| Test Name | O2 volume % |  Initial Sample Mass (mg)  | Cruicble Mass (mg) |
| --------- | :---------: | :------------------------: | :----------------: |
|FSRI\_STA\_N2\_3K\_R1  | 0 | 4.02 | 252.00 |
|FSRI\_STA\_N2\_10K\_R1 | 0 | 3.97 | 253.88 |
|FSRI\_STA\_N2\_10K\_R2 | 0 | 3.99 | 256.93 | 
|FSRI\_STA\_N2\_10K\_R3 | 0 | 3.94 | 255.14 | 
|FSRI\_STA\_N2\_30K\_R1 | 0 | 4.05 | 263.15 | 
|FSRI\_STA\_N2\_30K\_R2 | 0 | 4.05 | 256.71 | 
|FSRI\_STA\_N2\_30K\_R3 | 0 | 3.98 | 252.42 | 

### Experimental Conditions, Gasification (CAPA)
*Reference: More information is available at: 
  - [J. Swann, et al., Fire Safety Journal, 2017, https://doi.org/10.1016/j.firesaf.2017.03.038]
  - [Grayson Bellamy Masters Thesis, DEVELOPMENT AND IMPROVEMENTS OF THE CONTROLLED ATMOSPHERE PYROLYSIS APPARATUS, University of Maryland, 2022, https://doi.org/10.13016/gzi8-ivaz]
* Sample Surface Area: 0.00385 m2 (nominal)
* Sample Diameter: 0.07 m (nominal)
* Sample holder dimensions:
    - Circular pan: 80mm x 20mm
* Sample adhered to 0.0254 mm thick copper foil with high temperature zirconia adhesive (Cotronics Resbond 904)
* Bottom face of foil painted with Rust-Oleam High Heat black paint - emissivity ~ 0.92 in temperature range of interest [See: Bellamy, et al., Fire Safety Journal, 2023, https://doi.org/10.1016/j.firesaf.2023.103775]
* Infrared camera (FLIR E95) focused on exposed surface of painted copper foil
* Edge Insulation: 5mm thick insulation in ring around edge of sample and stacked to the bottom of the sample holder such that the surface of the sample is flush with the surface of the sample holder (Kaowool PM Board. Density = 256 kg/m3. Thermal Conductivity 0.0576, 0.0850, 0.125, 0.183 W/m-K (at 260, 538, 816, 1090 C, respectively)
* 185 SLPM N2 annular purge
* Optical pyrometer (Raytek RAYMI310LTF) focused on exposed sample surface during periods of negligible mass loss (pre- and post-decomposition) to measure surface temperature

##### Test Summary
Two repeated gasification tests were conducted to measure the mass loss, front surface temperature, and back surface temperature of white pine samples in a nitrogen environment at external heat fluxes of 40 and 60 kW/m2. The samples are cylindrical disks with a nominal diameter of 70 mm and a nominal thickness of 8.7 mm. The sample was insulated at the edges with top and back surfaces uninsulated. A cone heater identical to that installed in the cone calorimeter was used in the experiments with the surface of the cone 40 mm from the surface of the sample.

The spatial mean of the sample back surface temperature from a circle with a diameter of approximately 30 mm at the geometric center of the sample is presented in the test output files. 

Optical pyrometer measurements were corrected with the emissivity of the virgin and residual sample by dividing the temperature measured assuming emissivity = 1 by the actual emissivity raised to the 1/4 power. Virgin and residual mass emissivity measured with a Bruker Invenio R FTIR and a Bruker A562-G integrating sphere [See: McKinnon and Bellamy, Journal of Fire Sciences, 2024, https://doi.org/10.1177/07349041241235566]. Calculated emissivities used in correction provided in table below.

###### Test Heating Conditions  

|Test Name | Heat Flux (kW/m2)| Heater Temperature (K) | Initial mass (g) | Thickness (cm)| Virgin emissivity | Char emissivity |
|----------|:------:| :---: |:------:| :---: | :---: | :---: |
|FSRI\_CAPA\_N2\_40KW\_R1 | 40| 915.8 | 12.32 | 8.58 | 0.82 | 0.82 |
|FSRI\_CAPA\_N2\_40KW\_R2 | 40| 915.8 | 12.61 | 8.68 | 0.82 | 0.82 |
|FSRI\_CAPA\_N2\_60KW\_R1 | 60| 1033.4 | 13.07 | 8.69 | 0.79 | 0.83 |
|FSRI\_CAPA\_N2\_60KW\_R2 | 60| 1033.4 | 11.93 | 8.69 | 0.79 | 0.83 |


### Experimental Conditions, Cone Calorimetry (Deatak CC-2)

* Tested in general accordance with ASTM E1354
* No edge frame or retaining grid used - instead four ~1mm diameter black wires wrapped around sample at edges to tie down samples
* ~25 mm thick cerawool insulation on back surface

##### Test Summary
Cone calorimeter tests were conducted in general accordance with the ASTM E1354 standard with samples in the horizontal orientation. The heater was approximately 25 mm from the top surface of the sample and the spark igniter was approximately 12 mm from the top surface of the sample. Ignition times asnd times to flame out were observed and recorded manually via the operator pushing a button. Samples are labeled according to the orientation of their grain relative to the sample surface, e.g. `parallel' denotes a sample cut from long boards harvested from axial slices of the tree.

###### Test Heating Conditions  

|Test Name | Mass (g) | Sample Length (mm)| Sample Length (mm) | Sample Thickness (mm) | Time to Ignition (s) | Time to Flame Out (s)
|----------|:------:| :---: |:------:| :------:| :---: |:------:|
|  FSRI\_Wood\_Parallel\_Cone\_25kW\_hor\_R1        |  86.22   |  99.7   |  99.6   |  26.5   |  88.25  |  2279.75  | 
|  FSRI\_Wood\_Parallel\_Cone\_25kW\_hor\_R2        |  89.95   |  99.5   |  99.7   |  26.4   |  91.75  |  2131.75  | 
|  FSRI\_Wood\_Parallel\_Cone\_25kW\_hor\_R3        |  104.35  |  99.5   |  99.6   |  26.3   |  52.25  |  2050.25  | 
|  FSRI\_Wood\_Parallel\_Cone\_50kW\_hor\_R1        |  96.91   |  99.4   |  99.6   |  26.3   |  9.25   |  1460.5   | 
|  FSRI\_Wood\_Parallel\_Cone\_50kW\_hor\_R2        |  96.60   |  99.5   |  99.8   |  26.5   |  11.75  |  1405     | 
|  FSRI\_Wood\_Parallel\_Cone\_50kW\_hor\_R3        |  93.04   |  99.9   |  99.3   |  26.4   |  39.75  |  1449     | 
|  FSRI\_Wood\_Parallel\_Cone\_75kW\_hor\_R1        |  96.84   |  99.4   |  99.7   |  26.4   |  5      |  1220     | 
|  FSRI\_Wood\_Parallel\_Cone\_75kW\_hor\_R2        |  99.16   |  99.5   |  99.8   |  26.3   |  4.75   |  1199.5   | 
|  FSRI\_Wood\_Parallel\_Cone\_75kW\_hor\_R3        |  99.68   |  99.6   |  99.7   |  26.1   |  5      |  1258     | 
|  FSRI\_Wood\_Perpendicular\_Cone\_25kW\_hor\_R1   |  102.06  |  99.9   |  99.8   |  26.5   |  104    |  1957.75  | 
|  FSRI\_Wood\_Perpendicular\_Cone\_25kW\_hor\_R2   |  94.03   |  99.5   |  99.8   |  26.4   |  107    |  2001.5   | 
|  FSRI\_Wood\_Perpendicular\_Cone\_25kW\_hor\_R3   |  103.10  |  100.2  |  100.1  |  26.3   |  135.25 |  1821     | 
|  FSRI\_Wood\_Perpendicular\_Cone\_50kW\_hor\_R1   |  100.94  |  100.1  |  100.2  |  26.3   |  23.75  |  1234.25  | 
|  FSRI\_Wood\_Perpendicular\_Cone\_50kW\_hor\_R2   |  104.65  |  100.3  |  100.5  |  26.5   |  25.25  |  1278     | 
|  FSRI\_Wood\_Perpendicular\_Cone\_50kW\_hor\_R3   |  97.05   |  99.7   |  99.5   |  26.4   |  19.75  |  1213     | 
|  FSRI\_Wood\_Perpendicular\_Cone\_75kW\_hor\_R1   |  98.52   |  100.1  |  100.0  |  26.4   |  10.5   |  902.75   | 
|  FSRI\_Wood\_Perpendicular\_Cone\_75kW\_hor\_R2   |  103.75  |  100.7  |  100.5  |  26.3   |  14.25  |  969.5    | 
|  FSRI\_Wood\_Perpendicular\_Cone\_75kW\_hor\_R3   |  97.21   |  100.0  |  100.0  |  26.1   |  10     |  890.5    | 

### Experimental Conditions, Thermal Diffusivity (Netzsch LFA 467 HT Hyperflash)

* Light flash analysis
* Cylindrical sample ~12.7 mm diameter 
* Both sides of the sample coated with graphite paint

* Sample Diameter: 0.0127 m (nominal)
* Sample Surface Area: 0.0005 m2 (nominal)
* Sample thickness: ~1-2 mm (See Table)
* 4 sample holder (2 x 2) - only 2 samples loaded for each test
* 100 SCCM total N2 purge

##### Test Summary
Thermal diffusivity was measured using a Netzsch LFA 467 HT Hyperflash. The LFA 467 HT Hyperflash uses a xenon light source and an InSb infrared detector. Experiments were conducted on virgin wood samples at temperature intervals from 298 K (25 C) up to 623 K (350 C).

Samples are named below according to the grain orientation relative to the exposed surface of the sample, e.g. `Perpendicular' denotes a sample taken from an axial core of a tree. The dimensions and mass were measured prior to the experiments. The sample surfaces were painted with two coats of graphite spray and tested in open sample holders within the test chamber of the apparatus. Two samples were loaded into the sample holders (that hold a maximum of four samples) for each experiment. The experiments consisted of four shots at each temperature set point. 

The diffusivity was calculated with the standard Netzsch model (improved Cape-Lehmann) assuming the sample dimensions did not change with temperature (i.e. no thermal expansion was defined for the material). The mean calculated diffusivity over the four shots at each temperature is presented in each individual data file. 

###### Test Heating Conditions  

|Test Name | Mass (g) | Thickness (mm)| Diameter (mm) |
|----------|:------:| :---: |:------:|
|FSRI\_Wood\_LFA\_N2\_Parallel\_R1 | 91.24 | 1.885 | 12.68 |
|FSRI\_Wood\_LFA\_N2\_Parallel\_R2 | 95.64 | 1.966 | 12.73 |
|FSRI\_Wood\_LFA\_N2\_Parallel\_R3 | 102.58 | 1.935 | 12.70 |
|FSRI\_Wood\_LFA\_N2\_Parallel\_R4 | 93.41 | 1.903 | 12.72 |
|FSRI\_Wood\_LFA\_N2\_Parallel\_R5 | 59.47 | 1.195 | 12.52 |
|FSRI\_Wood\_LFA\_N2\_Parallel\_R6 | 65.54 | 1.082 | 12.65 |
|FSRI\_Wood\_LFA\_N2\_Perpendicular\_R1 | 95.61 | 1.880 | 12.70 |
|FSRI\_Wood\_LFA\_N2\_Perpendicular\_R2 | 93.90 | 1.897 | 1.897 |
|FSRI\_Wood\_LFA\_N2\_Perpendicular\_R3 | 103.24 | 2.009 | 12.74 |
|FSRI\_Wood\_LFA\_N2\_Perpendicular\_R4 | 106.45 | 2.045 | 12.76 |
|FSRI\_Wood\_LFA\_N2\_Perpendicular\_R5 | 99.17 | 1.918 | 12.70 |
|FSRI\_Wood\_LFA\_N2\_Perpendicular\_R6 | 94.82 | 1.835 | 12.73 |