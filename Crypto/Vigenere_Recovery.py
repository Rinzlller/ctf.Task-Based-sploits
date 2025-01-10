#!/usr/bin/env python3

KEY_CHAR_CHOICE = 4
KEY_CHOICE = 16
KEY_LEN = 3

def main():

	print(50*"#")
	print("###" + 13*" " + "Vigenere Recovery!" +  13*" " + "###")
	print(50*"#")
	print()

	with open("CT.txt", "r") as f:
		ct = f.read()
	ct = ''.join(ct.split())

	# AVERAGE IC must be about 0.0686
	# (or choice the first MAX value)
	for key_len_i in range(1, KEY_CHOICE + 1):
		print( "{}\t|\t{:.4f}\t|".format(key_len_i, IC_average(ct, key_len_i)) )
	
	print()
	Chi_square_test(ct, KEY_LEN)


def IC_average(ct: str, key_len: int) -> int:

	ic = 0
	ic_average = 0
	for group_id in range(key_len):
		
		IDs = range(group_id, len(ct), key_len)
		group = [ct[id] for id in IDs]
		counts = [group.count(c) for c in set(group)]
		ic = sum([n*(n-1) for n in counts])/len(group)/(len(group)-1)
		ic_average += ic / key_len
	
	return ic_average


def Chi_square_test(ct: str, key_len: int):
	
	F = [
		0.0812, #a
		0.0149, #b
		0.0271, #c
		0.0432, #d
		0.1202, #e
		0.0230, #f
		0.0203, #g
		0.0592, #h
		0.0731, #i
		0.0010, #j
		0.0069, #k
		0.0398, #l
		0.0261, #m
		0.0695, #n
		0.0768, #o
		0.0182, #p
		0.0011, #q
		0.0602, #r
		0.0628, #s
		0.0910, #t
		0.0288, #u
		0.0111, #v
		0.0209, #w
		0.0017, #x
		0.0211, #y
		0.0007  #z
	]

	key = [[float('inf')] * 26 for i in range(key_len)]
	# key = ""

	for key_id in range(key_len):

		IDs = range(key_id, len(ct), key_len)
		group = [ct[id] for id in IDs]
		chi_square_min = float('inf')
		key_char = ""

		for shift in range(26):
			group_shift = [chr((ord(g)-65-shift)%26+65) for g in group]

			f = [0] * 26
			chi_square = 0
			for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
			# for c in set(group):
				f_i = group_shift.count(c)/len(group_shift)
				F_i = F[ord(c)-65]
				chi_square += pow(f_i - F_i, 2) / F_i

			# print( "{}\t{}\t{}".format(chr(shift+65), "".join(group_shift), chi_square) )
			key[key_id][shift] = chi_square
			# if chi_square < chi_square_min:
			# 	chi_square_min = chi_square
			# 	key_char = chr(shift+65)

		# key += key_char

	key_min = ""

	for key_id in range(key_len):

		key_details = [{'chi_square':x, 'shift':i} for i,x in enumerate(key[key_id])] 
		key_details.sort(key=lambda x: x['chi_square'])
		
		print(f"KEY[{key_id}]:")
		for details in key_details[:KEY_CHAR_CHOICE]:
			print( f"\t{chr(details['shift']+65)}\t{details['chi_square']}" )

		key_min += chr(key_details[0]['shift']+65)

	print()
	print(key_min)


if __name__ == "__main__":
	main()
