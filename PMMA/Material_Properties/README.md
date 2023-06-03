## PMMA Material Properties

This folder holds calibrated pyrolysis models (i.e., material property datasets) and relevant metadata that identifies how these models were developed. These properties include:
* **Degradation Kinetics**: 
  * Pre-exponential Constant (A [s<sup>-1 </sup>])
  * Activation Energy (E [J mol<sup>-1</sup>])
  * Reaction order (n)
  * stoichiometric coefficient (?)
* **Thermodynamic Properties**: 
  * Heat capacity (c<sub>p</sub> [J kg<sup>-1 </sup> K<sup>-1 </sup>])
  * Heat of Reaction (h<sub>r</sub> [J kg<sup>-1 </sup>])
  * Density (&rho;  [kg m<sup>-3</sup>])
* **Transport Properties**: 
  * Thermal Conductivity (k [W m<sup>-1 </sup>K<sup>-1 </sup>])
  * Mass Diffusivity (D [m<sup>2 </sup>s<sup>-1</sup>])
  * Absorption Coefficient (&alpha;  [m<sup>-1</sup> or m<sup>-2 </sup>kg<sup>-1</sup>])
  * Emissivity (&epsilon; )


### PMMA Material Properties

In March 2023, the UMD Pyrolysis model (material properties defined in MaCFP\_PMMA\_UMD.json) was identified as the most 'central' or 'average' model of those currently available. That is, this model yields predictions closest (sum of square errors) to mean gasification predictions. It is suggested that this parameter set by used by modelers for initial model setup (to provide a common set of parameters for MaCFP PMMA). It is NOT implied to be the most accurate property set.

A pyrolysis model validation exercise has been identified to validate the accuracy of submitted PMMA Pyrolysis models. Further information is available online in the [Modeling Guidelines Wiki](https://github.com/MaCFP/macfp-db/wiki/MaCFP-2023-Modeling-Guidelines#additional-guidelines-for-nist-gasification-apparatus). and in the [Guidelines for Participation in the MaCFP-3 Workshop document](https://github.com/MaCFP/macfp-db/files/11416103/Guidelines_for_Participation_MaCFP3.pdf). A video presentation of these guidelines is also [available online](https://www.youtube.com/watch?v=bAFx0mYoyxw).