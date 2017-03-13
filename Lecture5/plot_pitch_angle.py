#!/usr/bin/python2
from Modules.imu_exercise import plot_accel
from Modules.imu_exercise_kalman import plot_accel as plot_kalman
from math import pi, sqrt, atan2

def do_running_average(data_list, n):
    #return an average of the last n elements in the given list.
    #If the list contains fewer than n samples, we just return the average of them.
    if(len(data_list) >= n):
        return sum(data_list[-n:]) / n
    else:
    #We have not sampled enough yet.
        return sum(data_list) / len(data_list)

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

def plot_roll_avg_func(**kwargs):
    #compute the variable
    plotdata = kwargs["plotdata"]
    roll = atan2(-kwargs["acc_x"],kwargs["acc_z"])
    roll *= 180/pi

    #Add the variable to plotdata. If it does not exist yet, simply create it in the dict
    try:
        roll_avg = do_running_average(plotdata["series"][0]["data"], 25)
        plotdata["series"][0]["data"].append(roll)
        plotdata["series"][1]["data"].append(roll_avg)
    except:
        plotdata["series"] = []
        plotdata["series"].append({"data" : [], "label" : "roll"})
        plotdata["series"].append({"data" : [], "label" : "roll lowpass"})
        plotdata["series"][0]["data"].append(roll)
        plotdata["series"][1]["data"].append(roll)

def plot_pitch_avg_func(**kwargs):
    #compute the variable
    plotdata = kwargs["plotdata"]
    pitch = atan2(kwargs["acc_y"], ( (kwargs["acc_x"] ** 2 + kwargs["acc_z"] ** 2) ** 0.5))
    pitch *= 180/pi

    #Add the variable to plotdata. If it does not exist yet, simply create it in the dict
    try:
        pitch_avg = do_running_average(plotdata["series"][0]["data"], 25)
        plotdata["series"][0]["data"].append(pitch)
        plotdata["series"][1]["data"].append(pitch_avg)
    except:
        plotdata["series"] = []
        plotdata["series"].append({"data" : [], "label" : "pitch"})
        plotdata["series"].append({"data" : [], "label" : "pitch lowpass"})
        plotdata["series"][0]["data"].append(pitch)
        plotdata["series"][1]["data"].append(pitch)

def plot_pitch_avg_func(**kwargs):
    #compute the variable
    plotdata = kwargs["plotdata"]
    pitch = atan2(kwargs["acc_y"], ( (kwargs["acc_x"] ** 2 + kwargs["acc_z"] ** 2) ** 0.5))
    pitch *= 180/pi

    #Add the variable to plotdata. If it does not exist yet, simply create it in the dict
    try:
        pitch_avg = do_running_average(plotdata["series"][0]["data"], 25)
        plotdata["series"][0]["data"].append(pitch)
        plotdata["series"][1]["data"].append(pitch_avg)
    except:
        plotdata["series"] = []
        plotdata["series"].append({"data" : [], "label" : "pitch"})
        plotdata["series"].append({"data" : [], "label" : "pitch lowpass"})
        plotdata["series"][0]["data"].append(pitch)
        plotdata["series"][1]["data"].append(pitch)

def plot_yaw_gyro_func(**kwargs):
    #compute the variable
    #Create the integral if it does not exist
    init_angle = 90
    plotdata = kwargs["plotdata"]
    bias =  2.65/5900
    #initialize to init angle if first time.
    try:
        plotdata["yaw_integral"]
    except:
        plotdata["yaw_integral"] = init_angle
        plotdata["yaw_integral_unbiased"] = init_angle


    #Integrate the gyro value
    plotdata["yaw_integral"] += kwargs["gyro_z"] * (kwargs["ts_now"] - kwargs["ts_prev"]) * 180/pi
    plotdata["yaw_integral_unbiased"] += kwargs["gyro_z"] * (kwargs["ts_now"] - kwargs["ts_prev"]) * 180/pi - bias

    #Add the variable to plotdata. If it does not exist yet, simply create it in the dict
    try:
        plotdata["series"][0]["data"].append(plotdata["yaw_integral"])
        plotdata["series"][1]["data"].append(plotdata["yaw_integral_unbiased"])

    except:
        plotdata["series"] = []
        plotdata["series"].append({"data" : [], "label" : "yaw_gyro"})
        plotdata["series"].append({"data" : [], "label" : "yaw_gyro_unbiased"})

        plotdata["series"][0]["data"].append(plotdata["yaw_integral"])
        plotdata["series"][1]["data"].append(plotdata["yaw_integral_unbiased"])

def __main__():
    ## Uncomment the file to read ##
    #fileName = 'nmea_data.txt'
    #fileName = 'imu_razor_data_static.txt'
    #fileName = 'imu_razor_data_yaw_90deg.txt'

    #Plot the pitch data
    fileName = 'imu_razor_data_pitch_45deg.txt'
    imuType = 'sparkfun_razor'
    plot_accel(imuType, fileName, plot_pitch_func, pngname = "pitch_accel.png", showplot = False)

    #plot the roll data
    fileName = 'imu_razor_data_roll_45deg.txt'
    imuType = 'sparkfun_razor'
    plot_accel(imuType, fileName, plot_roll_func, pngname = "roll_accel.png", showplot = False)

    #plot the static data
    fileName = 'imu_razor_data_static.txt'
    imuType = 'sparkfun_razor'
    plot_accel(imuType, fileName, plot_static_func, pngname = "static_accel.png", showplot = False)

    fileName = 'imu_razor_data_roll_45deg.txt'
    imuType = 'sparkfun_razor'
    plot_accel(imuType, fileName, plot_roll_avg_func, pngname = "roll_avg_accel.png", showplot = False)

    fileName = 'imu_razor_data_pitch_45deg.txt'
    imuType = 'sparkfun_razor'
    plot_accel(imuType, fileName, plot_pitch_avg_func, pngname = "pitch_avg_accel.png", showplot = False)

    fileName = 'imu_razor_data_yaw_90deg.txt'
    imuType = 'sparkfun_razor'
    plot_accel(imuType, fileName, plot_yaw_gyro_func, pngname = "gyro_yaw.png", showplot = False)

    fileName = 'imu_razor_data_static.txt'
    imuType = 'sparkfun_razor'
    plot_accel(imuType, fileName, plot_yaw_gyro_func, pngname = "gyro_yaw.png", showplot = False)

    #Plot using kalman filter and pitch dataset
    fileName = 'imu_razor_data_pitch_45deg.txt'
    imuType = 'sparkfun_razor'
    plot_kalman(imuType, fileName, showPlot = True, show3DLiveView = False,
        gyro_bias = {"x" : (50.5 / 1300.) / (180. / pi) * 100, "y" : (36.2 / 1300.) / (180. / pi) * 100, "z" : 0 },
        gyro_var = 0.38 / (180. / pi) / 100,
        axis = "pitch")

    #Plot using kalman filter and roll dataset
    fileName = 'imu_razor_data_roll_45deg.txt'
    imuType = 'sparkfun_razor'
    plot_kalman(imuType, fileName, showPlot = True, show3DLiveView = False,
        gyro_bias = {"x" : (50.5 / 1300.) / (180. / pi) * 100, "y" : (36.2 / 1300.) / (180. / pi) * 100, "z" : 0 },
        gyro_var = 0.38 / (180. / pi) / 100,
        axis = "roll")


__main__()
