#!/usr/bin/python2
from Modules.imu_exercise import plot_accel
from math import pi, sqrt, atan2
def plot_pitch_func(**kwargs):
    #compute the variable
    plotdata = kwargs["plotdata"]
    pitch = atan2(kwargs["acc_y"], ( (kwargs["acc_x"] ** 2 + kwargs["acc_z"] ** 2) ** 0.5))
    pitch *= 180/pi

    #Add the variable to plotdata. If it does not exist yet, simply create it in the dict
    try:
        plotdata["series"][0]["data"].append(pitch)
    except:
        plotdata["series"] = []
        plotdata["series"].append({"data" : [], "label" : "pitch"})
        plotdata["series"][0]["data"].append(pitch)

def plot_roll_func(**kwargs):
    #compute the variable
    plotdata = kwargs["plotdata"]
    roll = atan2(-kwargs["acc_x"],kwargs["acc_z"])
    roll *= 180/pi

    #Add the variable to plotdata. If it does not exist yet, simply create it in the dict
    try:
        plotdata["series"][0]["data"].append(roll)
    except:
        plotdata["series"] = []
        plotdata["series"].append({"data" : [], "label" : "roll"})
        plotdata["series"][0]["data"].append(roll)

def plot_static_func(**kwargs):
    #compute the variable
    plotdata = kwargs["plotdata"]
    roll = atan2(-kwargs["acc_x"],kwargs["acc_z"])
    roll *= 180/pi
    pitch = atan2(kwargs["acc_y"], ( (kwargs["acc_x"] ** 2 + kwargs["acc_z"] ** 2) ** 0.5))
    pitch *= 180/pi


    #Add the variable to plotdata. If it does not exist yet, simply create it in the dict
    try:
        plotdata["series"][0]["data"].append(roll)
        plotdata["series"][1]["data"].append(pitch)

    except:
        plotdata["series"] = []
        plotdata["series"].append({"data" : [], "label" : "roll"})
        plotdata["series"].append({"data" : [], "label" : "pitch"})
        plotdata["series"][0]["data"].append(roll)
        plotdata["series"][1]["data"].append(pitch)


def __main__():
    ## Uncomment the file to read ##
    #fileName = 'nmea_data.txt'
    #fileName = 'imu_razor_data_static.txt'
    #fileName = 'imu_razor_data_yaw_90deg.txt'

    #Plot the pitch data
    fileName = 'imu_razor_data_pitch_45deg.txt'
    imuType = 'sparkfun_razor'
    plot_accel(imuType, fileName, plot_pitch_func)
    #plot the roll data
    fileName = 'imu_razor_data_roll_45deg.txt'
    imuType = 'sparkfun_razor'
    plot_accel(imuType, fileName, plot_roll_func)
    #plot the static data
    fileName = 'imu_razor_data_static.txt'
    imuType = 'sparkfun_razor'
    plot_accel(imuType, fileName, plot_static_func)


__main__()
