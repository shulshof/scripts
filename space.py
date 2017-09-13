
import untangle
import requests
import argparse
import getpass



def main():

	# use argparse to acquire host, user and device to look for
	parser = argparse.ArgumentParser(description='Find ip from space based on hostname')
	parser.add_argument("-s",'--space',help="IP/Hostname of space")
	parser.add_argument('-u','--user',help='Space username')
	parser.add_argument('-d','--device',help='Device to acquire IP')
	args = parser.parse_args()

	# get the static vars ready

	URL = "https://" + args.space + "/api/space/device-management/devices/"
	USER = args.user
	DEVICE = args.device 

	# ask for password
	PASS = getpass.getpass(prompt='Enter space user password:')

	# disable invalid cert warning
	requests.packages.urllib3.disable_warnings()
	
	# connect to space
	r = requests.get(URL, auth=(USER, PASS), verify=False)
	
	#make sure we get status code 200 or we quit with error
	if r.status_code != 200:
		print "Could not connect to space, status code: " + str(r.status_code)
		exit(1)
	
	#take in XML code and parse
	result = untangle.parse(r.text.encode("ascii"))
	
	# iterate over the devices and look for the supplied named
	for d in result.devices.device:
		name = d.name.cdata
		ip = d.ipAddr.cdata
		# make sure we lowercase the results and the supplied name
		if DEVICE.lower() == name.lower():
			print "Host " + DEVICE + " IP is: " + ip
			exit(0)

			
	# we did not find what we were looking for
	print "Host: " + DEVICE + " not found!"
	exit(1)
	 


if __name__ == "__main__":
    main()




