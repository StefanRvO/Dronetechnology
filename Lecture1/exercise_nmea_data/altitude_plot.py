import NMEA_plotter


plotter = NMEA_plotter.NMEA_plotter()

#plot drone height over time
plotter.plot_height_over_time("nmea_trimble_gnss_eduquad_flight.txt")

#plot sattelites in use by static station over time.
plotter.plot_sattelites_in_use_over_time("nmea_ublox_neo_24h_static.txt")

#plot sattelites in use by static station over time by drone.
plotter.plot_sattelites_in_use_over_time("nmea_trimble_gnss_eduquad_flight.txt")
