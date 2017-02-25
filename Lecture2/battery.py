import matplotlib.pyplot as plt
import numpy as np


class battery(object):

	def __init__(s,x,y):
		s.x = x
		s.y = y
		s.minimum = min(s.y)
		s.smoothing_done = 0;
		# Correct the x(time)-axis
		s.x[:] = [x - min(s.x) for x in s.x]
		#print s.y[1]
		pass

	def showOriginal(s):
		plt.figure(1)
		plt.plot(s.x,s.y,linewidth=1,color='b')
		plt.show()

	def showSmooth(s):
		plt.figure(2)
		plt.plot(s.x,s.y,linewidth=1,color='b')
		plt.plot(s.sm_x,s.sm_y,linewidth=3,color='r')
		plt.show()

	def smooth(s,sm_factor):
		s.smoothing_done = 1;
		s.sm_factor = sm_factor
		s.sm_x = []
		s.sm_y = []

		s.sm_y.append(s.y[0])
		s.sm_x.append(s.x[0])
		for i in range(s.sm_factor, len(s.x)-s.sm_factor,s.sm_factor):
			this_y = np.mean(s.y[i-(s.sm_factor/2):i+(s.sm_factor/2)])
			s.sm_y.append((this_y))
			s.sm_x.append(s.x[i])
		s.sm_y.append(s.y[-1])
		s.sm_x.append(s.x[-1])


	def integrate(s):
		if s.smoothing_done == 0:
			print 'Smoothing has not been done yet'
		else:
			s.intgr_y = []
			s.intgr_y.append(0)
			for i in range(1, len(s.sm_x)):
				s.intgr_y.append((((s.sm_y[i]-s.minimum)+(s.sm_y[i-1]-s.minimum))/2)*(abs(s.sm_x[i]-s.sm_x[i-1])))

			print sum(s.intgr_y)



		print s.sm_x[1]-s.sm_x[0]
		print s.sm_x[2]-s.sm_x[1]
		print s.sm_x[3]-s.sm_x[2]
		print s.sm_x[4]-s.sm_x[3]
		print s.sm_y[0]-s.minimum
		print s.sm_y[1]-s.minimum

		print (((s.sm_y[83]-s.minimum)+(s.sm_y[82]-s.minimum))/2)*(abs(s.sm_x[83]-s.sm_x[82]))

		print (s.intgr_y)

		print len(s.intgr_y)
