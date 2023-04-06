# 
# KFB @ ESENSI (SNC Turkey), Ankara, TR
# 23 March 2023
# 
# Created for inspecting the acceleration data
# which requires two inputs
# (1) path of the excel file
# (2) start and stop frequency of the fft inspection range
# 
# Created right after the maiden flight of GöKHUN VTOL (22-March-2023)

import pandas as pd
import openpyxl as op
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from scipy.fft import fft, fftfreq
import numpy as np
import xlrd # pip install xlrd==1.2.0 <- use this version for xlsx file types!!!
import time as t

# INPUTS
# 
# Select the file to be analyzed ################################################################# (1)
filePath = "E:/BODY_VIBRATION_TEST/data/rpm_scan_2_6.xlsx"    # win path '/'
# Select the focused frequency range for fft inspection ########################################## (2)
x_start = 0                                                 # in Hz
x_stop = 400                                                # in Hz

# PROGRAM
#z
totalTime = 0
start = t.time()

# Load the data from the Excel file into a Pandas dataframe
# df = pd.read_excel('path/to/your/file.xlsx', sheet_name='Data1', header=2)
wb = xlrd.open_workbook(filePath, on_demand=True)
numberSheets = wb.nsheets # or wb.nsheets

end = t.time()
print('Time taken for gathering sheet number of excel: ', end - start)
totalTime += end-start
start = t.time()

df = pd.read_excel(filePath, sheet_name=2, header=1)

end = t.time()
print('Time taken for loading excel to the dataframe: ', end - start)
totalTime += end-start
start = t.time()

# Extract the time, acc1, and acc2 data from the dataframe
time = df.iloc[:,0]

acc1uav = df.iloc[:,1]
acc2uav = df.iloc[:,2]
acc3uav = df.iloc[:,3]

acc1avf = df.iloc[:,4]
acc2avf = df.iloc[:,5]
acc3avf = df.iloc[:,6]

end = t.time()
print('Time taken for loading first page: ', end - start)
totalTime += end-start
start = t.time()

for sheetNumber in range(3, numberSheets):
    df_new = pd.read_excel(filePath, sheet_name=sheetNumber, header=1)

    time_new = df_new.iloc[:,0]

    acc1uav_new = df_new.iloc[:,1]
    acc2uav_new = df_new.iloc[:,2]
    acc3uav_new = df_new.iloc[:,3]

    acc1avf_new = df_new.iloc[:,4]
    acc2avf_new = df_new.iloc[:,5]
    acc3avf_new = df_new.iloc[:,6]

    time = np.append(time, time_new)

    acc1uav = np.append(acc1uav, acc1uav_new)
    acc2uav = np.append(acc2uav, acc2uav_new)
    acc3uav = np.append(acc3uav, acc3uav_new)

    acc1avf = np.append(acc1avf, acc1avf_new)
    acc2avf = np.append(acc2avf, acc2avf_new)
    acc3avf = np.append(acc3avf, acc3avf_new)

    end = t.time()
    print('Time taken for loading next page: ', end - start)
    totalTime += end-start
    start = t.time()

# collect time with starting from 0.0 seconds and increasing with sampling rate
time = np.round(time - time[0], 4)

# Create a figure with two by three subplots
# colors_list = list(colors.cnames)

# firstColor = "xkcd:red"
# secondColor = "xkcd:green"
# thirdColor = "xkcd:blue"

# firstColor = "#FF0000" # red
# secondColor = "#00FF00" # green
# thirdColor = "#0000FF" # blue

firstColor = "xkcd:red" # red
secondColor = "xkcd:green" # green
thirdColor = "xkcd:blue" # blue

fourthColor = "xkcd:orange" # red 2
fifthColor = "xkcd:lime" # green 2
sixthColor = "xkcd:cyan" # blue 2

lineWidth = 1

fig1, ((uavX, uavY, uavZ), (avfX, avfY, avfZ)) = plt.subplots(2, 3)

# Plot the time vs acc1 data on the first subplot
uavX.plot(time, acc1uav, firstColor, linewidth=lineWidth)
uavX.set_xlabel('Time (s)')
uavX.set_ylabel('UAV +X (amplitude)')
uavX.set_title('Time vs UAV +X')

uavY.plot(time, acc2uav, secondColor, linewidth=lineWidth)
uavY.set_xlabel('Time (s)')
uavY.set_ylabel('UAV +Y (amplitude)')
uavY.set_title('Time vs UAV +Y')

uavZ.plot(time, acc3uav, thirdColor, linewidth=lineWidth)
uavZ.set_xlabel('Time (s)')
uavZ.set_ylabel('UAV +Z (amplitude)')
uavZ.set_title('Time vs UAV +Z')

# Plot the time vs acc2 data on the second subplot
avfX.plot(time, acc1avf, fourthColor, linewidth=lineWidth)
avfX.set_xlabel('Time (s)')
avfX.set_ylabel('AV FR +X (amplitude)')
avfX.set_title('Time vs AV FR +X')

avfY.plot(time, acc2avf, fifthColor, linewidth=lineWidth)
avfY.set_xlabel('Time (s)')
avfY.set_ylabel('AV FR +Y (amplitude)')
avfY.set_title('Time vs AV FR +Y')

avfZ.plot(time, acc3avf, sixthColor, linewidth=lineWidth)
avfZ.set_xlabel('Time (s)')
avfZ.set_ylabel('AV FR +Z (amplitude)')
avfZ.set_title('Time vs AV FR +Z')

end = t.time()
print('Time taken plotting the Acc data: ', end - start)
totalTime += end-start
start = t.time()

N = time.size
F = 5000.0
T = 1.0 / F
fftHz = fftfreq(N, T)[0:N//2]

fftAcc1 = abs(fft(acc1uav.values))[0:N//2]
fftAcc2 = abs(fft(acc2uav.values))[0:N//2]
fftAcc3 = abs(fft(acc3uav.values))[0:N//2]

fftAcc1avf = abs(fft(acc1avf.values))[0:N//2]
fftAcc2avf = abs(fft(acc2avf.values))[0:N//2]
fftAcc3avf = abs(fft(acc3avf.values))[0:N//2]

end = t.time()
print('Time taken for taking the FFT of the Acc data: ', end - start)
totalTime += end-start
start = t.time()

fig2, ((fuavX, fuavY, fuavZ), (favfX, favfY, favfZ)) = plt.subplots(2, 3)
fuavX.plot(fftHz, fftAcc1, firstColor, linewidth=lineWidth)
fuavX.set_xlabel('Hz')
fuavX.set_ylabel('amplitude')
fuavX.set_title('Frequency vs fft UAV +X')
fuavX.set_xlim([x_start, x_stop])

fuavY.plot(fftHz, fftAcc2, secondColor, linewidth=lineWidth)
fuavY.set_xlabel('Hz')
fuavY.set_ylabel('amplitude')
fuavY.set_title('Frequency vs fft UAV +Y')
fuavY.set_xlim([x_start, x_stop])

fuavZ.plot(fftHz, fftAcc3, thirdColor, linewidth=lineWidth)
fuavZ.set_xlabel('Hz')
fuavZ.set_ylabel('amplitude')
fuavZ.set_title('Frequency vs fft UAV +Z')
fuavZ.set_xlim([x_start, x_stop])

favfX.plot(fftHz, fftAcc1avf, fourthColor, linewidth=lineWidth)
favfX.set_xlabel('Hz')
favfX.set_ylabel('amplitude')
favfX.set_title('Frequency vs fft AV FR +X')
favfX.set_xlim([x_start, x_stop])

favfY.plot(fftHz, fftAcc2avf, fifthColor, linewidth=lineWidth)
favfY.set_xlabel('Hz')
favfY.set_ylabel('amplitude')
favfY.set_title('Frequency vs fft AV FR +Y')
favfY.set_xlim([x_start, x_stop])

favfZ.plot(fftHz, fftAcc3avf, sixthColor, linewidth=lineWidth)
favfZ.set_xlabel('Hz')
favfZ.set_ylabel('amplitude')
favfZ.set_title('Frequency vs fft AV FR +Z')
favfZ.set_xlim([x_start, x_stop])

end = t.time()
print('Time taken for plotting the FFT data: ', end - start)
totalTime += end-start
print('Total Run Time: ', totalTime)

fig3 = plt.figure()
fX = fig3.add_subplot(311)
linesfX1 = fX.plot(fftHz, fftAcc1, "xkcd:orange", label="UAV", linewidth=lineWidth * 2)
linesfX2 = fX.plot(fftHz, fftAcc1avf, "xkcd:blue", label="AV FR", linewidth=lineWidth)
fX.set_ylabel("amplitude")
fX.set_title("fft X Direction")
fX.set_xlim([x_start, x_stop])
fX.legend()
fX.grid()

fY = fig3.add_subplot(312)
linesfY1 = fY.plot(fftHz, fftAcc2, "xkcd:orange", label="UAV", linewidth=lineWidth * 2)
linesfY2 = fY.plot(fftHz, fftAcc2avf, "xkcd:blue", label="AV FR", linewidth=lineWidth)
fY.set_title("fft Y Direction")
fY.set_xlim([x_start, x_stop])
fY.legend()
fY.grid()

fZ = fig3.add_subplot(313)
linesfZ1 = fZ.plot(fftHz, fftAcc3, "xkcd:orange", label="UAV", linewidth=lineWidth * 2)
linesfZ2 = fZ.plot(fftHz, fftAcc3avf, "xkcd:blue", label="AV FR", linewidth=lineWidth)
fZ.set_xlabel("Hz")
fZ.set_title("fft Z Direction")
fZ.set_xlim([x_start, x_stop])
fZ.legend()
fZ.grid()

# Show the plot
plt.show()
