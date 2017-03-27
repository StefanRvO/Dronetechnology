#!/usr/bin/python2
from Modules.transverse_mercator_py.utm import utmconv
import numpy as np
class WaypointGenerator:
    def __init__(self, track_data):
        #-1 means that we don't care about this parameter.
        #For now, only one constraint can be used at the same time.
        self.track_data = track_data
        # instantiate utmconv class
        self.uc = utmconv()
        # convert from geodetic to UTM
    def create_waypoints(self, max_waypoints = -1, max_distance = -1, max_bearing = -1):
        #-1 means that we don't care about this parameter.
        #For now, only one constraint can be used at the same time.
        waypoints = []
        waypoints.append(0)
        for index in range(1, len(self.track_data)):
            if self.check_connection(waypoints[-1], index, max_distance) == True:
                continue
            else:
                waypoints.append(index - 1)
        waypoints.append(len(self.track_data) - 1)
        #Convert to a dict
        waypoint_dicts = []
        for i in waypoints:
            waypoint_dicts.append(self.track_data[i])
        return waypoint_dicts



    def check_connection(self, index_1, index_2, max_distance):
        if index_1 > len(self.track_data) - 1 or index_2 > len(self.track_data) - 1:
            print("Something very wrong happend...")
            return None

        utm_1 = self.uc.geodetic_to_utm (   self.track_data[index_1]["GPS_LAT"],
                                            self.track_data[index_1]["GPS_LON"])
        utm_2 = self.uc.geodetic_to_utm ( self.track_data[index_2]["GPS_LAT"],
                                            self.track_data[index_2]["GPS_LON"])
        #create a numpy vector for each point
        #We now test the distance from the line connecting the two coordinates
        #To every point between.
        vec_1 = np.array([  utm_1[3], utm_1[4],
                            self.track_data[index_1]["GPS_HEIGHT"]
                            ])
        #print(np.linalg.norm(vec_1))
        vec_2 = np.array([  utm_2[3], utm_2[4],
                            self.track_data[index_2]["GPS_HEIGHT"]
                            ])
        if(np.linalg.norm(vec_1 - vec_2) < 0.000001): return True #We don't want to divide by zero.

        for point in range(index_1 + 1, index_2):
            utm_point = list(self.uc.geodetic_to_utm ( self.track_data[point]["GPS_LAT"],
                                                self.track_data[point]["GPS_LON"]))
            vec_point = np.array([  utm_point[3], utm_point[4],
                                    self.track_data[point]["GPS_HEIGHT"]
                                    ])
            distance = np.linalg.norm(np.cross(vec_2 - vec_1, vec_1 - vec_point)) / np.linalg.norm(vec_2 - vec_1)
            if(distance > max_distance): return False
        return True
