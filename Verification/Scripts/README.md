## Verification Scripts to verify material property sets against analytical solutions.


Required:  Python 3.9

dynamic_tga.py

To execute the script

```

$ python dynamic_tga.py (model prediction file name) (year)
```
To find the model prediction file name look in 'Model_predictions/'.  To find the year look in '../PMMA/Material_Properties/'.

For example,
```

$ python dynamic_tga.py MaCFP_PMMA_NIST 2021
```

Output includes:

1.   Plot of temperature against both analytical solution and model prediction for mass

2.  Root mean square error in predicting mass, compared to the analytical solution

