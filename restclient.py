#!/usr/bin/env python
#
# Title:      REST client
# Author:     Martin Brenner
#

import json, requests
import time


class restclient:

    def __init__(self):
	#self.BASEURL="http://tecthulhu.boop.blue"
	#self.BASEURL="http://tecthulhuff.local/portals/Tecthulhu01.json"
	self.BASEURL="http://5.45.98.140:8080/module/status/json"


    def getjson(self):
        #reqstr = self.BASEURL + "/module/status/json"
	reqstr = self.BASEURL
        print reqstr
        r = requests.get(reqstr)
        #print "Status: ", r.status_code
        if r.status_code == requests.codes.ok:
            return r.json()
        else:
            return 0

    def main(self):
        json = rclient.getjson()
        if json != 0:
            print "JSON: ", json
	    if 0:
                print "Faction:", json['externalApiPortal']['controllingFaction']
                print "Level:", json['externalApiPortal']['level']
                print "Health:", json['externalApiPortal']['health']
                print "Title:", json['externalApiPortal']['title']
                print "Resonators:", len(json['externalApiPortal']['resonators'])
                for i in range(0, len(json['externalApiPortal']['resonators'])):
                    print json['externalApiPortal']['resonators'][i]['position']
            else:
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



