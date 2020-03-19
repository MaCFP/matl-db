# Dansk Brand og Sikringsteknisk Institut, Lund University (DBI_Lund)

A concise description of the tests done by the division of fire safety engineering at Lund University (Sweden) and DBI (Denmark), is presented here. For more information regarding specific tests please contact: Karlis Livkiss kal@dbigroup.dk

### Experimental Conditions, TGA
A Netzsch  STA 449 F3 Jupiter was used to conduct Simultaneous Thermal Analysis (TGA + DSC) experiments. STA experiments performed in Nitrogen at a heating rate of 20 K/min. Although tests were conducted simultaneously, TGA and DSC measurement data presented here are separated into two files, for consistency with other datasets.

* Heating Rate: 20 K/min
* Temperature program
  - Initial temperature 298.15 K
  - Isotherm: None
  - Maximum Temperature 1223.15 K
  - Final Isotherm: None
* Sample mass: 4.9-5.8 mg
* Sample geometry: powdered
* Calibration type: Indium for temperature and heat sensitivity
* Crucible type: Alumina, 85uL
* Carrier Gas
  - Nitrogen
  - Flow rate = [?] ml/min
 
| Test Name | Heating Rate [K/min] |  Initial Sample Mass [mg] | 
| --------- | :----: | :------------------------:|
|DBI_Lund\_STA\_N2\_20K\_1 |  20  | 5.8|  
|DBI_Lund\_STA\_N2\_20K\_2 |  20  | 4.9|  
|DBI_Lund\_STA\_N2\_20K\_3 |  20  | 5.5|  

### Experimental Conditions, Gasification Tests
Slab gasification tests were performed in a controlled atmosphere cone calorimeter at the Lund University division of fire safety engineering using a cone calorimeter made by Fire Testing Technology. An enclosed compartment is added to the test setup for controlling the atmospheric environment around the test sample. The oxygen level inside the compartment is measured with O2 analyser PMA 10 by M&C.

* Extraction flow rate: 24L/s
* Sample Surface Area: 0.01 m2 (nominal)
* Sample holder dimensions:
    - Square pan: 106mm x 106mm x 25mm [?]
    - Retainer frame: None
    - Retaining grid: None
* Backing Insulation:  Morgan Thermal Ceramics Superwool SW Plus was used as the backing material (Density 64 kg/m3, thickness 13 mm; thermal conductivity: see end of README, ~0.0375 [W/(m-K)])
* Thermocouple location: None

###### Test Heating Conditions  
|Test Name | Heat Flux [kW/m2]| Avg Heater Temperature [K]| O2 vol %|
|----------|:------:| :---: |:---: |
|DBILund\_Gasification\_25kW\_1 | 25| 913| 2.5-3.4 | 
|DBILund\_Gasification\_25kW\_2 | 25| 913| 3.5-4.0|
|DBILund\_Gasification\_25kW\_3 | 25| 913| 2.2-3.3|
|DBILund\_Gasification\_50kW\_1 | 50| 1093| 2.2-3.0|
|DBILund\_Gasification\_50kW\_2 | 50| 1093| 2.4-3.2|

It must be noted that the heater temperature may not be regarded as a ‘real’ temperature of the heater. It is a reference value for maintaining and controlling the heat flux. It should be assumed that the thermocouples on the heater coil are not fixed properly.

###### Test Calibration 
Heater calibration was performed before setting up a new irradiance level in accordance with ISO 5660-1:2019 section 10.2.5.  Operating analyser calibration zeroed with nitrogen and adjusted for a response of 20.95 % ± 0.01 % with dried ambient air (ISO-1:2019 5660 section 10.2.3). The distance from the conical heater to the specimen surface is set 25 mm in the start of the day.



###### Sample Preparation 
PMMA specimens were weighed and measured, then wrapped (bottom and sides) in aluminium foil, and placed on top of a 13 mm thick layer of Morgan Thermal Ceramics Superwool SW Plus (Density 64 kg/m3; nominally 100 x 100 mm square). 

|Test Name | Initial Sample Mass [g]| Sample Thickness [mm]| Final Sample mass [g]
|:----------:|:------:|:---: |:---: 
|DBILund\_Gasification\_25kW\_1 | 69.1|5.85|0.7|
|DBILund\_Gasification\_25kW\_2 | 73.8|6.24|0.4|
|DBILund\_Gasification\_25kW\_3 | 70.1|5.92|0.1|
|DBILund\_Gasification\_50kW\_1 | 68.6|5.78|0|
|DBILund\_Gasification\_50kW\_2 | 67.7|5.71|0|

###### Test Procedure
1) Test calibrations are performed as described above
2) The load cell is set to an arbitrary level for ensuring that it in the measurement range. As a result the mass in raw data files does not correspond to the specimen nor to the prepared test specimen, but is rather an arbitrary mass fitting the measurement range of the equipment
3) A baseline is done with the atmosphere controlling camber opened
4) The chamber is closed and the Nitrogen flow in the chamber is started. 0.85 l/s is performed until the oxygen level stabilise. Typically it was around 3 – 3.5 %
5) A second baseline is performed for 60 seconds. The start time of the second baseline is written in comments section after the test
6) The shield covering the conical heater is closed. The specimen is placed inside the chamber. This action requires opening the chamber and the atmosphere inside the chamber is with oxygen
7) 90 seconds are taken before starting the test to ensure that the atmosphere inside the chamber stabilizes (Measured irradiance to the specimen surface while the shield is closed are provided below
8) The shield is opened and the test is started
9) After the test, the remains of the PMMA and the aluminium are weighed
easured Irradiance to the specimen with a closed shield

|Time [s]|Irradiance, cone set to 25 kW/m2|Irradiance, cone set to 65 kW/m2|
|---|:---: |:---:|
|0|24.7|50.2|
|10|3.9|9.1|
|20|3.8|8.8|
|30|3.7|8.7|
|40|3.7|8.6|
|50|3.7|8.6|
|60|3.7|8.6|
|70|3.7|8.7|
|80|3.7|8.6|
|90|3.7|8.7|

Sample masses reported in .csv files indicate that the specimen mass dropped below 0 at the end of the test. This can be interpreted considering the test procedure and the test data managing and is most likely suggested to be due to the:
1) Scale accuracy when exposed to heat in the chamber
2) Combustion of the organic content from the backing insulation
3) Moisture loss from the backing insulation.



### Experimental Conditions, Cone calorimeter
Cone calorimeter tests were performed at DBI during November and December of 2019. The cone calorimeter iCone is made by Fire Testing Technology. Square and round samples of PMMA were tested. Back surface temperature was measured during during the first experiment in each test series (i.e., for each sample shape and incident heat flux) using a single thermocouple at the center of the sample's back surface.  A k-type thermocouple was used. "The wires were soldered to for a small bead and taped with small piece of aluminium tape to the back side of the test specimen."
For cone calorimeter tests, time-resolved cone heater temperature and sample-surface-area-normalized HRR are available but not currently provided, to ensure formatting consistency with other datasets.


* Extraction flow rate: 24L/s
* Sample holder dimensions:
    - Square pan: 106mm x 106mm x 25mm [?]
    - Retainer frame: None
    - Retaining grid: None
* Backing Insulation:  Described below (varies for square vs. round samples)
* Thermocouple location: Central on sample back surface
    
###### Test Heating Conditions  

|Test Name | Heat Flux [kW/m2]| Avg Heater Temperature [K]| Sample Shape |
|----------|:------:| :---: | :---: |
|DBILund\_Cone\_25kW\_1 | 25| 1147.5| Square | 
|DBILund\_Cone\_25kW\_2 | 25| 1147.5| Square |
|DBILund\_Cone\_25kW\_3 | 25| 1147.4| Square |
|DBILund\_Cone\_25kW\_4 | 25| 1144.5| Round  |
|DBILund\_Cone\_25kW\_5 | 25| 1144.3| Round  |
|DBILund\_Cone\_25kW\_6 | 25| 1144.5| Round  |
|DBILund\_Cone\_50kW\_1 | 50| 1329.4| Square |
|DBILund\_Cone\_50kW\_2 | 50| 1329.4| Square |
|DBILund\_Cone\_50kW\_3 | 50| 1329.4| Square |
|DBILund\_Cone\_65kW\_1 | 65| 1405.3| Square |
|DBILund\_Cone\_65kW\_2 | 65| 1405.4| Square |
|DBILund\_Cone\_65kW\_3 | 65| 1405.4| Square |


###### Sample Preparation 
Square PMMA specimens were weighed and measured, then wrapped (bottom and sides) in aluminium foil, and placed on top of two 13 mm thick layers of Morgan Thermal Ceramics Superwool SW Plus (Density 64 kg/m3; nominally 100 x 100 mm square). 

Round PMMA samples were approximately 7 cm in diameter. A standard sample holder with no edge frame was used. One layer of 3 mm insulfrax ’paper’ insulation was placed at the bottom of the sample holder and one layer of Morgan Thermal Ceramics 13mm was placed in the sample holder. Round PMMA samples were placed inside of two layers of 3 mm thick Insulfrax insulation paper and wrapped in an aluminium foil. Wrapped samples were then placed on the top of the Morgan thermal Ceramics insulation.

|Test Name | Initial Sample Mass [g]| Sample Thickness [mm]|Sample Surface Area [m2]|
|:----------:|:------:|:---:|:--:|
|DBILund\_Cone\_25kW\_1 | 72.96|6.16|0.01002|
|DBILund\_Cone\_25kW\_2 | 73.21|6.17|0.01003|
|DBILund\_Cone\_25kW\_3 | 72.24|6.08|0.01002|
|DBILund\_Cone\_25kW\_4 | 27.24|-   |0.00388|
|DBILund\_Cone\_25kW\_5 | 27.52|6.04|0.00385|
|DBILund\_Cone\_25kW\_6 | 27.42|5.99|0.00388|
|DBILund\_Cone\_50kW\_1 | 73.92|6.24|0.01002|
|DBILund\_Cone\_50kW\_2 | 73.75|6.25|0.01002|
|DBILund\_Cone\_50kW\_3 | 72.42|6.14|0.01003|
|DBILund\_Cone\_65kW\_1 | 73.31|6.18|0.01002|
|DBILund\_Cone\_65kW\_2 | 73.86|6.23|0.01003|
|DBILund\_Cone\_65kW\_3 | 73.03|6.16|0.01002|

### Thermal Conductivity
The thermal conductivities of PMMA and  Morgan Thermal Ceramics Super wool plus were measured using a Netzsch HFM 446 Medium.
|PMMA Temp [C]| Thermal Conductivity [W/(m-K)]|Insulation Temp [C]| Thermal Conductivity [W/(m-K)]|
|:-:|:-:|:-:|:-:|
|19.9|0.17331|25.0|0.03364|
|24.9|0.17384|30.0|0.03437|
|29.8|0.17402|35.0|0.03520|
|34.7|0.17448|40.0|0.03618|
|39.6|0.17609|45.0|0.03721|
|44.6|0.17784|50.0|0.03795|
|49.5|0.17862|55.5|0.03854|
|54.4|0.17821|60.0|0.03920|
|59.3|0.17775|65.0|0.04003|
|64.2|0.17770|70.0|0.04088|

