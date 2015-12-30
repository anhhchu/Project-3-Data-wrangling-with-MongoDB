#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
"""
Your task is to wrangle the data and transform the shape of the data
into the model we mentioned earlier. The output should be a list of dictionaries
that look like this:

{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

You have to complete the function 'shape_element'.
We have provided a function that will parse the map file, and call the function with the element
as an argument. You should return a dictionary, containing the shaped data for that element.
We have also provided a way to save the data in a file, so that you could use
mongoimport later on to import the shaped data into MongoDB. 

Note that in this exercise we do not use the 'update street name' procedures
you worked on in the previous exercise. If you are using this code in your final
project, you are strongly encouraged to use the code from previous exercise to 
update the street names before you save them to JSON. 

In particular the following things should be done:
- you should process only 2 types of top level tags: "node" and "way"
- all attributes of "node" and "way" should be turned into regular key/value pairs, except:
    - attributes in the CREATED array should be added under a key "created"
    - attributes for latitude and longitude should be added to a "pos" array,
      for use in geospacial indexing. Make sure the values inside "pos" array are floats
      and not strings. 
- if second level tag "k" value contains problematic characters, it should be ignored
- if second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
- if second level tag "k" value does not start with "addr:", but contains ":", you can process it
  same as any other tag.
- if there is a second ":" that separates the type/direction of a street,
  the tag should be ignored, for example:

<tag k="addr:housenumber" v="5158"/>
<tag k="addr:street" v="North Lincoln Avenue"/>
<tag k="addr:street:name" v="Lincoln"/>
<tag k="addr:street:prefix" v="North"/>
<tag k="addr:street:type" v="Avenue"/>
<tag k="amenity" v="pharmacy"/>

  should be turned into:

{...
"address": {
    "housenumber": 5158,
    "street": "North Lincoln Avenue"
}
"amenity": "pharmacy",
...
}

- for "way" specifically:

  <nd ref="305896090"/>
  <nd ref="1719825889"/>

should be turned into
"node_refs": ["305896090", "1719825889"]
"""


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
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

    
def update_zipcode(zip_code):
    if zip_code.startswith("7")==False:
       zip_code = zip_code.replace("TX ","")                  
    if len(zip_code) > 5:
       zip_code = zip_code[:5]
    if len(zip_code) <5:
       zip_code = "NULL"      
    return zip_code


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
    
def update_number(number):
    num_list = re.findall(r'\d+',number)
    #print num_list
    if num_list[0] == '1' or num_list[0] == '01' or num_list[0]=="011":
        num_list.remove(num_list[0])
    number = '-'.join(num_list)
    
    if len(number)>12:
        number = number[:12]
    
    return number

created_list = [ "version", "changeset", "timestamp", "user", "uid"]
fields = ["id","visible"] 

def shape_element(element):
    #print element.tag
    node = {}
    created = {}
    pos = []
    
    if element.tag == "node" or element.tag == "way" :
        #print element.attrib['visible']
        # YOUR CODE HERE
        node["type"] = element.tag
        for field in fields:
            if field in element.attrib:
                node[field] = element.attrib[field]
                
        if "lat" and "lon" in element.attrib:
            pos.append(float(element.attrib["lat"]))
            pos.append(float(element.attrib["lon"]))            
            node["pos"] = pos
            
        for create in created_list:
            created[create] = element.attrib[create]
        node["created"] = created
        
        node_refs = []
        for nd in element.iter("nd"):           
            ref = nd.attrib["ref"]
            node_refs.append(ref)
            node["node_refs"] = node_refs
        address = {}
        for tag in element.iter("tag"):
            k = tag.attrib['k']
            if k== "addr:street":                              
                tag.attrib['v']  = update_name(tag.attrib['v'], mapping)
            if k =="addr:postcode" or k=='tiger:zip_left' or k =='tiger:zip_right':                
                tag.attrib['v'] = update_zipcode(tag.attrib['v'])    
            if k == "population":
                tag.attrib['v'] = int(tag.attrib['v'])
            if k == "phone":
                tag.attrib['v'] = update_number(tag.attrib['v'])   
            if k.startswith("addr:"):
                key = k[5:]
                if ":" not in key:
                    address[key] = tag.attrib['v']
            elif k.startswith("tiger:"):
                if k == "tiger:county" or k == "tiger:zip_left" or k == "tiger:zip_right":                     
                    node[k[6:]] = tag.attrib['v'] 
            elif k.startswith("gnis:"):
                if k == "gnis:Class" or k == "gnis:County": 
                    node[k[5:]] = tag.attrib['v']
            else:
                node[k] = tag.attrib['v']
            node['address'] = address
                    
        if "address" in node:
            if not address:
               del node["address"]
        
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            pprint.pprint(el)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data


def test():
    # NOTE: if you are running this code on your computer, with a larger dataset, 
    # call the process_map procedure with pretty=False. The pretty=True option adds 
    # additional spaces to the output, making it significantly larger.
    data = process_map('D:\udacity_data_analysis\project3\P3\dallas_texas\sample.osm', False)
    #pprint.pprint(data)
    
    

if __name__ == "__main__":
    test()