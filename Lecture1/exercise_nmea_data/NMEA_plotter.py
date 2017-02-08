#Python(2) class for plotting NMEA_data!
#Be sure to install requirements (pip install -r requirements.txt)

import pynmea2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates
import datetime

class parsed_object:
    def __init__(self):
        pass


class NMEA_plotter:
    def __init__(self):
        self.self_passed = ["$GPGSV", ]

    def plot_height_over_time(self, nmea_file):
        #Plots the altitude over time.
        #Just displays the plot when done (Should probably be changed so we return a plotobject or something)
        self.plot_x_over_time(nmea_file, plotattrib = 'altitude', sentence_type = "$GPGGA")

    def plot_sattelites_in_use_over_time(self, nmea_file):
        #Plots the altitude over time.
        #Just displays the plot when done (Should probably be changed so we return a plotobject or something)
        self.plot_x_over_time(nmea_file, plotattrib = 'num_sats', sentence_type = "$GPGGA")

    def plot_sattelites_in_view_over_time(self, nmea_file):
        #Plots the altitude over time.
        #Just displays the plot when done (Should probably be changed so we return a plotobject or something)
        self.plot_x_over_time(nmea_file, plotattrib = 'sats_in_view', sentence_type = "$GPGSV")

    def plot_x_over_time(self, nmea_file, plotattrib, sentence_type):
        #Plot variable x over time (from gpgga data)

        x = []
        y = []
        times = []
        with open(nmea_file, "r") as data_file:
            day_cnt = 1
            last_time = None
            cur_time = None
            cur_data = None
            for line in data_file:
                # We want GPGGA data!
                if "$GPGGA" in line:
                    msg = pynmea2.parse(line)
                    #We really want a datetime instead of just a time...
                    millisecond =  float(msg.timestamp.hour    * 60 * 60 * 1000)
                    millisecond += float(msg.timestamp.minute  * 60 * 1000)
                    millisecond += float(msg.timestamp.second  * 1000)
                    millisecond += msg.timestamp.microsecond / 1000.
                    #Make sure time always moves forward. Time delta
                    if(last_time is not None and last_time > millisecond):
                        day_cnt += 1
                    last_time = millisecond
                    cur_time = datetime.datetime.combine(datetime.date(1,1,day_cnt), msg.timestamp)
                #Add the actual data
                if sentence_type in line:
                    gps_data = None
                    if sentence_type not in self.self_passed:
                        #Use pynmea2 to parse the data
                        msg = pynmea2.parse(line)
                        gps_data = getattr(msg, plotattrib)

                    else:
                        msg = self.parse_line(line)
                        gps_data = getattr(msg, plotattrib)
                    #append the attribute to the y series.
                    if gps_data is not None:
                        y.append(gps_data)
                        times.append(cur_time)

        for time in times:
            x.append((time - times[0]).total_seconds())

        plt.plot(x,y)
        plt.show()

    def parse_line(self, line):
        if "$GPGSV" in line:
            return self.parse_gpgsv(line)

    def parse_gpgsv(self, line):
        return_obj = parsed_object()
        splitted_line = line.split(',')
        setattr(return_obj, 'type', splitted_line[0])
        setattr(return_obj, 'sats_in_view', splitted_line[3])
        return return_obj
