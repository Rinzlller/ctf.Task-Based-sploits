#!/usr/bin/env python3

import re

def main():
    f = open("/home/rinzler/Downloads/flags", "r")
    file = f.read()
    f.close()
    
    for str in file.split("malloc(20)"):
	    flag = re.findall(r"fputc\('(.*)',", str)
	    print("".join(flag))


if __name__ == "__main__":
    main()
