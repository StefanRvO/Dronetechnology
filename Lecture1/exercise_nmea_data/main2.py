from exportkml import *
import pynmea2

kml = kmlclass()
#gpgga = nmea.GPGGA()

# Create kml file
kml.begin("test.kml", "test", "hej", 100)
kml.trksegbegin("drone", "route", "yellowLineGreenPoly", "absolute")

# Open file for reading
with open("nmea_ublox_neo_24h_static.txt", "r") as data_file:
#with open("nmea_trimble_gnss_eduquad_flight.txt", "r") as data_file:

    i = 0
    for line in data_file:

        # Only read lines if they are not empty
        if "$GPGGA" in line:
            msg = pynmea2.parse(line)
            if None not in [msg.latitude, msg.longitude, msg.altitude]:
                i+=1
                if i < 65000:
                    kml.trkpt(float(msg.latitude), float(msg.longitude), float(msg.altitude))

kml.trksegend()
kml.end()
