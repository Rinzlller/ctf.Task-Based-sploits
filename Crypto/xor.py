#! /usr/bin/python3

import os
import binascii

def main():

	flag = bytes.fromhex("65f32f851cdb20eee875eea5a9a30f826cfd247eb550dcc89d1d4cdf952f5c28ca5f162355567fd262bb96")
	some_simple_text = bytes.fromhex("70f8259330c137d4e873ff9ea6a559ab2dea1a60d943859aa545578395301d28a0741d1e065a24d45cb19f")

	FlagText = bytes.fromhex( xor(flag, some_simple_text) )

	flag = b'accessdenied{n3v3r_r3u53_th3_k3y5_'
	flag += b'_'*(43 - len(flag))
	some_simple_text = bytes.fromhex( xor(FlagText, flag) )
	print( some_simple_text[:34] )

	some_simple_text = b'this_is_not_the_real_flag,so_try_to_find_it'
	some_simple_text += b'_'*(43 - len(some_simple_text))
	flag = bytes.fromhex( xor(FlagText, some_simple_text) )
	print( flag[:25] )

	# flag 65f32f851cdb20eee875eea5a9a30f826cfd247eb550dcc89d1d4cdf952f5c28ca5f162355567fd262bb96
	# xored some_simple_text 70f8259330c137d4e873ff9ea6a559ab2dea1a60d943859aa545578395301d28a0741d1e065a24d45cb19f

	#accessdenied{bl1nd_bl1ndd_blinddd_sql_5fe2db70}
	#accessdenied{1nt3g3r_0v3rfl0w5_4r3_d4ng3r0u5_2d7b9a76}


def xor(plain_text, key):
    assert len(plain_text) == len(key)
    ciphertext = bytearray([a ^ b for a, b in zip(plain_text, key)])
    return ciphertext.hex()


if __name__ == "__main__":
    main()
