from Modules.transverse_mercator_py.utm import utmconv
from math import pi, cos
from numpy import sin, arccos, sqrt, arcsin, pi

# Calculate the great circle distance between two coordinates
def great_circle_dist(lat1_deg, lon1_deg, lat2_deg, lon2_deg):
    # Convert from latitude/longtitude degrees to radians
    lat1_rad = (lat1_deg / 180) * pi
    lat2_rad = (lat2_deg / 180) * pi
    lon1_rad = (lon1_deg / 180) * pi
    lon2_rad = (lon2_deg / 180) * pi

    # Calculate and return great circle distance
    return arccos(sin(lat1_rad)*sin(lat2_rad)+cos(lat1_rad)*cos(lat2_rad)*cos(lon1_rad-lon2_rad)) * 6366.71
    #return arcsin(sqrt((sin((lat1_rad-lat2_rad)/2))**2 + cos(lat1_rad)*cos(lat2_rad)*(sin((lon1_rad-lon2_rad)/2))**2)) * 6366.71

def test_utm_gcd_difference():
    # define test position
    test_lat =  55.0000000000
    test_lon = 009.0000000000
    print 'Test position [deg]:'
    print '  latitude:  %.10f'  % (test_lat)
    print '  longitude: %.10f'  % (test_lon)

    # instantiate utmconv class
    uc = utmconv()

    # convert from geodetic to UTM
    (hemisphere, zone, letter, easting, northing) = uc.geodetic_to_utm (test_lat,test_lon)
    print '\nConverted from geodetic to UTM [m]'
    print '  %d %c %.5fe %.5fn' % (zone, letter, easting, northing)
    #easting += 1000
    northing += 1000

    # convert back from UTM to geodetic
    (lat, lon) = uc.utm_to_geodetic (hemisphere, zone, easting, northing)
    print '\nConverted back from UTM to geodetic [deg]:'
    print '  latitude:  %.10f'  % (lat)
    print '  longitude: %.10f'  % (lon)

    # Great circle distance
    print "\nGreat circle distance: %f " % great_circle_dist(test_lat, test_lon, lat, lon)
