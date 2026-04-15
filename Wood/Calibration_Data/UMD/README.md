# University of Maryland (UMD)

### Experimental Conditions: TGA/DSC
A NETZSCH STA 449 F3 Jupiter was used to simultaneously conduct Thermogravimetric Analysis (TGA) and Differential Scanning Calorimetry (DSC) experiments.

* Heating Rate: 10 K/min
* Temperature program
  - Initial Temperature: 294 K
  - Initial Isotherm: 1800 s (hold at 294 K for 1800 s)  
  - Maximum Temperature: 1098 K
  - Final Isotherm: 1800 s (hold at 1098 K for 1800 s)  
* Sample mass: 4 mg +/- 0.3 mg
* Sample geometry: Powdered
* Calibration type: Before each experiment, a baseline test was performed using an empty crucible. Temperature/Heat flow calibration were performed every 2 months (or 100 tests, whichever is sooner) using a set of 8 reference materials with transition temperature between 312-1081 K
* Crucible
  - Type: Pt-Rh
  - Volume: 85 uL
  - Diameter: 6.8 mm
  - Mass: 253.480 mg
  - Lid: True
  - Note: Pt-Rh crucibles (outer diameter 6.8mm / volume 85 uL) with a lid ( a small hole in the lid allowed for gaseous decomposition products to escape).
* Carrier Gas
  - Type: Nitrogen
  - Flow rate: 70 ml/min (50 mL/min purge, 20 mL/min protective)
  - Note: Ultra High Purity (UHP) Nitrogen
* Instrument
  - Type: NETZSCH STA 449 F3 Jupiter
  - Furnace Type: Platinum
  - Notes: None

| Test Name | O2 volume % |  Initial External Sample Mass (mg) | Sample Mass Prior to Heating Ramp (mg) |
| --------- | :---------: | :------------------------: | :------------------------: |
|UMD\_STA\_N2\_10K\_R1 | 0 | 4.301| 4.066
|UMD\_STA\_N2\_10K\_R2 | 0 | 4.062| 3.842
|UMD\_STA\_N2\_10K\_R3 | 0 | 3.942| 3.904

**Notes:** **Initial External Sample Mass** refers to the mass of the sample before being inserted into the instrument. **Sample Mass Prior to Heating Ramp** refers to the mass of the sample at the beginning of the dynamic heating segment of the test. The discrepancy reflects moisture lost before the measurement begins and during the 1800 s isothermal segment prior to the heating ramp.

### Experimental Conditions, Gasification (CAPA)
*Reference: More information is available at:
  - [J. Swann, et al., Fire Safety Journal, 2017, https://doi.org/10.1016/j.firesaf.2017.03.038]
  - [Grayson Bellamy Masters Thesis, DEVELOPMENT AND IMPROVEMENTS OF THE CONTROLLED ATMOSPHERE PYROLYSIS APPARATUS, University of Maryland, 2022, https://doi.org/10.13016/gzi8-ivaz]
* Sample Surface Area: 0.00385 m2 (nominal); see test conditions table for per-sample values
* Sample Diameter: 0.07 m (nominal); see test conditions table for per-sample values
* Sample holder dimensions:
    - Circular pan: 81.9 mm inner diameter x 25.0 mm depth
* Sample adhered to 0.0127 mm thick copper foil with high temperature zirconia adhesive (Cotronics Resbond 904)
* Bottom face of foil painted with Medtherm High Temperature Optical Black Coating (HT2000) - manufacturer stated absorptance ~ 0.92 over 0.5-20 um in temperature range of interest [See: Bellamy, et al., Fire Safety Journal, 2023, https://doi.org/10.1016/j.firesaf.2023.103775]
* Infrared camera (FLIR E40) focused on exposed surface of painted copper foil
* Edge Insulation: 6 mm thick insulation in ring around edge of sample and stacked to the bottom of the sample holder such that the surface of the sample is flush with the surface of the sample holder (Kaowool PM Board. Density = 240 kg/m3. Thermal Conductivity 0.0577, 0.0851, 0.126, 0.183 W/m-K (at 260, 538, 816, 1093 C, respectively))
* 185 SLPM N2 annular purge

##### Test Summary
Ten gasification tests were conducted to measure the mass loss and back surface temperature of white pine samples in a nitrogen environment at external heat fluxes of 30, 50, and 70 kW/m2. The samples are cylindrical disks with a nominal diameter of 70 mm and a nominal thickness of 8.5 mm. The sample was insulated at the edges with top and back surfaces uninsulated. A cone heater identical to that installed in the cone calorimeter was used in the experiments with the surface of the cone 40 mm from the surface of the sample.

The spatial mean of the sample back surface temperature from a circle with a diameter of approximately 60 mm at the geometric center of the sample is presented in the test output files.

Tests were conducted in a laboratory environment with ambient temperature of 24-28 C and relative humidity of 21-31%.

###### Test Heating Conditions

| Test Name | Heat Flux (kW/m2) | Heater Temperature (K) | Diameter (mm) | Thickness (mm) | Initial Dry Mass (g) | Mass Loss (g) | Top Surr. T (K) | Bot. Surr. T (K) |
|-----------|:-----------------:|:----------------------:|:-------------:|:--------------:|:--------------------:|:-------------:|:---------------:|:----------------:|
| UMD\_Wood\_CAPA\_N2\_30kW\_R1 | 30 | 873.4  | 69.51 | 8.50 | 11.43 | 6.26 | 392.4 | 302.9 |
| UMD\_Wood\_CAPA\_N2\_30kW\_R2 | 30 | 870.9  | 69.42 | 8.52 | 12.17 | 6.39 | 394.6 | 303.8 |
| UMD\_Wood\_CAPA\_N2\_30kW\_R3 | 30 | 873.1  | 69.60 | 8.49 | 11.16 | 5.55 | 390.9 | 301.9 |
| UMD\_Wood\_CAPA\_N2\_50kW\_R1 | 50 | 1002.9 | 69.48 | 8.45 | 12.60 | 9.12 | 447.7 | 307.9 |
| UMD\_Wood\_CAPA\_N2\_50kW\_R2 | 50 | 1001.9 | 69.48 | 8.52 | 11.97 | 8.60 | 447.7 | 307.6 |
| UMD\_Wood\_CAPA\_N2\_50kW\_R3 | 50 | 1004.5 | 69.27 | 8.50 | 12.10 | 8.97 | 449.7 | 308.1 |
| UMD\_Wood\_CAPA\_N2\_50kW\_R4 | 50 | 1004.5 | 69.50 | 8.49 | 11.05 | 8.00 | 449.3 | 307.9 |
| UMD\_Wood\_CAPA\_N2\_70kW\_R1 | 70 | 1100.2 | 69.62 | 8.50 | 11.48 | 8.69 | 497.0 | 311.7 |
| UMD\_Wood\_CAPA\_N2\_70kW\_R2 | 70 | 1100.8 | 69.53 | 8.50 | 10.90 | 8.39 | 498.8 | 311.7 |
| UMD\_Wood\_CAPA\_N2\_70kW\_R3 | 70 | 1100.3 | 69.63 | 8.51 | 11.26 | 8.71 | 497.5 | 312.1 |

**Notes:**
- **Mass Loss** is computed from the assembly mass before and after the test (assembly = sample + copper foil + adhesive + paint + edge insulation + sample cup). This is reported in preference to a sample-only char yield because some sample, adhesive, and copper material is typically retained or lost on the foil during disassembly, making sample-only measurements less reliable.
- **Top Surr. T** is the Top (Heater Exposed) Surface Surroundings Temperature, time-averaged over the heater-on portion of the test from the outer wall thermocouple (the enclosure wall facing the cone heater). **Bot. Surr. T** is the Bottom (IR Measured) Surface Surroundings Temperature, time-averaged from the inner wall thermocouple (the enclosure wall on the IR viewing side of the sample).
- **UMD\_Wood\_CAPA\_N2\_50kW\_R4**: the back-surface IR data dropped out at t = 43 s; mass data is complete for the full test. Back-surface temperature for t >= 43 s appears as `NaN` in the file.
- **UMD\_Wood\_CAPA\_N2\_70kW\_R1**: post-test char properties were measured as char diameter = 64.4 mm, char thickness = 9.2 mm, char mass = 2.73 g, and char density = 91.5 kg/m3. Char properties were not measured for the other samples.