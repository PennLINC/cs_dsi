import os
import os.path as op
import pandas as pd
import numpy as np
import statistics

# check the correct way to compute median of a upper triangle matrix that includes np.nan

toy_d = {'col1': [np.nan, np.nan, np.nan, np.nan],
        'col2': [1, np.nan, np.nan, np.nan],
        'col3': [2, 3, np.nan, np.nan],
        'col4': [4, 5, 6, np.nan]}
toy_df = pd.DataFrame(data=toy_d)

print(toy_df)

median = toy_df.median().median()
print("calculated median = " + str(median))

actual_median = statistics.median([1,2,3,4,5,6])
print("median should be = " + str(actual_median))
