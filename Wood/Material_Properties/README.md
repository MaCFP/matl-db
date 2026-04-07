## `MaCFP-Wood' Material Properties

This folder holds calibrated pyrolysis models (i.e., material property datasets) and relevant metadata that identifies how these models were developed. These properties include:
* **Degradation Kinetics**: 
  * Pre-exponential Constant (A [s<sup>-1 </sup>])
  * Activation Energy (E [J mol<sup>-1</sup>])
  * Reaction order (n)
  * Stoichiometric coefficient (?)
* **Thermodynamic Properties**: 
  * Heat capacity (c<sub>p</sub> [J kg<sup>-1 </sup> K<sup>-1 </sup>])
  * Heat of Reaction (h<sub>r</sub> [J kg<sup>-1 </sup>])
  * Density (&rho;  [kg m<sup>-3</sup>])
  * Heat of Combustion (&Delta;H<sub>c</sub> [kJ g<sup>-1 </sup>])
* **Transport Properties**: 
  * Thermal Conductivity (k [W m<sup>-1 </sup>K<sup>-1 </sup>])
  * Mass Diffusivity (D [m<sup>2 </sup>s<sup>-1</sup>])
  * Absorption Coefficient (&alpha;  [m<sup>-1</sup> or m<sup>-2 </sup>kg<sup>-1</sup>])
  * Emissivity (&epsilon; )


### Pyrolysis model calibration (MaCFP-4, 2026)

A pyrolysis model calibration exercise was organized to develop material property sets that accurately reproduce the anaerobic pyrolysis of `MaCFP Wood'. Oxidation of this same wood will be studied in detail at MaCFP-5 and beyond.

Modelers are asked to:
1. Calibrate (material property sets)[https://github.com/MaCFP/matl-db/tree/master/Wood/Material_Properties] to describe the anaerobic pyrolysis and char formation of this material.
2. Prepare [computational results for model-to-model comparison](https://github.com/MaCFP/matl-db/tree/master/Wood/Calibration_Results) (i.e., prediction of idealized 0D and 1D material decomposition scenarios)

#### Calibration Approach
Modelers are not provided limitations or suggestions regarding their pyrolysis model parameterization (i.e., calibration) approach; however, they are required to use either (a) at least one of the milligram-scale datasets (e.g., TGA or DSC) and one gram-scale experiment (e.g., cone calorimetry or controlled atmosphere gasification experiments), or (b) at least two of the gram-scale experiments available in the [Calibration Data](https://github.com/MaCFP/matl-db/tree/master/Wood/Calibration_Data) section of the MaCFP repository. Modelers can supplement MaCFP data with any literature data that they deem necessary (please be sure to cite any and all appropriate references, including those for measurement data found on the MaCFP Repo).

#### How to Property sets
When submitting property sets, modelers are asked to provide a detailed description (README.md) of:
* The method of determination of each of these parameters (written) 
* Decomposition reaction mechanism (written and mathematical)
* Temperature-dependent properties (written and mathematical)


A report summarizing these experimental results and Guidelines for particiation in this calibration exercise are availabe on the [Releases Page](https://github.com/MaCFP/matl-db/releases/tag/v4.0.0).