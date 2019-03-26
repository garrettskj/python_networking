#!/usr/bin/python3

'''
Let's make a subnet calculator

this is based off the subnet calculator lesson from 
TrendElearning
- Updated for Python3
- Updated to be functional
- additional comments and exception handling was added.
'''

import random
import sys

def get_ip_address():
	#Checking IP address validity
	while True:
		try:
			ip_address = input("Enter an IP address: ")
			
			#Checking octets			
			a = ip_address.split('.')
						
			# do a ghetto check to see if it "looks about right"
			# there needs to be only 4 octets after the split
			# the first octet needs to between 1 and 223
			# the first octet can't be 127
			# the first two octets can't be 169.254
			# the last three octets need to be between 0 and 255
			if (len(a) == 4) and (1 <= int(a[0]) <= 223) and (int(a[0]) != 127) and (int(a[0]) != 169 or int(a[1]) != 254) and (0 <= int(a[1]) <= 255 and 0 <= int(a[2]) <= 255 and 0 <= int(a[3]) <= 255):
				break
			
			else:
				print("\nThe IP address is INVALID! Please retry with a valid IPV4 address!\n")
				continue

		except ValueError:
			print("\nThe IP address is INVALID! Please retry with a valid IPV4 address!\n")

	return ip_address

def get_subnet_mask():

	masks = [255, 254, 252, 248, 240, 224, 192, 128, 0]
	
	#Checking Subnet Mask validity
	while True:

		try:
			subnet_mask = input("Enter a subnet mask: ")
			
			#Checking octets			
			b = subnet_mask.split('.')

			# just like the IP address checks:
			# make sure it's 4 octets
			# make sure that the first octet is 255
			## this only handles a /8 and higher.
			# make sure that each octet is found in the masks list above.
			# do a ghetto ordering, just to make sure that it's not 'oddly' masked.
			# 255.255.254.255 <- this is a valid mask, but not in this example

			if (len(b) == 4) and (int(b[0]) == 255) and (int(b[1]) in masks) and (int(b[2]) in masks) and (int(b[3]) in masks) and (int(b[0]) >= int(b[1]) >= int(b[2]) >= int(b[3])):
				break
			
			else:
				print("\nThe mask is INVALID! Please retry with a valid Subnet Mask!\n")
				continue

		except ValueError:
			print("\nThe mask is INVALID! Please retry with a valid Subnet Mask!\n")

	return subnet_mask

def convert_ip_to_binary(ip):

	#First let's break apart the octets
	octets_padded = []
	octets_decimal = ip.split(".")
		
	# for each octet	
	for octet in octets_decimal:
		
		# convert to binary
		# grab the binary number string after the 'b'
		binary_octet = bin(int(octet)).split("b")[1]
		
		# if it's a full 8 num, just add it as-is
		if len(binary_octet) == 8:
			pass		
		#otherwise, fill in the zeros
		elif len(binary_octet) < 8:
			binary_octet = binary_octet.zfill(8)
		
		octets_padded.append(binary_octet)

	full_binary_string = "".join(octets_padded)
	#print(decimal_string)   #Example: for 255.255.255.0 => 11111111111111111111111100000000
	
	#Counting host bits in the mask and calculating number of hosts/subnet
	#no_of_zeros = full_binary_string.count("0")
	#no_of_ones = 32 - no_of_zeros
	#no_of_hosts = abs(2 ** no_of_zeros - 2) #return positive value for mask /32

	return full_binary_string

def get_wildcard_mask(subnet_mask):

	# We don't need to do subnet mask validation here, because it was already checked above.
	octet_list = subnet_mask.split('.')

	# For each octet, subtract it from 255
	wildcard_octets = []
	for w_octet in octet_list:
		wild_octet = 255 - int(w_octet)
		wildcard_octets.append(str(wild_octet))
		
	wildcard_mask = ".".join(wildcard_octets)
	
	return wildcard_mask

def binary_addr_to_dec(binary_addr):

	# using the binary address, slice up every 8 numbers
	net_ip_octets = []
	for octet in range(0, len(binary_addr), 8):
		net_ip_octet = binary_addr[octet:octet+8]
		net_ip_octets.append(net_ip_octet)
	
	# time to convert back to decimal
	net_ip_address = []
	for each_octet in net_ip_octets:
		net_ip_address.append(str(int(each_octet, 2)))
		
	# let's get a readable address
	network_address = ".".join(net_ip_address)
	
	return network_address

def get_network_range(binary_ip, binary_submask):
	''' returns back the first address, broadcast address, number of hosts, and the CIDR mask'''

	# count the number of zeros in the binary mask
	no_of_zeros = binary_submask.count("0")
	
	# Next get the CIDR count, based on those 0s
	no_of_ones = 32 - no_of_zeros

	no_of_hosts = abs(2 ** no_of_zeros - 2) #return positive value for mask /32

	# Get the first address, by only looking at the network range slice and adding 0*8
	network_address_binary = binary_ip[:(no_of_ones)] + "0" * no_of_zeros
	
	# get the last address, by adding 1*8
	broadcast_address_binary = binary_ip[:(no_of_ones)] + "1" * no_of_zeros

	first_address = binary_addr_to_dec(network_address_binary)

	last_address = binary_addr_to_dec(broadcast_address_binary)

	return [first_address, last_address, no_of_hosts, no_of_ones]

def subnet_calc():
	try:
		print("\n")
		
		ip_address = get_ip_address()
		
		subnet_mask = get_subnet_mask()

		binary_submask = convert_ip_to_binary(subnet_mask)

		binary_ip = convert_ip_to_binary(ip_address)

		wildcard_mask = get_wildcard_mask(subnet_mask)

		network_range = get_network_range(binary_ip, binary_submask)

		############# Application #1 - Part #3 #############

		#Results for selected IP/mask
		print("\n")
		print(f"Network address is: {network_range[0]}")
		print(f"Broadcast address is: {network_range[1]}")
		print(f"Number of valid hosts per subnet: {network_range[2]}")
		print(f"Wildcard mask: %s" % wildcard_mask)
		print(f"Mask bits: {network_range[3]}")
		print("\n")

	except KeyboardInterrupt:
		print("\n\nProgram aborted by user. Exiting...\n")
		sys.exit()
		
#Calling the function

if __name__ == '__main__':
	subnet_calc()