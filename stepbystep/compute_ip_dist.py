import math
import geoip2.database

class GeographicalPoint:
	def __init__(self, latitude, longitude):
		self.latitude = latitude * 3.14 / 180 # radius
		self.longitude = longitude * 3.14  / 180 # radius

	def get_latitude(self):
		return self.latitude

	def get_longitude(self):
		return self.longitude

def compute_dist(point1, point2):
	R = 6371.009 # kilometers 

	d_latitude = point2.get_latitude() - point1.get_latitude()
	d_longitude = point2.get_longitude() - point1.get_longitude()

	# mean_latitude = ( point1.get_latitude() + point2.get_latitude() ) / 2
	# dist = math.pow(d_latitude,2) + math.pow( ( math.cos(mean_latitude)*d_longitude ), 2)
	# dist = R * math.sqrt(dist)

	a2 = math.sin(d_latitude/2)**2 + math.cos(point1.get_latitude()) * math.cos(point2.get_latitude()) * math.sin(d_longitude/2)**2;                 
	c2 = 2 * math.asin(min(1,math.sqrt(a2))) ;            
	d2 = R * c2 ;                           
	print 'Distance using Haversine formula = %f' % d2  ;                                           

	return d2

def compute_ip_dist(ip):
	pointMe = GeographicalPoint(41.507181, -81.589571)

	# This creates a Reader object. You should use the same object
	# across multiple requests as creation of it is expensive.
	reader = geoip2.database.Reader('GeoLite2-City.mmdb')

	# Replace "city" with the method corresponding to the database
	# that you are using, e.g., "country".
	response = reader.city(ip)

	print "---- coordinate: ----"
	print response.location.latitude
	print response.location.longitude

	pointIP = GeographicalPoint(response.location.latitude, response.location.longitude)

	dist = compute_dist(pointMe, pointIP)

	reader.close()

	return dist

def main():

	ip = '23.10.205.11'

	dist = compute_ip_dist(ip)

	print dist

if __name__ == "__main__":
    main()