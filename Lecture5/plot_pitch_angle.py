#!/usr/bin/python2
from Modules.imu_exercise import plot_accel
from math import pi, sqrt, atan2
def plot_func(**kwargs):

        roll = atan2(-kwargs["acc_x"],kwargs["acc_z"])
        pitch = kwargs["acc_y"]/( (kwargs["acc_x"] ** 2 + kwargs["acc_z"] ** 2) ** 0.5)
        return pitch

def __main__():
    ## Uncomment the file to read ##
    #fileName = 'nmea_data.txt'
    #fileName = 'imu_razor_data_static.txt'
    #fileName = 'imu_razor_data_yaw_90deg.txt'
    fileName = 'imu_razor_data_pitch_45deg.txt'
    #fileName = 'imu_razor_data_roll_45deg.txt'

    ## IMU type
    #imuType = 'vectornav_vn100'
    imuType = 'sparkfun_razor'
    plot_accel(imuType, fileName, plot_func)

__main__()
