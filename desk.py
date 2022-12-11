#!/usr/bin/env python3

import requests
import sys
import re
import random

flagRegEx = "[A-Z0-9]{31}="
port = None # define port of service
our_host = None # define it in attack sploit
DEBUG = True # dont forgot change it in attack sploit

alph = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM0123456789'

def idg( size = 8, chars=alph ):
	return ''.join( random.choice( chars ) for _ in range( size ) )

def login():
	pass

def register():
	pass

if __name__ == "__main__":

	if len( sys.argv ) > 1:
		host = sys.argv[ 1 ]
	else:
		print "Usage python " + sys.argv[ 0 ] + " <host>"
		sys.exit( -1 )

	if not our_host and not DEBUG:
		print "Set our_host var!!!!"
		sys.exit( -2 )
	if not port:
		print "Set port var!!!!"
		sys.exit( -3 )

	if host == our_host:
		sys.exit( -4 )

	host = 'http://' + host + ":" + str( port ) + "/"

	print(idg())
	
	# sys.stdout.flush() # after print
	# resp = requests.get( host )

	# find flags and print on stdout
	# flag_list = re.findall( flagRegEx, buf )
	# for flag in flag_list:
	#	print flag

	# POST requests
	# data = { 'key':'value', 'key1':'value1' }
	# res = requests.post( host + "some-url", data=data )


	# do not forgot about strip(), split(), replace() - functions to parsing