#!/usr/bin/env python
#
# Title:      REST client
# Author:     Martin Brenner
#

import json, requests
import time


class restclient:

    def __init__(self):
	self.BASEURL="http://tecthulhu.boop.blue"


    def getjson(self):
        reqstr = self.BASEURL + "/module/status/json"
        print reqstr
        r = requests.get(reqstr)
        print "Status: ", r.status_code
        if r.status_code == requests.codes.ok:
            return r.json()
        else:
            return 0

    def main(self):
        json = rclient.getjson()
        if json != 0:
            print "JSON: ", json
            print "Faction:", json['status']['controllingFaction']
            print "Level:", json['status']['level']
            print "Health:", json['status']['health']
            print "Title:", json['status']['title']
            print "Resonators:", len(json['status']['resonators'])
            for i in range(0, len(json['status']['resonators'])):
                print json['status']['resonators'][i]['position']
        else:
            print "Error"

if __name__ =='__main__':
        rclient = restclient()
        rclient.main()



