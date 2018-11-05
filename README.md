# Prediction of Bike Sharing Usage based on Citibike New York Data in 2018

Please download and open the html files to see the plots. The available plots demonstrate the stations with the highest Departures and Arrivals.

To install, please do:

```bash
pip install bsprediction
```

## Key Variables
Arrivals: number of trips that end at a station per day. 

Departures: number of trips that start at a station per day. 

Characteristic prediction: prediction of bike sharing usage at a specific location, given that there are no bike stations in a vicinity of the location.

## Dependency
numpy, pandas, keras

## Library Description

This is a python library in process. 

There are two kinds of prediction available. All predictions come with asymptotica 95% confidence intervals.

```python
import bsprediction 
import numpy as np
import pandas as pd

data = pd.DataFrame({
    'latitude':[40.75058535], 
    'longitude':[-73.99468482]
})
```

1. Prediction of characteristic bike sharing usage. 

Please notice that this is not the true bike sharing usage, but rather an order of magnitude analysis.

```python
bsprediction.predict(data)
```
The results will: 
Arrivals = 826.452942, Arrivals_CI = [821.8796256964637, 831.0262580925988]

2. Prediction of bike sharing usage given the current active Citibike stations.

The result will be a pandas dataframe of the predicted bike sharing usage 
