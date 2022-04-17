import numpy as np
from numpy import nan
import pandas as pd
import libs
import Dataer
df = [1,2,3,4,5,10,1,2,1,2,3,2,1]

a = Dataer.IQR_Outliers(df)
print(a)
