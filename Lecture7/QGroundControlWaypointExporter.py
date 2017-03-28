#Class for creating QGroundControl waypoints
# qgc parameters
qgc_dunno = 0
qgc_frame_takeoff = 0 # 0 = abs 3 = relative
qgc_frame_wpt = 0 # 0 = abs 3 = relative
qgc_poi_heading = 0
qgc_vert_vmax = 1.0
qgc_radius = 3.5
qgc_loiter = 1
qgc_dunno2 = 1



# qgc constants
MAV_CMD_NAV_WAYPOINT = 16
MAV_CMD_NAV_TAKEOFF = 22







class QGroundControl_WP_Exporter:
    def __init__(self, track_data):
        self.track_data = track_data

    def export(self, filename):
        wp_string = 'QGC WPL 120\n'
        wp_num = 0
        for wp in self.track_data:
            if(wp_num == 0):
                wp_string = wp_string + '%d\t%d\t%d\t%d\t%.2f\t%.0f\t%.2f\t%.2f\t%.8f\t%.8f\t%.3f\t%d\n' % \
                    (0, qgc_dunno, qgc_frame_takeoff, MAV_CMD_NAV_TAKEOFF, qgc_radius, qgc_loiter*1000, 0, 10000, wp["GPS_LON"], wp["GPS_LAT"], wp["GPS_HEIGHT"], qgc_dunno2)
            else:
                wp_string = wp_string + '%d\t%d\t%d\t%d\t%.2f\t%.0f\t%.2f\t%.2f\t%.8f\t%.8f\t%.3f\t%d\n' % \
                    (0, qgc_dunno, qgc_frame_takeoff, MAV_CMD_NAV_WAYPOINT, qgc_radius, qgc_loiter*1000, 0, 10000, wp["GPS_LON"], wp["GPS_LAT"], wp["GPS_HEIGHT"], qgc_dunno2)
            wp_num+=1
        with open(filename, "w") as data_file:
            data_file.write(wp_string)
