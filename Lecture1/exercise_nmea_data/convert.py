from exportkml import kmlclass
import sys
from pynmea.streamer import NMEAStream
from pynmea import nmea
import traceback

kml = kmlclass()

kml.begin(sys.argv[2], "test", "test2", 9)
kml.trksegbegin("test3", "test4", "red", "absolute")

#Import the data
with open(sys.argv[1], 'r') as data_file:
    while True:
        next_line = data_file.readline()
        if len(next_line) == 0:
            break
        gpgga = nmea.GPGGA()
        gpgga.parse(next_line)
        try:
            kml.trkpt(float(gpgga.latitude) / 100, float(gpgga.longitude) / 100, float(gpgga.antenna_altitude))
        except:
            print("No latitude")
            traceback.print_exc()
kml.trksegend()

kml.end()
