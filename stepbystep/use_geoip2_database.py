import geoip2.database

def main():
	# This creates a Reader object. You should use the same object
	# across multiple requests as creation of it is expensive.
	reader = geoip2.database.Reader('GeoLite2-City.mmdb')

	# Replace "city" with the method corresponding to the database
	# that you are using, e.g., "country".
	response = reader.city('128.101.101.101')

	print response.country.iso_code
	print response.country.name
	print response.country.names['zh-CN']
	print response.subdivisions.most_specific.name
	print response.subdivisions.most_specific.iso_code
	print response.city.name
	print response.postal.code

	print "---- coordinate: ----"
	print response.location.latitude
	print response.location.longitude

	reader.close()

if __name__ == "__main__":
    main()