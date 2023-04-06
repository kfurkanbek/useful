# 
# KFB @ ESENSI (SNC Turkey), Ankara, TR
# 04 April 2023
# 
# Created for inspecting the throttle with RPM data
# which requires one inputs
# (1) path of the txt file for throttle
# (2) paths of the txt file for RPMs from ESC
# important note: RPM = eRPM / 26

import time as t
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from scipy.fft import fft, fftfreq

# INPUTS
# 
# Select the file to be analyzed ################################################################# (1)
throttlePath = 'E:/THROTTLE_RPM/throttle_export.txt'    # win path '/'
# Select the file to be analyzed ################################################################# (1)
escPath0 = 'E:/THROTTLE_RPM/data/esc0.csv'    # win path '/'
escPath1 = 'E:/THROTTLE_RPM/data/esc1.csv'    # win path '/'
escPath2 = 'E:/THROTTLE_RPM/data/esc2.csv'    # win path '/'
escPath3 = 'E:/THROTTLE_RPM/data/esc3.csv'    # win path '/'

# PROGRAM
#
totalTime = 0
start = t.time()

# Load the data into a Pandas DataFrame
throttle = pd.read_csv(throttlePath, sep='\t')

esc0 = pd.read_csv(escPath0, sep=',')
esc1 = pd.read_csv(escPath1, sep=',')
esc2 = pd.read_csv(escPath2, sep=',')
esc3 = pd.read_csv(escPath3, sep=',')

# Find the index where the value passes the limit first time
# Slice the rows
startIndex = throttle[throttle['throttle_2 [%]'] > 10.00].index[0]
throttleRev = throttle.loc[::-1]
stopIndex = throttleRev[throttleRev['throttle_2 [%]'] > 5.00].index[0]
throttle = throttle.loc[startIndex:stopIndex]

samplingRate = 100.00 # Hz
dt = 1.00 / samplingRate
totalSeconds = (stopIndex - startIndex+1) / samplingRate
defaultOffset = 0.00
# print(totalSeconds)

esc0['eRPM'] = esc0['eRPM']/26
esc1['eRPM'] = esc1['eRPM']/26
esc2['eRPM'] = esc2['eRPM']/26
esc3['eRPM'] = esc3['eRPM']/26

startIndex = esc0[esc0['eRPM'] > 1000.00].index[0]
escRev = esc0.loc[::-1]
stopIndex = escRev[escRev['eRPM'] > 1000.00].index[0]
esc0 = esc0.loc[startIndex:stopIndex]

startIndex = esc1[esc1['eRPM'] > 1000.00].index[0]
escRev = esc1.loc[::-1]
stopIndex = escRev[escRev['eRPM'] > 1000.00].index[0]
esc1 = esc1.loc[startIndex:stopIndex]

startIndex = esc2[esc2['eRPM'] > 1000.00].index[0]
escRev = esc2.loc[::-1]
stopIndex = escRev[escRev['eRPM'] > 1000.00].index[0]
esc2 = esc2.loc[startIndex:stopIndex]

startIndex = esc3[esc3['eRPM'] > 1000.00].index[0]
escRev = esc3.loc[::-1]
stopIndex = escRev[escRev['eRPM'] > 1000.00].index[0]
esc3 = esc3.loc[startIndex:stopIndex]

# Create a new column with time values in seconds
N = len(throttle)
throttle['Time [s]'] = throttle['throttle_0 [%]']
for i in range(0, N, 1):
    throttle['Time [s]'].values[i] = i * dt

N0 = len(esc0)
escRate0 = totalSeconds / N0
# print(N0*escRate0)
esc0['Time [s]'] = esc0["Voltage (V)"]
for i in range(0, N0, 1):
    esc0['Time [s]'].values[i] = i * escRate0 + defaultOffset

N1 = len(esc1)
escRate1 = totalSeconds / N1
# print(N1*escRate1)
esc1['Time [s]'] = esc1["Voltage (V)"]
for i in range(0, N1, 1):
    esc1['Time [s]'].values[i] = i * escRate1 + defaultOffset

N2 = len(esc2)
escRate2 = totalSeconds / N2
# print(N2*escRate2)
esc2['Time [s]'] = esc2["Voltage (V)"]
for i in range(0, N2, 1):
    esc2['Time [s]'].values[i] = i * escRate2 + defaultOffset

N3 = len(esc3)
escRate3 = totalSeconds / N3
# print(N3*escRate3)
esc3['Time [s]'] = esc3["Voltage (V)"]
for i in range(0, N3, 1):
    esc3['Time [s]'].values[i] = i * escRate3 + defaultOffset

# Print the first few rows of the mean DataFrame to check that it worked
# print(throttle.head())
# print(esc0.head())
# print(esc1.head())
# print(esc2.head())
# print(esc3.head())

#print("%.5f",esc0['Time [s]'])
# plt.subplot(1,1,1)
# plt.plot(esc0['Time [s]'])
# plt.legend()
# plt.grid()

N = len(throttle)
F = 100.0
T = 1.0 / F
fftHz = fftfreq(N, T)[0:N//2]

fftThrottle_0 = abs(fft(throttle['throttle_0 [%]'].values))[0:N//2]
fftThrottle_1 = abs(fft(throttle['throttle_1 [%]'].values))[0:N//2]
fftThrottle_2 = abs(fft(throttle['throttle_2 [%]'].values))[0:N//2]
fftThrottle_3 = abs(fft(throttle['throttle_3 [%]'].values))[0:N//2]

T0 = escRate0
T1 = escRate1
T2 = escRate2
T3 = escRate3

fftHz_0 = fftfreq(N0, T0)[0:N0//2]
fftHz_1 = fftfreq(N1, T1)[0:N1//2]
fftHz_2 = fftfreq(N2, T2)[0:N2//2]
fftHz_3 = fftfreq(N3, T3)[0:N3//2]

fftEsc_0 = abs(fft(esc0['eRPM'].values))[0:N0//2]
fftEsc_1 = abs(fft(esc1['eRPM'].values))[0:N1//2]
fftEsc_2 = abs(fft(esc2['eRPM'].values))[0:N2//2]
fftEsc_3 = abs(fft(esc3['eRPM'].values))[0:N3//2]

# ================================================================================================================

fig1 = plt.figure()
ax11 = fig1.add_subplot(211)
lines11 = ax11.plot(throttle['Time [s]'], throttle['throttle_0 [%]'], label="throttle_0 [%]")
lines12 = ax11.plot(throttle['Time [s]'], throttle['throttle_1 [%]'], label="throttle_1 [%]")
lines13 = ax11.plot(throttle['Time [s]'], throttle['throttle_2 [%]'], label="throttle_2 [%]")
lines14 = ax11.plot(throttle['Time [s]'], throttle['throttle_3 [%]'], label="throttle_3 [%]")
ax11.set_xlabel("Time [s]")
ax11.set_title("throttle [%]")
ax11.legend()
ax11.grid()

ax12 = fig1.add_subplot(212)
lines21 = ax12.plot(fftHz, fftThrottle_0, label="fft throttle_0 [amplitude]")
lines22 = ax12.plot(fftHz, fftThrottle_1, label="fft throttle_1 [amplitude]")
lines23 = ax12.plot(fftHz, fftThrottle_2, label="fft throttle_2 [amplitude]")
lines24 = ax12.plot(fftHz, fftThrottle_3, label="fft throttle_3 [amplitude]")
ax12.set_xlabel("Hz")
ax12.set_title("fft throttle [amplitude]")
ax12.legend()
ax12.grid()

# ================================================================================================================

fig3 = plt.figure()
ax31 = fig3.add_subplot(211)
lines311 = ax31.plot(esc0['Time [s]'], esc0['eRPM'], label="ESC0 [rpm]")
lines312 = ax31.plot(esc1['Time [s]'], esc1['eRPM'], label="ESC1 [rpm]")
lines313 = ax31.plot(esc2['Time [s]'], esc2['eRPM'], label="ESC2 [rpm]")
lines314 = ax31.plot(esc3['Time [s]'], esc3['eRPM'], label="ESC3 [rpm]")
ax31.set_xlabel("Time [s]")
ax31.set_title("ESC [rpm]")
ax31.legend()
ax31.grid()

ax32 = fig3.add_subplot(212)
lines321 = ax32.plot(fftHz_0, fftEsc_0, label="fft ESC0 rpm [amplitude]")
lines322 = ax32.plot(fftHz_1, fftEsc_1, label="fft ESC1 rpm [amplitude]")
lines323 = ax32.plot(fftHz_2, fftEsc_2, label="fft ESC2 rpm [amplitude]")
lines324 = ax32.plot(fftHz_3, fftEsc_3, label="fft ESC3 rpm [amplitude]")
ax32.set_xlabel("Hz")
ax32.set_title("fft ESC [Amplitude]")
ax32.legend()
ax32.grid()

# ================================================================================================================

fig2 = plt.figure()
ax211 = fig2.add_subplot(221)
ax212 = ax211.twinx()
lines211 = ax211.plot(throttle['Time [s]'], throttle['throttle_0 [%]'], "xkcd:orange", label="throttle_0 [%]")
lines212 = ax212.plot(esc0['Time [s]'], esc0['eRPM'], "xkcd:blue", label="ESC0 [rpm]")
ax211.set_xlabel("Time [s]")
ax211.set_title("ESC0 RPM and Throttle")
ax211.legend()
ax211.grid()
ax212.set_ylim(0,3600)

ax221 = fig2.add_subplot(222)
ax222 = ax221.twinx()
lines221 = ax221.plot(throttle['Time [s]'], throttle['throttle_1 [%]'], "xkcd:orange", label="throttle_1 [%]")
lines222 = ax222.plot(esc1['Time [s]'], esc1['eRPM'], "xkcd:blue", label="ESC1 [rpm]")
ax221.set_xlabel("Time [s]")
ax221.set_title("ESC1 RPM and Throttle")
ax221.legend()
ax221.grid()
ax222.set_ylim(0,3600)

ax231 = fig2.add_subplot(223)
ax232 = ax231.twinx()
lines231 = ax231.plot(throttle['Time [s]'], throttle['throttle_2 [%]'], "xkcd:orange", label="throttle_2 [%]")
lines232 = ax232.plot(esc2['Time [s]'], esc2['eRPM'], "xkcd:blue", label="ESC2 [rpm]")
ax231.set_xlabel("Time [s]")
ax231.set_title("ESC2 RPM and Throttle")
ax231.legend()
ax231.grid()
ax232.set_ylim(0,3600)

ax241 = fig2.add_subplot(224)
ax242 = ax241.twinx()
lines241 = ax241.plot(throttle['Time [s]'], throttle['throttle_3 [%]'], "xkcd:orange", label="throttle_3 [%]")
lines242 = ax242.plot(esc3['Time [s]'], esc3['eRPM'], "xkcd:blue", label="ESC3 [rpm]")
ax241.set_xlabel("Time [s]")
ax241.set_title("ESC3 RPM and Throttle")
ax241.legend()
ax241.grid()
ax242.set_ylim(0,3600)

# ================================================================================================================

fig4 = plt.figure()
ax411 = fig4.add_subplot(221)
ax412 = ax411.twinx()
lines411 = ax411.plot(fftHz, fftThrottle_0, label="fft throttle_0 [amplitude]")
lines412 = ax411.plot(fftHz_0, fftEsc_0, label="fft ESC0 rpm [amplitude]")
ax411.set_xlabel("Hz")
ax411.set_title("fft: ESC0 RPM and Throttle")
ax411.legend()
ax411.grid()

ax421 = fig4.add_subplot(222)
ax422 = ax421.twinx()
lines421 = ax421.plot(fftHz, fftThrottle_1, label="fft throttle_1 [amplitude]")
lines422 = ax421.plot(fftHz_1, fftEsc_1, label="fft ESC1 rpm [amplitude]")
ax421.set_xlabel("Hz")
ax421.set_title("fft: ESC1 RPM and Throttle")
ax421.legend()
ax421.grid()

ax431 = fig4.add_subplot(223)
ax432 = ax431.twinx()
lines431 = ax431.plot(fftHz, fftThrottle_2, label="fft throttle_2 [amplitude]")
lines432 = ax431.plot(fftHz_2, fftEsc_2, label="fft ESC2 rpm [amplitude]")
ax431.set_xlabel("Hz")
ax431.set_title("fft: ESC2 RPM and Throttle")
ax431.legend()
ax431.grid()

ax441 = fig4.add_subplot(224)
ax442 = ax441.twinx()
lines441 = ax441.plot(fftHz, fftThrottle_3, label="fft throttle_3 [amplitude]")
lines442 = ax441.plot(fftHz_3, fftEsc_3, label="fft ESC3 rpm [amplitude]")
ax441.set_xlabel("Hz")
ax441.set_title("fft: ESC3 RPM and Throttle")
ax441.legend()
ax441.grid()

# ================================================================================================================

# print(57.30*(esc0['eRPM']/3000.00)^2)
esc0['Thrust [N]'] = (esc0['eRPM']*esc0['eRPM'])*(57.30/(3000.00*3000.00))
esc1['Thrust [N]'] = (esc1['eRPM']*esc1['eRPM'])*(57.30/(3000.00*3000.00))
esc2['Thrust [N]'] = (esc2['eRPM']*esc2['eRPM'])*(57.30/(3000.00*3000.00))
esc3['Thrust [N]'] = (esc3['eRPM']*esc3['eRPM'])*(57.30/(3000.00*3000.00))

fig5 = plt.figure()
ax511 = fig5.add_subplot(221)
lines511 = ax511.plot((esc1['Thrust [N]']+esc2['Thrust [N]']) - (esc0['Thrust [N]']+esc3['Thrust [N]']), label="Thrust1+2 - 0+3 [N]")
ax511.set_xlabel("Time [s]")
ax511.set_title("Left-Right Thrust Diff: Thrust 1+2 vs Thrust 0+3")
ax511.legend()
ax511.grid()

ax521 = fig5.add_subplot(222)
lines511 = ax521.plot((esc0['Thrust [N]']+esc2['Thrust [N]']) - (esc1['Thrust [N]']+esc3['Thrust [N]']), label="Thrust0+2 - 1+3 [N]")
ax521.set_xlabel("Time [s]")
ax521.set_title("Front-Back Thrust: Thrust 0+2 vs Thrust 1+3")
ax521.legend()
ax521.grid()

ax531 = fig5.add_subplot(223)
lines511 = ax531.plot((esc2['Thrust [N]'] - esc1['Thrust [N]']), label="Thrust2 - 1 [N]")
ax531.set_xlabel("Time [s]")
ax531.set_title("Left Thrust Diff: Thrust 2 vs Thrust 1")
ax531.legend()
ax531.grid()

ax541 = fig5.add_subplot(224)
lines511 = ax541.plot((esc0['Thrust [N]'] - esc3['Thrust [N]']), label="Thrust0 - 3 [N]")
ax541.set_xlabel("Time [s]")
ax541.set_title("Right Thrust Diff: Thrust 0 vs Thrust 3")
ax541.legend()
ax541.grid()

minLen = min(len(esc0['Thrust [N]']), len(esc1['Thrust [N]']), len(esc2['Thrust [N]']), len(esc3['Thrust [N]']))
leftRightDiff = (esc1['Thrust [N]'].values[0:minLen]+esc2['Thrust [N]'].values[0:minLen]) - (esc0['Thrust [N]'].values[0:minLen]+esc3['Thrust [N]'].values[0:minLen])
frontBackDiff = (esc0['Thrust [N]'].values[0:minLen]+esc2['Thrust [N]'].values[0:minLen]) - (esc1['Thrust [N]'].values[0:minLen]+esc3['Thrust [N]'].values[0:minLen])
leftDiff = (esc2['Thrust [N]'].values[0:minLen] - esc1['Thrust [N]'].values[0:minLen])
rightDiff = (esc0['Thrust [N]'].values[0:minLen] - esc3['Thrust [N]'].values[0:minLen])

NX = minLen
TX = totalSeconds / NX

fftHz_X = fftfreq(NX, TX)[0:NX//2]

fftEsc_LR = abs(fft(leftRightDiff))[0:NX//2]
fftEsc_FB = abs(fft(frontBackDiff))[0:NX//2]
fftEsc_L = abs(fft(leftDiff))[0:NX//2]
fftEsc_R = abs(fft(rightDiff))[0:NX//2]

fig6 = plt.figure()
ax611 = fig6.add_subplot(221)
lines611 = ax611.plot(fftHz_X, fftEsc_LR, label="LR fft [amplitude]")
ax611.set_xlabel("Hz")
ax611.set_title("LR Diff fft [amplitude]")
ax611.legend()
ax611.grid()

ax621 = fig6.add_subplot(222)
lines621 = ax621.plot(fftHz_X, fftEsc_FB, label="FB fft [amplitude]")
ax621.set_xlabel("Hz")
ax621.set_title("FB Diff fft [amplitude]")
ax621.legend()
ax621.grid()

ax631 = fig6.add_subplot(223)
lines631 = ax631.plot(fftHz_X, fftEsc_L, label="L fft [amplitude]")
ax631.set_xlabel("Hz")
ax631.set_title("L Diff fft [amplitude]")
ax631.legend()
ax631.grid()

ax641 = fig6.add_subplot(224)
lines641 = ax641.plot(fftHz_X, fftEsc_R, label="R fft [amplitude]")
ax641.set_xlabel("Hz")
ax641.set_title("R Diff fft [amplitude]")
ax641.legend()
ax641.grid()

plt.show()
