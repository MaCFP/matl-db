For information on how to participate, please read the [Guidelines for Participation in the 2021 MaCFP Condensed Phase Workshop](https://iafss.org/wp-content/uploads/GuidelinesforParticipation_v1.3.pdf).

#### Virtual Discusion Forum
A Google Discussion Group for the MaCFP Working Group can be accessed here: [MaCFP Virtual Discussion Forum](https://groups.google.com/g/macfp-discussions/). The purpose of this forum is to facilitate data sharing and model development to improve computational predictions of thermal degradation and pyrolysis in fire


##### Information presented at the MaCFP-2 Workshop can be found on the [**GitHub Releases**](https://github.com/MaCFP/matl-db/releases) page:
[**MaCFP-2 Presentations (Waterloo, 2021)**](https://github.com/MaCFP/matl-db/releases/tag/v1.1.0)

[**Preliminary Summary of Experimental Measurements submitted to MaCFP-2**](https://github.com/MaCFP/matl-db/releases/tag/v1.0.0)

#### How to Submit Experimental Data

Experimental and Modeling Results will be submitted, stored, and made publicly available on the [MaCFP GitHub Repository](https://github.com/MaCFP/matl-db/tree/master/Non-charring/PMMA). Experimental data may be shared by submitting pull requests to this repository or by sending data via email to [Dr. Isaac Leventon](mailto:Isaac.Leventon@NIST.gov) or [Dr. Morgan Bruns](mailto:mbruns@stmarytx.edu).

###### File Format 
Experimental and Model results should be organized in simple ASCII comma-delimited files (*.csv files) with clear header names.  Note: For all submitted measurement data, please ensure that results are obtained with a data acquisition rate of 1 Hz (for bench scale measurements; e.g. cone calorimeter) and 2 K^-1 (for mg-scale experiments; e.g. TGA). Examples of how to format data submissions, which may be used as templates, are included [here](https://github.com/MaCFP/matl-db/tree/master/Non-charring/PMMA).

###### File Naming
For simplicity, please collect your files in a single folder with your INSTITUTE name [INSTITUTE]. Please save measurement results with a name indicating your INSTITUTE, the experimental apparatus used, test conditions, and test repetition number. For example: INSITUTE\_TGA\_N2\_10K\_r1.csv or Institute\_ConeCalorimeter\_25kW\_r1.csv.  Gram-scale experiments (e.g., Cone, FPA, gasification) should include this external heat flux information in the file name, as indicated above; mg-scale experiments (e.g., TGA or DSC) should include heating rate and gaseous environment in the filename.

###### File Organization
Measurement data from repeated experiments should be saved and submitted as separate files, numbered sequentially (e.g.,INSITUTE\_TGA\_N2\_10K\_r1.csv and INSITUTE\_TGA\_N2\_10K\_r2.csv). 

###### File Description
Please also include a separate README file (.md) that provides a description of the test conditions of all experiments conducted and submitted (see the Measurements section of [Guidelines for Participation in the
2021 MaCFP Condensed Phase Workshop.pdf](https://iafss.org/wp-content/uploads/GuidelinesforParticipation_v1.3.pdf), for details on what information should be included in this file).   

Note, some iteration on formatting may be required before the results can be merged into the MaCFP database.
