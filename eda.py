import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Param: year { Integer } 
# Param: week { Integer } 
# Param: stat { String } 
# Return: { Pandas DataFrame } - dataframe from the proper csv
def get_csv_data(year, week, stat):
    pass_df = pd.read_csv("data-"+str(year)+"/"+str(year)+"-"+stat+"-week-"+str(week)+".csv",index_col=None)
    return pass_df

# Param: year { Integer } - Year to get the stat from
# Param: start_week { Integer } - Latest week to get data from 1 -> week
# Param: end_week { Integer } - Latest week to get data from 1 -> week
# Param: stat { String } - 'passing', 'rushing', or 'receiving' stat to get data for
# Return: { Pandas DataFrame } - Holding the data from that stat over weeks 1 through n that year
def get_season_stat(year, start_week, end_week, stat):
    total_df = pd.DataFrame()
    for i in range(start_week,end_week):
        cur_df = get_csv_data(year,i,stat)
        total_df = pd.concat([total_df,cur_df],ignore_index=True).reset_index(drop=True)
    return total_df

# Param: df { Pandas DataFrame } - dataframe 
# Param: x_axis { String } - string to display the x_axis data
# Param: y_axis { String } - string to display the y_axis data
# Param: annotation { String } - string to display on each datapoint
# Return: { None } - Just display the plot
def plot_df(df,x_axis,y_axis, annotation):
    p1 = sns.regplot(data=df, x=x_axis, y=y_axis)
    for line in range(1,df.shape[0]):
        p1.text(df[x_axis].iloc[line]+0.2, df[y_axis].iloc[line], df[annotation].iloc[line], horizontalalignment='left', size='small', color='red')
    plt.show()


year = 2019
start_week = 1
end_week = 17

player = sys.argv[1]
stat_type = sys.argv[2].lower()

if stat_type == "rushing":
    stat_list = ["rush_att","rush_yds","opponent"]
elif stat_type == "passing":
    stat_list = ["pass_att", "pass_yds", "opponent"]
elif stat_type == "receiving":
    stat_list = ["targets", "rec_yds", "opponent"]


df = get_season_stat(year,start_week,end_week,stat_type)
df = df.loc[df["player"] == player]
plot_df(df[stat_list],stat_list[0],stat_list[1],stat_list[2])

