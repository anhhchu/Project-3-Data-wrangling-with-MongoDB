# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 21:06:19 2015

@author: jasmin may
"""

"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "D:\udacity-data analysis\project 3\P3\dallas_texas.osm\dallas_texas.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", "Walk",
            "Trail", "Parkway", "Commons","Circle","Highway","Suit","Way","Turnpike","Trace","Tollway","Center","Bay","Expressway","Freeway","Run"]

# UPDATE THIS VARIABLE
mapping = { "St": "Street","St.": "Street",
            "Rd":"Road","Rd.":"Road","RD":"Road",
            "Ave":"Avenue","Av":"Avenue", "Ave.":"Avenue",
            "BLVD":"Boulevard","BLVD.":"Boulevard","Blvd":"Boulevard","Blvd.":"Boulevard","blvd":"Boulevard",
            "Dr":"Drive","Dr.":"Drive", "dr":"Drive", "Trl":"Trail",
            "pkwy":"Parkway", "Pkwy":"Parkway",
            "Hwy":"Highway","Hwy78":"Highway 78", "SH":"State Highway","TX":"Highway",
            "Fwy":"Freeway",
            "Cir":"Circle",
            "Ln":"Lane",
            "Pl":"Place",
            "Expessway":"Expressway","Expy":"Expressway",
            "N":"North","N.":"North","S":"South","S.":"South","W":"West","W.":"West","E":"East","E.":"East",
            "I":"Interstate", "i":"Interstate","FM":"Farm to Market","Farm-to-Market":"Farm to Market","Fm":"Farm to Market","CR":"County Road","U.S.":"US",
            "Sinder":"Snider"
            }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)
    


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")
    


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):                    
                    audit_street_type(street_types, tag.attrib['v'])

    return street_types


def update_name(name, mapping):

    # YOUR CODE HERE
    m = street_type_re.search(name)
    if m:
        street_type = m.group()
        #print m
    if street_type in mapping:
        new_street_type = mapping[street_type]
        name = name.replace(street_type, new_street_type)
    for key in mapping.keys():
        #print key
        if key in name:            
            for word in name.split():
                if word == key:
                    name = name.replace(word,mapping[key])
            for word in name.split("-"):
                if word == key:
                    name = name.replace(word,mapping[key])
                    name = name.replace("-"," ")

    return name


def test():
    st_types = audit(OSMFILE) #return the default dict of street type which doesn't match with expected
    #assert len(st_types) == 3
    #pprint.pprint(dict(st_types))

    for st_type, ways in st_types.iteritems(): #iter thru the dict
        for name in ways:
            better_name = update_name(name, mapping)
            print name + "=>" + better_name

    

if __name__ == '__main__':
    test()