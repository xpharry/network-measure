# Open a file
file = open("targets.txt", "r")
print "Name of the file: ", file.name
print "Closed or not : ", file.closed
print "Opening mode : ", file.mode
print "Softspace flag : ", file.softspace

# read a file by line
file.readline()
ip_list=[]
for line in file:
	ip=line[0:len(line)-1]
	# print ip
	ip_list.append(ip)
	# print line,

# Close opend file
file.close()

# check data stored in ip_list
for ip in ip_list:
	print ip
