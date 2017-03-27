#!/usr/bin/python2
from Modules.exercise_route_planning.aqlogreader.AQLogReader import aqLogReader
from Modules.exercise_nmea_data.exportkml import *
from WaypointGenerator import WaypointGenerator
import pynmea2
from QGroundControlWaypointExporter import QGroundControl_WP_Gen
def plot_route(kml_filename, data_list):
    #the data_list is a list off dicts. each dict contains "data" and "color"
    #The data should be an array of dicts with "GPS_LAT", "GPS_LON", "GPS_HEIGHT"

    kml = kmlclass()

    # Create kml file
    kml.begin(kml_filename, "test", "hej", 10)
    for the_dict in data_list:
        kml.trksegbegin("drone", "route", the_dict["color"], "absolute")
        for d in the_dict["data"]:
            kml.trkpt(float(d["GPS_LAT"]), float(d["GPS_LON"]), float(d["GPS_HEIGHT"]))

        kml.trksegend()
    kml.end()


def __main__():
    #Plot 021-AQL
    aq_reader = aqLogReader("Modules/exercise_route_planning/021-AQL.LOG")
    aq_reader.setChannels(["GPS_LAT", "GPS_LON", "GPS_HEIGHT", "UKF_POSN", "UKF_POSE"])
    data = aq_reader.getData()
    dict_data = []
    for d in data:
        if(d[0] == 0.0 and d[1] == 0.0 and d[2] == 0.0): continue

        dict_data.append({  "GPS_LAT" :     d[0],
                            "GPS_LON" :     d[1],
                            "GPS_HEIGHT" :  d[2],
                            "UKF_POSN" :    d[3],
                            "UKF_POSE" :    d[4],
                        })
    wp_gen = WaypointGenerator(dict_data)
    waypoints = wp_gen.create_waypoints(max_distance = 1)
    plot_route("aql_021.kml", [{"color" : "yellowLineGreenPoly", "data" : waypoints},
                            {"color" : "blueLineGreenPoly", "data" : dict_data},
                            ])
    q_control_wp = QGroundControl_WP_Gen(waypoints)
    q_control_wp.export("qg_wp.txt")
    #Plot NMEA data
    # nmea_dict_data = []
    # with open("Modules/exercise_route_planning/nmea_trimble_gnss_eduquad_flight.txt", "r") as data_file:
    #     for line in data_file:
    #         # Only read lines if they are not empty
    #         if "$GPGGA" in line:
    #             msg = pynmea2.parse(line)
    #             if None not in [msg.latitude, msg.longitude, msg.altitude]:
    #                 nmea_dict_data.append({  "GPS_LAT" : float(msg.latitude),
    #                                     "GPS_LON" :     float(msg.longitude),
    #                                     "GPS_HEIGHT" :  float(msg.altitude),
    #                                 })
    # wp_gen_nmea = WaypointGenerator(nmea_dict_data)
    # waypoints_nmea = wp_gen_nmea.create_waypoints(max_distance = 1)
    # plot_route("nmea.kml", [{"color" : "yellowLineGreenPoly", "data" : waypoints_nmea},
    #                         {"color" : "blueLineGreenPoly", "data" : nmea_dict_data},
    #                         ])


__main__()
