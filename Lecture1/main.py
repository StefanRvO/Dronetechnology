from Modules.exercise_nmea_data.exportkml import *
import pynmea2
import utm_test
from Modules.NMEA_plotter import NMEA_plotter

def plot_route(kml_filename, data_filename):

    kml = kmlclass()

    # Create kml file
    kml.begin(kml_filename, "test", "hej", 10)
    kml.trksegbegin("drone", "route", "yellowLineGreenPoly", "absolute")

    # Open file for reading
    with open(data_filename, "r") as data_file:
        for line in data_file:
            # Only read lines if they are not empty
            if "$GPGGA" in line:
                msg = pynmea2.parse(line)

                kml.trkpt(float(msg.latitude), float(msg.longitude), float(msg.altitude))

    kml.trksegend()
    kml.end()

def __main__():


    plot_route("drone_track.kml", "nmea_trimble_gnss_eduquad_flight.txt")
    #plot_route("static_track.kml", "nmea_ublox_neo_24h_static.txt")


    utm_test.test_utm_gcd_difference()

    plotter = NMEA_plotter.NMEA_plotter()
    #plot drone height over time
    plotter.plot_height_over_time("nmea_trimble_gnss_eduquad_flight.txt")
    #plot sattelites in use by static station over time.
    plotter.plot_sattelites_in_use_over_time("nmea_ublox_neo_24h_static.txt")
    #plot sattelites in use by drone over time.
    plotter.plot_sattelites_in_use_over_time("nmea_trimble_gnss_eduquad_flight.txt")


__main__()
