# README File for Universidad Adolfo Ibáñez (UAI)
    Universidad Adolfo Ibáñez; Santiago, Chile.
    Please contact **[Name] (email)** for more information.

# Experimental conditions: milligram-scale thermogravimetric test
A custom thermogravimetric test setup was used to conduct mass loss experiments on mg-scale samples. The setup consisted of a vertical tubular furnace and an analytical balance, allowing continuous mass measurements during heating.

The crucible containing the sample was placed inside the furnace by means of a brass rod passing through the lower section of the tube. The position of the crucible is approximately 140 mm from the furnace bottom edge, lying at the center of the tube (along the longitudinal axis). The rod was mechanically connected to the analytical balance via a 3D support resting on the balance pan, allowing continuous mass measurements during the test.

The furnace was equipped with a top cover with a 2 mm diameter hole that restricts the outlet of the nitrogen flow. At the bottom of the furnace, a custom cover made of ceramic fiber was fabricated to allow the brass rod to pass through, while a copper tube was used to inject the nitrogen flow into the furnace.


Prior to each test, the system was flooded with nitrogen for 30 minutes. The same gas flow was maintained throughout the entire experiment. The nitrogen flow was controlled using a Bronkhorst F-201CV-10K-AAD-22-V mass flow controller operated via an E-8000 analog controller. 

The crucible was mechanically connected to the analytical balance through the brass rod and connected to the 3D part. 


**Reference: More information is available at: [J. Smith, et al., Journal Na,e, 20xx]

* Heating rate: 20 K/min
* Temperature program
    - Initial temperature: 35 - 40°C
    - Initial Isotherm: 900 s
    - Maximum temperature: 800°C
    - Final Isotherm: None
* Sample geometry: Powdered
* Calibration type: Two calibration procedures were performed:
  - **Mass calibration**: The analytical balance exhibited a time-dependent drift characterized by a gradual decrease in the measured mass. To quantify this effect, a blank experiment (no sample) was conducted under identical experimental conditions. The resulting drift curve was subtracted from the mass measured during each experiment. The drift was fitter using a third-order polynomial function of time (in minutes).
  - **Temperature calibration**: Since the tubular furnace reports the furnace wall temperature rather than the crucible temperature, a Type-K thermocouple connected to a Labjack T7-Pro data acquisition system was placed directly at the crucible location. The recorded temperature evolution was used to establish the calibration function relating the crucible temperature to the furnace temperature. The calibration curve was fitted using a third-order polynomial function of the furnace wall temperature (in °C). 
* Crucible
  - Type: AISI 304 Stainless Steel
  - Volume: ???
  - Diameter: 7.3 mm (Inner)
  - Mass: ???
  - Lid: None
  - Note: Cylindrical Geometry, 4.2 mm depth
* Carrier Gas
  - Type: Nitrogen
  - Flow rate: 1.5 L/min
  - Note: industrial grade nitrogen, "Atmosphere: Anaerobic"
* Instrument
  - Type: Custom
  - Furnace Type: Nabertherm GmbH Vertical tubular furnace (RT 50/250/11)
  - Notes: Maximum temperature: 1100°C. Inner tube diameter: 50 mm. Tube length: 360 mm
  - Balance type: Radwag Analytical balance (AS 310.R2)
  - Balance Notes: Maximum capacity: 310 g. Resolution: 0.1 mg



| Test Name | O2 volume % |  Initial Sample Mass (mg) | 
| --------- | :---------: | :------------------------: |
|UAI\_TGA\_N2\_10K\_R1 | 0 | 15|  
|UAI\_TGA\_N2\_10K\_R2 | 0 | 15|  
|UAI\_TGA\_N2\_10K\_R3 | 0 | 15|  