import os
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from scipy import stats
from typing import Type
import numpy as np
import pandas as pd
import yaml
import os, sys

l1 = [1,2,3,4]
print(l1[0:-1])