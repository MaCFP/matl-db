# Technical Institute of Fire Protection in Prague (TIFP)

### Experimental Conditions: TGA, DSC
TGA and DSC were performed simultaneously using an STA appartus.
STA experiments performed both in nitrogen and in air. Although tests were conducted simultaneously, TGA and DSC measurement data presented here are separated into two files, for consistency with other datasets.
Note: DSC heat flow data was rescaled (multiplied by -1)such that endothermic heat flow events are positive (endo up)

##### STA Tests in Nitrogen
* Heating Rate: 10 K/min
* Temperature program
  - Initial Temperature: 300.15 K
  - Initial Isotherm: 5 minutes
  - Maximum Temperature: 823.15 K
  - Final Isotherm: None
* Sample mass: ~5.4 mg
* Sample geometry: powdered
* Calibration type: nitrogen 70 ml/min, Al2O3 crucible, open, 10 °C/min, 20 to 1000 °C, material In, Bi, Zn, Al, Ag
* Crucible
  - Type: Al2O3
  - Volume: 85 µL
  - Diameter: None
  - Mass: None
  - Lid: False
  - Note: None
* Carrier Gas
  - Type: Nitrogen
  - Flow rate: 70 ml/min
  - Note: Pure Nitrogen (0% O2), purge flow 50 ml/min + protective 20 ml/min
* Instrument
  - Type: STA apparatus
  - Note: Simultaneous Thermal Analysis (TGA + DSC), measurement data presented as two separated files. 8 runs were performed - five with 1 evacuation and fill cycle before measurement (tests 1,2,4,5,6), three with 4 evacuation and fill cycles before measurement (tests 7,8,9). Tests 4-9 were conducted in Fall 2020 following the identification of two 'peaks' in TGA mass loss data when just one evacuation cycle prior to measurement was performed.

| Test Name | O2 volume % |  Initial Sample Mass (mg) | 
| --------- | :---------: | :------------------------: |
|TIFP\_STA\_N2\_10K\_1 | 0 | 5.4338|  
|TIFP\_STA\_N2\_10K\_2 | 0 | 5.3668|  
|TIFP\_STA\_N2\_10K\_4| 0 | 5.1046|  
|TIFP\_STA\_N2\_10K\_5| 0 | 5.7616|  
|TIFP\_STA\_N2\_10K\_6| 0 | 5.4602|  
|TIFP\_STA\_N2\_10K\_7| 0 | 5.6086|  
|TIFP\_STA\_N2\_10K\_8| 0 | 5.0804|  
|TIFP\_STA\_N2\_10K\_9| 0 | 5.7491|  

##### STA Tests in Air
* Heating Rate: 10 K/min
* Temperature program
  - Initial temperature 298.15 K
  - Isotherm: None
  - Maximum Temperature 1023.15 K
* Sample mass: ~5.85 mg
* Sample geometry: powdered
* Calibration type: air,  10 °C/min, material In
* Crucible type: Al2O3, 70 microliters, no lid
* Carrier Gas
  - Air (vol % O2 = ambient)
  - Flow rate = purge flow 50 ml/min + protective 10 ml/min

| Test Name | O2 volume % |  Initial Sample Mass (mg) | 
| --------- | :---------: | :------------------------: |
|TIFP\_STA\_O2-21\_10K\_1 | Ambient | 4.4790|  
|TIFP\_STA\_O2-21\_10K\_2 | Ambient | 5.2040|  



### Experimental Conditions: Cone Calorimeter
* Radiant heat flux 25 and 65 kW/m2, three runs were performed for each heat flux. Backside tempereature measured by K type thermocouples glued to the sample in the middle (x=0, y=0) and at location x=-25 mm, y=0. 
* Extraction flow rate: 24L/s
* Sample Surface Area: 0.0084 m2
* Sample holder dimensions:
    - according to ISO 5660-1, stainless steel
    - Retainer frame/grid: frame was used
* Backing Insulation: earth-alkali silicate wool, [thickness?], thermal conductivity at 600K 0.16 kW/m/K 
* Thermocouple location:
    - Temperature1: glued to back surface of sample, at center
    - Temperature2: glued to back surface of sample, x=-25 mm, y=0
* Note: For consistency with datasets submitted by other institutions, cone calorimeter HRR measurements submitted by TIFP have been normalized by sample surface area (nominal) to provide HRR per unit area [kW/m2]

###### Test Heating Conditions [confirm units of Temperature ?]  
|Test Name | Heat Flux (kW/m2)| Heater Temperature (K) 
|----------|:------:| :---: |
|TIFP_Cone_25kW_1| 25 | 1134.65 |
|TIFP_Cone_25kW_2| 25 | 1134.65 |
|TIFP_Cone_25kW_3| 25 | 1134.65 |
|TIFP_Cone_65kW_1| 65 | 1397.15 |
|TIFP_Cone_65kW_2| 65 | 1397.15 |
|TIFP_Cone_65kW_3| 65 | 1397.15 |


### Experimental Conditions: Gasification Tests
* Radiant heat flux 65 kW/m2, two runs were performed in a cone calorimeter apparatus with vitiated atmosphere module, pure nitrogen.
* Extraction flow rate: 24L/s
* Sample Surface Area: 0.0084 m2
* Sample holder dimensions:
    - according to ISO 5660-1, stainless steel
    - Retainer frame/grid: frame was used
* Backing Insulation: earth-alkali silicate wool, [thickness?], thermal conductivity at 600K 0.16 kW/m/K 
* Thermocouple location: None

###### Test Heating Conditions [confirm units of Temperature ?]  
|Test Name | Heat Flux (kW/m2)| Heater Temperature (K) 
|----------|:------:| :---: |
|TIFP_Gasification_65kW_1| 65 | 1403.15 |
|TIFP_Gasification_65kW_2| 65 | 1403.15 |
