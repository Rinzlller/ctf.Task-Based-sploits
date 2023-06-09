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
port = '5555'
host = f'{ip}:{port}'


def id_gen( size = 10, first = names, next = alph_full ):
	beg = choice(first)
	return  beg + ''.join(choice(next) for i in range(size - len(beg)))


def main():

	for _i in range(40):

		u_name = id_gen(next=alph_caps)
		passwd = id_gen(first=alph_full)
		
		register( u_name, passwd )
		sess = login( u_name, passwd )
		
		add_icecream( sess )


def register( u_name, passwd ):
	#http://10.10.228.14:5555/registerForm?login=asvdv&password=3246326
	requests.get(f'http://{host}/registerForm?login={u_name}&password={passwd}')#, data = {'login':u_name, 'password':passwd})


def login( u_name, passwd ):
	#http://10.10.228.14:5555/loginForm?login=asdv&password=1234
	s = requests.session()
	s.get(f'http://{host}/loginForm?login={u_name}&password={passwd}')#, data = {'login':u_name, 'password':passwd})
	return s


def add_icecream( s ):
	#http://10.10.228.22:5555/addForm?icecream=text
	flag = id_gen(first=['I'], size=31, next=alph_caps) + '='
	s.get(f'http://{host}/addForm?icecream={flag}')


if __name__ == '__main__':
	main()