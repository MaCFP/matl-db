# README File for TIFP+UCT
Technical Institute of Fire Protection, Prague (TIFP) and University of Chemistry and Technology, Prague (UCT).
Please contact Lucie.Hasalova@hzscr.cz or salekv@vscht.cz in case of any concerns.

### Experimental Conditions: TGA/DSC
A NETZSCH STA 449 F3 Jupiter was used to simultaneously conduct Thermogravimetric Analysis (TGA) and Differential Scanning Calorimetry (DSC) experiments. DSC data serve as suplementary only and are not suitable for calibration.

* Heating Rate: 5, 10, and 20 K/min
* Temperature program
  - Initial Temperature: 303 K
  - Initial Isotherm: 300 s (hold at 303 K for 300 s)  
  - Maximum Temperature: 973 K
  - Final Isotherm: 300 s (hold at 973 K for 300 s)
* Sample mass: 5 mg +/- 0.20 mg
* Sample geometry: Powdered
* Calibration type: For each heating rate, a single baseline test was performed using an empty crucible. Temperature/Heat flow calibration for each heating rate were performed prior to MaCFP measurements using a set of 5 reference materials (In, Bi, Zn, Al, Ag) with melting temperatures between 429-1225 K. For more accurate DSC measurements, baseline (blank) measurements would have to be performed before each individual run and the heat flow rate (W/g) would need to be recalculated for the actual, not the initial sample mass.
* Crucible
  - Type: Al2O3
  - Volume: 85 uL
  - Diameter: 9 mm
  - Mass: 132-139 mg
  - Lid: False
  - Note: NETZSCH Al2O3 crucibles were used (part ID NGB800453). For more accurate DSC measurements, Concavus crucibles would be required. 
* Carrier Gas
  - Type: Nitrogen
  - Flow rate: 50 ml/min (50 mL/min purge, 20 mL/min protective - no contact with the sample)
  - Note: Ultra High Purity (UHP) Nitrogen
* Instrument
  - Type: NETZSCH STA 449 F3 Jupiter
  - Furnace Type: Steel
  - Notes: None

| Test Name | O2 volume % | Initial Sample Mass (mg) |
| --------- | :---------: | :----------------------: |
|TIFP+UCT\_STA\_N2\_5K\_R1 | 0 | 4.930|  
|TIFP+UCT\_STA\_N2\_5K\_R2 | 0 | 5.077|  
|TIFP+UCT\_STA\_N2\_5K\_R3 | 0 | 5.107|  
|TIFP+UCT\_STA\_N2\_5K\_R4 | 0 | 5.088| 
|TIFP+UCT\_STA\_N2\_10K\_R1 | 0 | 5.196|  
|TIFP+UCT\_STA\_N2\_10K\_R2 | 0 | 4.952| 
|TIFP+UCT\_STA\_N2\_10K\_R3 | 0 | 5.139| 
|TIFP+UCT\_STA\_N2\_20K\_R1 | 0 | 5.023| 
|TIFP+UCT\_STA\_N2\_20K\_R2 | 0 | 5.112| 
|TIFP+UCT\_STA\_N2\_20K\_R3 | 0 | 4.917| 

* Note
  - The first and second two measurements at heating rate of 5 K/min were taken on a different day. The difference in TGA data may be caused by different humidity levels. MLR data in the main part of thermal decomposition which are used for calibration are not affected.

### Experimental Conditions: Cone calorimeter with controlled atmosphere

* Test Standard: ISO/TS 5660-5:2020
* Extraction flow rate: 24L/s
* Sample Surface Area: 0.01 m2 (nominal)
* Sample holder dimensions:
    - Square pan: 106mm x 106mm x 25mm
    - Retainer frame: None
    - Retaining grid: None
* Backing Insulation: 2.3 cm thick layer of Dalfratherm 1260 Hybrid Blanket. Density = 128 kg/m3. Thermal Conductivity 0.05, 0.09, 0.13, 0.18, 0.25 W/m-K (at 200, 400, 600, 800, 1000 C, respectively)
* Thermocouple location: Three thermocouples (TCs, bare-wire K-type with uninsulated junctions, bead diameter ~1 mm) were positioned along the main diagonal of a 10×10 cm square, measured from the bottom-left corner (0,0) in a top-down view. TC1 (2.9, 2.9 cm) was located toward the bottom-left corner, TC2 (5.0, 5.0 cm) at the center of the square, and TC3 (7.1, 7.1 cm) toward the top-right corner.
* Ignition Source: -

##### Test Summary
Experiments were conducted on FTT iCone mini with controlled atmosphere module and truncated conical radiant heater. Three repeated pyrolysis tests were conducted to measure the mass loss and back surface temperature in nitrogen environment at external heat flux of 30 and 60 kW/m2, respectively. The sample has a rectangular shape 10 x 10 cm and thickness of 2.54 cm (1 inch). Three thermocouples were glued with the kapton tape to the back of the sample. The sample was wrapped in double coat of aluminium foil from sides and bottom and placed on the sample holder with inserted insulation blanket. No frame or grid were used.

###### Test Heating Conditions  

|Test Name | Heat Flux (kW/m2)| Heater Temperature (K) |Thickness (cm)|Grain orientation (-)|t_ign (s)|t_flameout (s)|
|----------|:------:| :---: |:------:| :---: | :---: | :---: |
|TIFP+UCT\_Gasification\_30KW\_hor\_parallel\_R1 | 30| 913 | 2.54 | parallel| -| -|
|TIFP+UCT\_Gasification\_30KW\_hor\_parallel\_R2 | 30| 913 | 2.54 | parallel|-| -|
|TIFP+UCT\_Gasification\_60KW\_hor\_parallel\_R1 | 30| 1082 | 2.54 | parallel|-| -|
|TIFP+UCT\_Gasification\_60KW\_hor\_parallel\_R2 | 30| 1082 | 2.54 | parallel|-| -|
|TIFP+UCT\_Gasification\_60KW\_hor\_parallel\_R3 | 30| 1082| 2.54 | parallel|-| -|

* Note
  - Two types of samples were distributed among the MaCFP contributors - cut with the wood grain parallel and perpendicular to sample's front surface. The sample type was added to the name of each measurement.
