import os
import os.path as op
import pandas as pd
import numpy as np
import statistics

# I'm concerned about grp='retro_btwn_rel', its `$grp/$trk/all_subjects_${acq}.csv` is stacked upper matrices (with NA elsewhere)
# several blocks of subjects, each block is session by session

toy_d = {'col1': [np.nan, np.nan, np.nan, np.nan],
        'col2': [1, np.nan, np.nan, np.nan],
        'col3': [2, 3, np.nan, np.nan],
        'col4': [4, 5, 6, np.nan]}
toy_df = pd.DataFrame(data=toy_d)

print(toy_df)

# copied the way that hamsi used to get the median; not include `.drop(["Unnamed: 0", "Subject"], axis=1)` here
median = toy_df.median().median()
print("calculated median = " + str(median))

actual_median = statistics.median([1,2,3,4,5,6])
print("median should be = " + str(actual_median))
