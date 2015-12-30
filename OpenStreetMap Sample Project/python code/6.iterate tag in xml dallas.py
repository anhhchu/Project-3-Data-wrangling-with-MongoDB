# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 14:15:38 2015

@author: jasmin may
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Your task is to use the iterative parsing to process the map file and
find out not only what tags are there, but also how many, to get the
feeling on how much of which data you can expect to have in the map.
Fill out the count_tags function. It should return a dictionary with the 
tag name as the key and number of times this tag can be encountered in 
the map as value.

Note that your code will be tested with a different data file than the 'example.osm'
"""
import xml.etree.cElementTree as ET
import pprint


def count_tags(filename):
        # YOUR CODE HERE
        tree = ET.parse(filename)
        root = tree.getroot()
        #print root
        data ={}
        #print root.tag
        count = 1
        for elem in root.iter():
            #print elem
            tag = elem.tag
            attribute = elem.attrib
            print tag
            print attribute
            if tag not in data:
                data[tag]=count
                count=1
            elif tag in data:
                data[tag]=data[tag]+1

        return data


def test():

    tags = count_tags('D:\udacity-data analysis\project 3\P3\dallas_texas.osm\dallas_texas.osm')
    pprint.pprint(tags)

    

if __name__ == "__main__":
    test()