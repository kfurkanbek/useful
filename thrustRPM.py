# 
# KFB @ ESENSI (SNC Turkey), Ankara, TR
# 31 March 2023
# 
# Created for inspecting the thrust data
# which requires one inputs
# (1) path of the txt file

import time as t
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors

# INPUTS
# 
# Select the file to be analyzed ################################################################# (1)
filePath = 'C:/Users/Public/Documents/Dewesoft/Exports/at_high_1_bat_step_4.txt'    # win path '/'

# PROGRAM
#
totalTime = 0
start = t.time()

# Read the sample rate information from the 5th row
with open(filePath, 'r') as f:
    sampleRateRow = f.readlines()[4]
    sampleRate = float(sampleRateRow.split(": ")[1].strip())

pwmWidth = 0.002 # 2 ms

# Load the data into a Pandas DataFrame, skipping the first 10 rows
data = pd.read_csv(filePath, sep='\t', skiprows=9)

# Find the index where the 4th value passes the 4.9 limit first time
# Slice the rows
data = data.loc[data[data['AI 8 PWM (V)'] > 4.9].index[0]:]

# Get the title row
title_row = pd.read_csv(filePath, sep="\t", nrows=1, skiprows=9, header=None)

# Create a new column with time values in seconds
data['Time (s)'] = pd.Series(data.index / sampleRate)

# Print the first few rows of the data to check that it loaded correctly
# print(data.head())

end = t.time()
print('Time taken for reading the txt file: ', end - start)
totalTime += end-start
start = t.time()

# Calculate the mean of columns with 400 data intervals and store in new DataFrame
mean_df = pd.DataFrame()
for col in data.columns:
    col_data = data[col]
    col_mean = col_data.groupby(col_data.index // (pwmWidth*sampleRate)).mean()
    mean_df[col] = col_mean

# Find the index where the value passes the limit first time
# Slice the rows
ssIndex = mean_df[mean_df['Thrust (N)'] < -40].index
startIndex = ssIndex[0]
stopIndex = ssIndex.size-1
mean_df = mean_df.loc[startIndex:stopIndex]

# Create a new column with time values in seconds
mean_df['Time (s)'] = pd.Series(mean_df.index * pwmWidth)

# Print the first few rows of the mean DataFrame to check that it worked
print(mean_df.head())

end = t.time()
print('Time taken for taking the mean of all values: ', end - start)
totalTime += end-start
start = t.time()

# throttle_list = [20, 90, 20, 90, 20, 90, 30, 80, 30, 80, 30, 80, 40, 70, 40, 70, 40, 70, 40, 50, 40, 50, 40, 50, 40, 60, 50,  60, 50, 60, 50, 70, 60, 70, 60, 70, 60]
throttle_list = [20, 90, 20, 90, 20, 90, 30, 80, 30, 80, 30, 80, 40, 70, 40, 70, 40, 70, 40, 50, 40, 50, 40, 50, 40, 60, 50,  60, 50, 60, 50, 70, 60, 70, 60, 70, 60]
time_duration = 4.999 # s
data_duration = (time_duration/pwmWidth)+20
data_offset = (1.5/pwmWidth)
N = len(throttle_list)
mean_df['Throttle %'] = mean_df['Time (s)']
for i in range(0, N, 1):
    mean_df['Throttle %'].loc[i*(data_duration)+data_offset:(i+1)*(data_duration)+data_offset] = throttle_list[i]

# Print the first few rows of the mean DataFrame to check that it worked
# print(mean_df.head())

end = t.time()
print('Time taken for creating the throttle input values: ', end - start)
totalTime += end-start
start = t.time()

# Define colors
firstColor = "xkcd:red" # red
secondColor = "xkcd:green" # green
thirdColor = "xkcd:blue" # blue

fourthColor = "xkcd:orange" # red 2
fifthColor = "xkcd:lime" # green 2
sixthColor = "xkcd:cyan" # blue 2

lineWidth = 1

plt.subplot(2,1,1)
plt.plot(mean_df['Time (s)'], ((mean_df['AI 8 PWM (V)']*20)-50)*2, label="Input PWM [%]")
# plt.plot(mean_df['Time (s)'], mean_df['Throttle %'], label="Input Throttle [%]")
plt.xlabel("Time [s]")
plt.legend()
plt.grid()

plt.subplot(2,1,2)
plt.plot(mean_df['Time (s)'], ((mean_df['AI 8 PWM (V)']*20)-50)*2, label="Input PWM [%]")
plt.plot(mean_df['Time (s)'], -mean_df['Thrust (N)'], label="Thrust [N]")
plt.xlabel("Time [s]")
plt.legend()
plt.grid()

# Create a figure with one subplots
fig1 = plt.figure()
ax11 = fig1.add_subplot(111)
ax12 = ax11.twinx()
lines11 = ax11.plot(mean_df['Time (s)'], ((mean_df['AI 8 PWM (V)']*20)-50)*2, firstColor, label="Input PWM [%]",  linewidth=lineWidth)
lines12 = ax12.plot(mean_df['Time (s)'], -mean_df['Thrust (N)'], thirdColor, label="Thrust [N]", linewidth=lineWidth)
fig1.legend()

fig2 = plt.figure()
ax21 = fig2.add_subplot(211)
ax22 = fig2.add_subplot(212)
lines21 = ax21.plot(mean_df['Time (s)'], mean_df['AI 4 Voltage (V)'], firstColor, label="Voltage (V)", linewidth=lineWidth)
lines22 = ax22.plot(mean_df['Time (s)'], mean_df['AI 5 Ampere 3 (A)'], thirdColor, label="Ampere (A)", linewidth=lineWidth)
fig2.legend()

# fig2 = plt.figure()
# ax2 = fig2.add_subplot(111)
# lines2 = ax2.plot(data['AI 8 PWM (V)'], data['Thrust (N)'], secondColor, linewidth=lineWidth)

end = t.time()
print('Time taken for plotting all the values: ', end - start)
totalTime += end-start
print('Total Run Time: ', totalTime)

plt.show()
