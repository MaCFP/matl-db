# University of Edinburgh

### Test Summary
Standard cone calorimeter tests were carried out on 100 x 100 x 6 mm slabs of cast black PMMA. Standard cone calorimeter sample holders were used to expose a 95 x 95 mm face of the material to the heating element. A Schmidt-boelter heat flux gauge was used to calibrate the conical heater to within 1% of the desired heat flux. 

For experiments 1-3 (both 25 and 65 kW/m2):

The sample was wrapped with 1 layer of aluminum foil to contain the melting of the PMMA slab over the course of the experiment. The foil was in contact with an aluminum block 10 mm thick with a hole milled for a 1 mm K-type thermocouple. The thermocouple was located 5 mm from the surface that was in contact with the foil. The remaining sample holder depth was filled with ceramic paper.

Before each trial the sample mass was recorded. The sample was observed to be entirely consumed in all of the experiments. The thermocouple wire leading from the sample holder was ran between the opening of the glass doors of the cone calorimeter so that the doors could remain closed. Some slack was provided in the cable to mitigate tension on the sample, however the mass readings may have been influenced by the presence of the thermocouple wire. The reported mass includes the mass of the sample holder, aluminum block, and backing insulation. 

Difference between total mass lost and reported initial sample mass is generally within 5-10%; the highest difference observed was approximately 10 g. The difference in recorded mass loss and initial sample mass may be a result of the thermocouple wire interfering with load cell measurements.

For experiments 4-6 (both 25 and 65 kW/m2):

The sample was wrapped with 1 layer of aluminum foil to contain the melting of the PMMA slab over the course of the experiment. The sample was backed by 12 sheets of 3 mm thick Superwool XTRA Paper (per the product literature - avg density: ~200 kg/m3; Thermal conductivity 0.05 W/mK (200C), 0.08 W/mk (400C), 0.13 W/mK (600C), 0.3 W/m/K @ 1000)

No thermocouples were used in experiments 4-6. All mass was observed to be consumed. 


##### POSTPROCESSING NOTE: 
Sample Holder Mass was not tared prior to testing, thus initial mass in submitted datasets could be >1000g. All cone calorimeter mass data was thus postprocessed ("tared") such that the initial mass, m0_exp, was determined (5s average when readings were first steady) and the difference (m_diff = m0_exp - m0) between this value and the reported initial mass of the sample (m0) was calculated. ALL reported mass values where then reduced by m_diff.

HRR was reported in units of [kW]. All cone calorimeter HRR data was thus scaled by initial sample surface area (i.e., 1/ (95 x 95 mm)) to report HRR per unit area [kW/m2]


#### Experimental Conditions
* Extraction flow rate: 24L/s nominal
* Sample Surface Area: 0.009 m2 (nominal)
* Note: Samples were 10x10cm, but supported in holders that exposed a 95 x 95 mm face of the material to the heating element
* Sample holder dimensions:
    - Square pan complying with specifications of standard ISO 5660-1
    - Retainer frame: None
* Backing Insulation: For experiments 1-3: 3 mm thick Superwool brand cermaic paper on the back face of an aluminum block in contact with sample. Density ~200 kg/m3; thermal conductivity 0.05 W/m/K @ 200 C, 0.3 W/m/K @ 1000 C; specific heat capacity unknown, but estimated ~1100 J/kg/K based on similar material
For experiments 4-6: no aluminum block; only Superwool paper (12 sheets of 3 mm in total)
* Thermocouple location: For tests 1-3, a 1-mm thermocouple was placed in the aluminum block 5 mm from the surface on the block in contact with the foil (back face of the tested sample). For tests 4-6, a thermocouple was not used.
* Sample chamber doors were closed


###### Sample Mass and Test Heating Conditions  
|Test Name | Initial sample mass (g)| Heat Flux (kW/m2)| HeaterTemperature [C]| Time to ignition (s)|
|----------|:------:| :---: | :---:  | :---: |
|Edinburgh_Cone_25kW_1| 69.99 | 25 | 575 | 103 |
|Edinburgh_Cone_25kW_2 | 69.23 | 25 | 575 | 104 |
|Edinburgh_Cone_25kW_3 | 73.51 | 25 | 575 | 98  |
|Edinburgh_Cone_25kW_4 | 67.00 | 25 | 575 | 107 |
|Edinburgh_Cone_25kW_5 | 70.29 | 25 | 575 | 105 |
|Edinburgh_Cone_25kW_6 | 71.95 | 25 | 575 | 136 |
|Edinburgh_Cone_65kW_1 | 67.00 | 65 | 840 | 16  |
|Edinburgh_Cone_65kW_2 | 70.45 | 65 | 840 | 16  |
|Edinburgh_Cone_65kW_3 | 71.63 | 65 | 840 | 17  |
|Edinburgh_Cone_65kW_4 | 71.16 | 65 | 840 | 13  |
|Edinburgh_Cone_65kW_5 | 70.55 | 65 | 840 | 12  |
|Edinburgh_Cone_65kW_6 | 69.59 | 65 | 840 | 12  |
