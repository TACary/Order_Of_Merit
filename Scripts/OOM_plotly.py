# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 17:59:50 2021

@author: Tim
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff

df = pd.read_csv(r"C:\Users\Tim\Documents\Python Scripts\OOM_results.csv")

fig = ff.create_table(df)
fig.show()
