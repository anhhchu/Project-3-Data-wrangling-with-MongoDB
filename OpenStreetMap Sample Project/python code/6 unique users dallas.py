# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 17:26:54 2015

@author: jasmin may
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
"""
Your task is to explore the data a bit more.
The first task is a fun one - find out how many unique users
have contributed to the map in this particular area!

The function process_map should return a set of unique user IDs ("uid")
"""

def get_user(element):
    #print element

            
    return


def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        #print element #get["user"]
        if element.tag == "node":
            user = element.attrib['user']
            users.add(user)
        if element.tag == "way":
            user = element.attrib['user']
            users.add(user)
        if element.tag == "relation":
            user = element.attrib['user']
            users.add(user)
        pass

    return users


def test():

    users = process_map('D:\udacity_data_analysis\project3\P3\dallas_texas\dallas_texas.osm')
    print len(users)  
    #pprint.pprint(users)
    #assert len(users) == 6



if __name__ == "__main__":
    test()