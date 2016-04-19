# Open a file
file = open("targets.txt", "r")
# print "Name of the file: ", file.name
# print "Closed or not : ", file.closed
# print "Opening mode : ", file.mode
# print "Softspace flag : ", file.softspace

# read a file by line
string = file.read()
print string

ip_list = string.split('\n')
# for line in file:
#     line = line.strip()
#     if not len(line) or line.startswith('#'):
#         continue  
#     ip_list.append(line) 

# Close opend file
file.close()

# check data stored in ip_list
for ip in ip_list:
    # if not ip == ip_list[0]:
    #     ip = ip[3:]
	print ip.strip()
	ip = ip.strip()
	print len(ip)
	for i in range(len(ip)):
		print str(i) + " ** " + ip[i]
