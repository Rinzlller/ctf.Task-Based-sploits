#!/usr/bin/env python3

import sys
import requests
import hashlib
import re
from random import choice
from time import sleep


alph_full = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
alph_caps = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
names = ['goliath', 'royal', 'dacota', 'marry', 'hunter', 'twilight' ,'smile' ,'castle', 'lucky', 'wolf']
FlagRegExp = re.compile(r'[A-Za-z0-9]{31}=')

#ip = sys.argv[1]
ip = '127.0.0.1'
port = '9990'
host = f'{ip}:{port}'


def id_gen( size = 10, first = names, next = alph_full ):
	beg = choice(first)
	return  beg + ''.join(choice(next) for i in range(size - len(beg)))


def main():

	while True:

		u_name = id_gen(next=alph_caps)
		passwd = id_gen(first=alph_full)
		
		register( u_name, passwd )
		sess = login( u_name, passwd )

		for i in range(50):
			create_club( sess )
		
		print( 'ok' )
		sleep( 15 )
		



def register( u_name, passwd ):
	#http://10.80.32.2:9990/zaregatsya | POST | {"имя":"hehehe","пароль":"hehehehehehe"}
	requests.post(f'http://{host}/zaregatsya', json={"имя":u_name,"пароль":passwd})


def login( u_name, passwd ):
	#http://10.80.32.2:9990/vhod | POST | {"имя":"hehehe","пароль":"hehehehehehe"}
	s = requests.session()
	s.post(f'http://{host}/vhod', json={"имя":u_name,"пароль":passwd})
	return s


def create_club( s ):
	#http://10.80.0.2:9990/novklub | POST | {"пароль":"123","профессия":"","название":""}
	name = id_gen(next=alph_caps)
	s.post(f'http://{host}/novklub', json={"пароль":"","профессия":"123","название":name})


if __name__ == '__main__':
	main()