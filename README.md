# A Geometrical Analysis of Bike Sharing Usage


## Intro

Please refer to https://bike-sharing-prediction.herokuapp.com.

## Dependency

scikit-learn, googlemaps

## Description

You will need a google maps geocoding API key, which will be used to get coordinates based on addresses.

```python
import bspred
from bspred import compound_estimator
import numpy as np
import pandas as pd

key = ""

addresses = ['41 E 11th St']

df = bspred.predict(addresses, key)
```

A quick visualization by using bokeh :

```python
p = bspred.plot_with_new(df)
show(p)
```

