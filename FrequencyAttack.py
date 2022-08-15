#!/usr/bin/env python3

def main():
	f = open("cry100", "r")
	cb = f.read().lower()
	f.close()
	
	stat = {}
	for b in cb:
		if b.encode() in stat:
			stat[b.encode()] += 1
		else:
			stat[b.encode()] = 0

	replace = " OEUSLNADIB\nYHWRCTM_P?KFG3"#.lower()
	for eXchar in replace:
		maxChar = list(stat.keys())[0]
		for s in stat:
			if stat[s] > stat[maxChar]: maxChar = s
		print(f"{maxChar}({stat[maxChar]}) -> ", eXchar.encode())
		cb = cb.replace( maxChar.decode(), eXchar )
		stat[maxChar] = 0
	print("#"*50)
	# cb = cb.replace("!", "")
	# cb = cb.replace("^", "")
	# cb = cb.replace("◀", "{")
	# cb = cb.replace("▶", "}")
	print(cb.lower())


if __name__ == "__main__":
    main()
