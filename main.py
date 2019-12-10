import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def get_csv_data(year, week, stat):
    pass_df = pd.read_csv("data-"+str(year)+"/"+str(year)+"-"+stat+"-week-"+str(week)+".csv",index_col=None)
    return pass_df

qb_season_data = {}
for i in range(1,16):
    df = get_csv_data(2018,i,"passing")
    if i==1:
        fig, ax = df.plot(x='pass_yds',y='pass_hurried', style='o')
        ax.annotate("i",df[['pass_yds', 'pass_hurried']])
        plt.show()
    qb_season_data[i] = df.loc[df["player"] == sys.argv[1]]

for k, v in qb_season_data.items():
    print(v[["player", "pass_yds", "pass_sacked","pass_blitzed","pass_hurried","pass_hits"]])
