from exportkml import *
import pynmea2

kml = kmlclass()
#gpgga = nmea.GPGGA()

# Create kml file
kml.begin("test.kml", "test", "hej", 10)
kml.trksegbegin("drone", "route", "yellowLineGreenPoly", "absolute")

# Open file for reading
with open("nmea_trimble_gnss_eduquad_flight.txt", "r") as data_file:
    for line in data_file:
        current_line = line.split(',')  # Split the line by commas into a array

        # Only read lines if they are not empty
        if current_line[0] == "$GPGGA":
            msg = pynmea2.parse(line)

            kml.trkpt(float(msg.latitude), float(msg.longitude), float(msg.altitude))

kml.trksegend()
kml.end()
