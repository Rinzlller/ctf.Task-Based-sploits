#!/usr/bin/env python3

# WORDLIST:	/usr/share/wordlists/rockyou.txt

# from urllib.parse import quote, unquote			#unquote("%2F")		quote("\")
# from html import unescape
# from hashlib import md5

# from pwn import *
# from os import system
# import requests
# from base64 import *
# from json import dumps, loads							#dumps({"key":"value"})

# import string

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

code = "ANEcwu4fYegObF1i2VXyvJHxKd0qBkMl36ILRaUjPG8rToSZzpCDt7n9mWsh5Q"

def main():

	ct = "9N_GN_tN_wu_qY_xi_Md_08_zfN_ctN_HQE_O7w_vnf_xZb_1Gv_VB6_y6f_lNG_H5N_0Nr_xNo_dBG_09j_rZI_QwB_122_CHT_tE1_qDO_emd_0Za_xuV_I2Y_Bxd_WG6_Okb_sgS_7cb_GPO_cSx_a0L_BRb_r0N_Ac1_Bli_4Rk_3fo_KfB_oj0_wOY_StI_acr"
	words = ct.split("_")
	nums = [0] * len(words)
	
	for i in range(len(words)):
		c = nums[i] = decrypt(words[i])
		if i > 2:
			c = (nums[i] - nums[i-1] - nums[i-2]) % 179179
		print(chr(c), end="")
	


def decrypt(word):
	num = 0
	for i in range(len(word)):
		num += code.index(word[i]) * pow(len(code), i)
	return num



if __name__ == "__main__":
	main()
