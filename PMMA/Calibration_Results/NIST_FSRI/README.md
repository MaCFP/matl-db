# NIST_FSRI Calibration Results

This folder holds results of NIST_FSRI efforts on modeling the PMMA gasification tests.

## Notes on Modeling

* The constant specific heat value reported for the insulation was replaced (in advance of performing any simulations) with a temperature depdendent curve. This curve was generated using the reported composition of Kaowoll PM (44 % Al2O3 and 56 % SiO2) and specific heat data from the NIST Webbook.

* The black painted insulation only test, using the reported time-dependence of the heat flux, was used to calibrate the heat transfer coefficient in the gasification device. FDS simulations of the Kaowoll PM and Al backplate were performed using the default FDS method for determining the heat transfer coefficient followed by fixing the value at 10 and 20 W/m/K. A linear fit of h and the predicted end temperatures at each TC location was used to determine the h that would result in the measured temperature. For the three TC locations, these values were 13.2, 13.1, and 13.8 W/m/K and h. For PMMA simulations h was set to 13 W/m/K.

* For the gasification tests, the adhesive used to bond the PMMA disc to the Kaowoll was combustible. IN modeling, the reported mass of adhesive was treated as PMMA. For example,  if the PMMA sample was 25 g and 1 g of adhesive was used, then the sample thickness was increased by 4 % to account for the adhesive mass. As was done in the experiments, the reported FDS mass output was tared to the PMMA sample mass.

## Folder Structure

### Sensitivity

The data in this folder examine the sensitivity of the results to level of detail of the gasification tests included in the FDS input. In a typical use case, an FDS user attempting to use cone type data would likely only know the nominal flux for the test and not any spatial or temporal dependence in that flux. Additionally, each property dataset reports a density; however, each gasification test also results in a density based on the reported disc diameter, thickness, and mass. Two sets of sensitivity runs were made.

#### Set 1

The first set looks at the impact on predicting the mass loss rate. It uses the 50 kW/m2 R3 test. The sensitivities include:

* simple: Setting EXTERNAL_FLUX=50 with no time or spatial dependence using the NIST property set density (i.e., the reported gasification density was adjusted to preserve mass).
* simple_rho: Setting EXTERNAL_FLUX=50 with no time or spatial dependence using density based on the reported dimensions and mass for the gasification test.
* fluxT: The simple case plus RAMP_Q to ramp the EXTERNAL_FLUX using the reported time dependence.
* fluxR: The simple case where 5 VENT inputs were used for the PMMA sample. Each VENT represented an equal area ring segment of the disc (ring segments between 0, SQRT(0.2) r, SQRT(0.4) r, etc.). The EXTERNAL_FLUX was set to the average flux over that ring using the reported radial data
* full: Both fluxT and fluxR
* full_rho: Using the gasification test derived density.

Results show that the times to reach 0 mass varied by 12 s out of times that were approximately 420 s or 3 %. The density assumption resulted in 1 to 2 s change or < 0.5 %.

#### Set 2

The second set looks at the impact on predicting the end temperature. Based on the first set results only the simple and full approaches were used with the 50 kW/m2 T1 test. Prior to burnout the difference in temperatures over time was under 7 K.

#### Conclusion

Based on the sensitivity study, the full set of gasification experiments was run using the simple approach.

### NIST_Props

This folder contains predictions for all the PMMA gasification experiments.

### All_Props

This folder contains predictions for all other property sets whose json files contain a full set of properties (kinetics plus rho, c, k) using the 50 kW/m2 R3 test. This set of results contributed to provide insights on possible user/modeling tool effects.