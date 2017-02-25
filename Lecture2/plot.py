import matplotlib.pyplot as plt
import numpy as np
from battery import battery

x = []
y = []

with open('log-2016-01-14.txt') as data_file:
	for line in data_file:
		currentline = line.split('\t')
		hour = int(currentline[4][0:2])
		minute = int(currentline[4][2:4])
		second = int(currentline[4][4:6])
		tot_seconds = second + (minute*60) + (hour*3600)
		voltage = float(currentline[11])
		x.append(tot_seconds)
		y.append(voltage)


myBattery = battery(x,y)
myBattery.smooth(50)
myBattery.showSmooth()

myBattery.integrate()
