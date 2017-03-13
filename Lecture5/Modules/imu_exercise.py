#!/usr/bin/python
# -*- coding: utf-8 -*-

# IMU exercise
# Copyright (c) 2015-2017 Kjeld Jensen kjen@mmmi.sdu.dk kj@kjen.dk

##### Insert initialize code below ###################




######################################################

# import libraries
from math import pi, sqrt, atan2
import matplotlib.pyplot as plt


# looping through file
def plot_accel(imuType, fileName, plot_func, showplot = True, saveplot = True):
    ## Variables for plotting ##
    showPlot = True
    plotData = []
    plotdata = {}
    # open the imu data file
    f = open (fileName, "r")

    # initialize variables
    count = 0

    for line in f:
        count += 1

        # split the line into CSV formatted data
        line = line.replace ('*',',') # make the checkum another csv value
        csv = line.split(',')

        # keep track of the timestamps
        ts_recv = float(csv[0])
        if count == 1:
            ts_now = ts_recv # only the first time
            ts_prev = ts_now
            ts_now = ts_recv

        if imuType == 'sparkfun_razor':
            # import data from a SparkFun Razor IMU (SDU firmware)
            acc_x = float(csv[2]) / 1000.0 * 4 * 9.82;
            acc_y = float(csv[3]) / 1000.0 * 4 * 9.82;
            acc_z = float(csv[4]) / 1000.0 * 4 * 9.82;
            gyro_x = float(csv[5]) *  1/14.375 * pi/180.0;
            gyro_y = float(csv[6]) * 1/14.375 * pi/180.0;
            gyro_z = float(csv[7]) * 1/14.375 * pi/180.0;

        elif imuType == 'vectornav_vn100':
            # import data from a VectorNav VN-100 configured to output $VNQMR
            acc_x = float(csv[9])
            acc_y = float(csv[10])
            acc_z = float(csv[11])
            gyro_x = float(csv[12])
            gyro_y = float(csv[13])
            gyro_z = float(csv[14])

        ##### Insert loop code below #########################

        # Variables available
        # ----------------------------------------------------
        # count        Current number of updates
        # ts_prev    Time stamp at the previous update
        # ts_now    Time stamp at this update
        # acc_x        Acceleration measured along the x axis
        # acc_y        Acceleration measured along the y axis
        # acc_z        Acceleration measured along the z axis
        # gyro_x    Angular velocity measured about the x axis
        # gyro_y    Angular velocity measured about the y axis
        # gyro_z    Angular velocity measured about the z axis

        ## Insert your code here ##


        plot_func(acc_x = acc_x, acc_y = acc_y, acc_z = acc_z
            , gyro_x = gyro_x, gyro_y = gyro_y, gyro_z = gyro_z, plotdata = plotdata)
        # in order to show a plot use this function to append your value to a list:
        #plotData.append (plotvar*180.0/pi)

        ######################################################

    # closing the file
    f.close()

    # show the plot
    if showPlot == True:
        #plt.plot(plotData)
        for series in plotdata["series"]:
            plt.plot(series["data"], label=series["label"])
        plt.legend()
        if(saveplot):
            plt.savefig(fileName + ".png")
        if(showplot):
            plt.show()
