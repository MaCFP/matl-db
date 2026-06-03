### Contributor
Names: Mark McKinnon (FSRI) and Grayson Bellamy (UMD)
Institution: University of Maryland (MD, USA) and UL Research Institute Fire Safety Research Institute (MD, USA)

## Calibration Philosophy
Two property sets were submitted. One submitted property set (appended with '-OPT') relied primarily on an optimization scheme to simultaneously determine several properties from minimal datasets. The second set (appended with '-OPT') calibrated a model using as many directly measured properties as possible. Both properties sets used the same kinetics and thermodynamics for the thermal degradation reactions. 

### Kinetics and Energetics Determination

Thermal degradation kinetics were determined through optimization of TGA data collected in STA tests run by FSRI (3 K/min, 30K/min) and UMD (10 K/min). A multi-stage hill-climbing algorithm implemented in the julia programming language was used to maximize a goodness-of-fit metric between the experimental data and data simulated using a pyrolysis model also developed in julia (`Pyrolysis.jl'). The kinetic scheme was developed with six sequential first-order reactions: one reaction to represent moisture evaporation and five thermal degradation reactions. The definition of the goodness-of-fit metric and additional information about the optimization scheme and kinetic mechanism may be found in Ref [1]. The DM model was constructed using FDS (FDS-6.10.1-2293-g562ab9e-nightly) and neglected the moisture evaporation step of the kinetic scheme. 

Temperature-dependent specific heat capacities of the virgin material were determined through linear least-squares fitting of directly measured specific heat capacities (HFM from 25 C to 45 C and apparent specific heat capacity from STA from approximately 150 C to 185 C (10K/min DSC data from UMD and FSRI)) with a linear interpolation between these ranges. Char heat capacity was determined according to a fit of the DSC data from STA experiments at 10K/min collected at temperatures above the offset of decomposition. 

OPT model
Intermediate species heat capacities were fit to the apparent specific heat capacity according to cp_int_i(T) = (1 - p_i) * cp_virgin(T) + p_i * cp_char(T) on the STA segment only, with cumulative-yield progress p = [0.10105, 0.33224, 0.85066, 0.92302]. Char and Ash were defined to share the same linear form. Moisture specific heat capacity taken from the NIST Chemistry Webbook [2].

DM model
First two intermediate species were assumed to have the same temperature-dependence as the virgin material and final two intermediates were assumed to have the heat capacity of the char component. 

Heats of reaction were determined through an optimization scheme which targeted the DSC data with a heating rate of 10 K/min. The sensible heat baseline corresponded to the heat capacities from the OPT model. The OPT model also incorporated a state-dependent heat of sorption function that relies on temperature and moisture content.

### Thermo-physical Properties

A mean density of the dried virgin component was determined from direct mass and volume measurements of regular shaped samples. The density of solid products of decomposition were determined from a combination of TGA and dilatometry data (both at 10K/min) for both models. The mass fraction from TGA and the relative change in length (dL/L0) were used to determine a density multiplier as a function of temperature. There is a minor discrepancy in the models between density of intermediates because these are impossible to isolate and are produced and consumed over a temperature range. The OPT model favored the density of intermediates toward the lower end of the temperature ranges where they existed and the DM model favored density toward the temperature at which the peak component concentration was observed.

Emissivity was defined as a heat source-dependent quantity for all components based on the FSRI integrating sphere data. The effective source temperature was back-calculated using the Stefan-Boltzmann Law assuming the target surface temperature was room temperature and estimating the view factor from the cone to the target sample material according to Ref [3]. The source was assumed to radiate as a black body with an spectral distribution defined by Wein's Law. The resulting spectral distribution was multiplied by the spectrally-resolved emissivity measurements from the integrating sphere. This process is described in detail in Ref [4]. The two models used slightly different philosophies to define the emissivity in the models:

OPT model
Virgin and char emissivites taken directly from measurements and resultant calculations. Char emissivity in the model pooled from data collected on chars from CAPA test at 40 and 60 kW/m2. Emissivities of intermediates defined through a mixture model dependent on degradation reaction progress:  epsilon_int_i(q) = epsilon_virgin(q) + (epsilon_char(q) - epsilon_virgin(q)) * p_dn_i, with downstream-progress p_dn = [0.16518, 0.21033, 0.54359, 0.69793].

DM model
Virgin adnd first intermediate assigned virgin emissivity. Second and third intermediates assigned spectral emissivity of char remaining in CAPA tests at 20 kW/m2. Fourth intermediate, char, and ash at 10 kW/m2 and 30 kW/m2 assigned emissivity of char from CAPA test at 20 kW/m2, Fourth intermediate, char, and ash at 60 kW/m2 assigned emissivity of char from CAPA test at 60 kW/m2. Assumptions about surface emissivity of intermediates were based on visual observations about the evolution of the appearance of the sample in CAPA experiments. 

For both models, the absorption coefficient was assumed to be sufficiently high that all radiation was absorbed at the boundary. This assumption is based on past measurements of infrared transmission through both virgin wood samples and char samples using an integrating sphere.

OPT model
Thermal conductivity was determined for all solid and gaseous components as well as moisture through an inverse analysis optimization scheme with all other parameters defined in the pyrolysis model for the OPT model. This scheme used back surface temperature data collected at UMD in CAPA experiments conducted at 30, 50, and 70 kW/m2 as the target data.

DM model
Thermal conductivity was determined for all solid components using a combination of LFA, TGA, and DSC data. LFA data were corrected for thermal expansion/thickness changes over the tested temperature range using dilatometry data collected at 10K/min. Apparent specific heat capacities from DSC data at 10K/min and temperature-dependent density data were used in conjunction with LFA-determined thermal diffusivities to calculated thermal conductivities. All data were determined from virgin material samples taken through a minimum temperature range of 25-600 C. The calculated thermal conductivity at 200 C appears to be an outlier and did not fit the trend of the data, so it was not included in the tabular temperature-dependent thermal conductivity definition. Conductivity between each individual point was assumed to follow a linear interpolation. Conductivities above and below the upper and lower bounds were assumed to be constant at the values at the limit.

### References

[1] Bellamy, et al. Thermal decomposition models for wood: Comparing parallel and sequential reaction schemes for fire modeling applications. Applications in Energy and Combustion Science. 2026. https://doi.org/10.1016/j.jaecs.2026.100500

[2] https://webbook.nist.gov/cgi/cbook.cgi?ID=C7732185&Units=SI&Mask=2#Thermo-Condensed

[3] Wilson, M.T., Dlugogorski, B.Z. and Kennedy, E.M., 2003. Uniformity Of Radiant Heat Fluxes In Cone Calorimeter. Fire Safety Science 7: 815-826. doi:10.3801/IAFSS.FSS.7-815

[4] McKinnon MB, Bellamy GT. Fire Safety Research Institute Materials and Products database—A resource to support fire modeling. Journal of Fire Sciences. 2024;42(3):175-216. doi:10.1177/07349041241235566
  
