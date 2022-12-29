#!/usr/bin/env python3

import re

def main():
    f = open("strings", "r")
    file = f.read()
    f.close()
    
    strs = re.findall(r"db '(.*)',0", file)
    print(strs)


if __name__ == "__main__":
    main()
