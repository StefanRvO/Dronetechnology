#!/usr/bin/python2
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
_speed_of_light = 299792458 #m/s

class FresnelPlotter:
    def __init__(self, tx_coord, rx_coord):
        self.tx_coord = np.array([tx_coord["x"], tx_coord["y"], tx_coord["z"]])
        self.rx_coord = np.array([rx_coord["x"], rx_coord["y"], rx_coord["z"]])
        self.direction_vec = np.array([tx_coord["x"] - rx_coord["x"],
                                       tx_coord["y"] - rx_coord["y"],
                                       tx_coord["z"] - rx_coord["z"]
                                       ])
        self.perp_1 = np.array([ - self.direction_vec[1], self.direction_vec[0], 0 ])
        self.perp_2 = np.array([ - self.direction_vec[2], 0, self.direction_vec[0] ])
        self.perp_1 = self.perp_1 / np.linalg.norm(self.perp_1)
        self.perp_2 = self.perp_2 / np.linalg.norm(self.perp_2)

        self.distance = np.linalg.norm(self.direction_vec)
    def plot(self, zone_cnt, freq):
        #Plot the freznel zone with the given coordinates and zones.
        wave_length = _speed_of_light / freq
        fig = pyplot.figure(figsize=(16, 8), dpi=100,)
        ax = fig.add_subplot(111, projection='3d')
        distances =  np.linspace(0, self.distance, 200) #From tx
        u = np.linspace(0, 2 * np.pi, 30) # all spehrical angles
        unit_vec = - self.direction_vec / self.distance
        print(distances)
        for n in range(1, zone_cnt + 1):
            x = []
            y = []
            z = []
            radiuses = (n * wave_length * distances * (self.distance - distances) \
                        / self.distance) ** 0.5
            for i in range(len(radiuses)):
                r = radiuses[i]
                d = distances[i]
                coord = self.tx_coord + unit_vec * d
                for j in range(len(u)):
                    cos_part = r * np.cos(u[j]) * self.perp_1
                    sin_part = r * np.sin(u[j]) * self.perp_2
                    x.append( (coord + cos_part +  sin_part)[0] )
                    y.append( (coord + cos_part +  sin_part)[1] )
                    z.append( (coord + cos_part +  sin_part)[2] )

            ax.plot(x, y, z, label = "zone %d" % n )
        ax.scatter(self.tx_coord[0], self.tx_coord[1], self.tx_coord[2], label = 'tx')
        ax.scatter(self.rx_coord[0], self.rx_coord[1], self.rx_coord[2], label = 'rx')
        pyplot.legend()
        pyplot.show()
def _main_():
    plotter = FresnelPlotter( tx_coord = {"x" : 0, "y" : 0, "z" : 0},
                rx_coord = {"x" : 50, "y" : 80, "z" : 10})

    plotter.plot(2, 433 * 10 ** 6)

if __name__ == "__main__":
    _main_()
