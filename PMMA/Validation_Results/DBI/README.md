Institute: Danish Institute of Fire and Security Technology (DBI)
Submission to the MaCFP3 project
Test case: NIST Gasification Apparatus
Contributors: Karlis Livkiss, Bjarne Husted, Guoxiang Zhao, Abhishek Bhargava


CFD package: Fire Dynamics Simulator version 6.7.9
Model description: 1 D model, DT=0.01, CELL_SIZE_FACTOR=0.1  

Boundary conditions: 
The convective heat transfer coefficient was set 12 W/(m^2 K). This value was based on the theoretical calculation in the natural convection and simulations of the heat transfer through the Kaowool PM Insulation boards (the test data provided by NIST). A sensitivity study was done, and it was found that the model results are highly sensitive to the choice of the convective heat transfer coefficient.
The ambient temperature was set to 25 degrees C, as provided in the validation tests description(20 – 30 degrees C was reported). A sensitivity study was done and it was found that the ambient temperature has only a minor influence to the modelling results.
The external radiant heat flux was set to be 49.3 kW/m^2 for target heat flux 50kW/m2 and 24.7 kW/m^2 for target heat flux 25kW/m^2.
The thermal conductivity at ambient temperature of the Kaowool insulation backing was set 0.03364 W/m/K (based on the DBI's measurements of the same material, as submitted in MaCFP-2). The thermal conductivity at elevated temperatures and specific heat capacity was set as provided by NIST.
The thickness of the backing insulation was set 0.0286 m, representing roughly 5 layers of backing insulation. The backing was set as BACKING='INSULATED'.

Limitations:
The epoxy layer was not considered in the simulation.

Validation and calibration of parameters:
The original input parameter data set was first compared to the validation test cases MaCFP-PMMA_Gasification_q50_Mass_R3, MaCFP-PMMA_Gasification_q50_Mass_R4 and MaCFP-PMMA_Gasification_q50_Mass_R5. 
The validity of the parameters was assessed based on the mass loss measurements, rather than from back side temperature measurements.

Non-calibrated model:
The non-calibrated model used the material properties as presented in the MaCFP-2 workshop (PMMA/Material_Properties/MaCFP_PMMA_DBI_1.json). Nevertheless, few additional parameters were added to the original parameter set, based on the available research literature. The absorption coefficient was set 2250 m^(-1) and the surface emissivity was set to 0.96. Sensitivity studies were done, and it was concluded that both of these parameters have only a minor influence to the model results. The model with the non-calibrated parameter values did not provide a satisfactory result. The model provided an adequate initial phases of the gasification. Nevertheless it significantly over-predicted the MLR, and ,as the result, it predicted the total consumption of the sample earlier compared to the test results. 

Calibrated model
The decision about the calibration was based on observations of the difference between the model and the test MLR curves. The problem with the model was the latter stages of the simulation, where the MLR was significantly overestimated. It was also observed that the heat of pyrolysis, reported by DBI was significantly lower compared to other participants of MaCFP-2 and values stated in available research literature. The heat of reaction was increased to values reported by NIST and, after that did not gave a desired magnitude to the effect, it was increased to Aalto University value of 983 kJ/kg. The change of the heat of pyrolysis to 983 kJ/kg was the only change in the parameter set. 
