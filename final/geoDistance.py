import math
import geoip2.database
import socket

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
	# This creates a Reader object. You should use the same object
	# across multiple requests as creation of it is expensive.
	reader = geoip2.database.Reader('GeoLite2-City.mmdb')
	# Replace "city" with the method corresponding to the database
	# that you are using, e.g., "country".
	response = reader.city(ip)
	print "coordinate: %f %f" %(response.location.latitude, response.location.longitude)

	pointMe = GeographicalPoint(41.507181, -81.589571)
	pointIP = GeographicalPoint(response.location.latitude, response.location.longitude)
	dist = compute_dist(pointMe, pointIP)

	reader.close()
	return dist


def importServers():
    # Open a file
    file = open("targets.txt", "r")

    # read a file by line
    temp = file.read()
    ip_list = temp.split('\n')
    ip_list = ip_list[1:]

    # Close opend file
    file.close()

    # # check data stored in ip_list
    # for ip in ip_list:
    #   print ip

    return ip_list

def main():
    ip_list = importServers()
    i = 0;
    for dest_name in ip_list:
        i = i+1
        dest_name = dest_name.strip()
        print "destination No.%d: %s" %(i, dest_name)
        dest_name = u'%s' %dest_name
        ip = socket.gethostbyname(dest_name)
        compute_ip_dist(ip)
        print

if __name__ == '__main__':
    main()