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
