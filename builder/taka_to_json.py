#!/usr/bin/python

from collections import defaultdict
import os
import json
import sys
import xml.parsers
from xml.dom import minidom

def load_elements(from_dir):
    elements = defaultdict(lambda: (set(), set()))
    for e in os.listdir(os.path.join(from_dir, "xml/element")):
        try:
            x = minidom.parse(os.path.join(from_dir, "xml/element/%s" % e))
        except xml.parsers.expat.ExpatError:
            continue
        element_id = int(x.getElementsByTagName('elementId')[0].childNodes[0].nodeValue)
        subelement_ids = [int(se.childNodes[0].nodeValue) for se in x.getElementsByTagName('pElementId')[0].getElementsByTagName('int')]
        subelement_ids = [s for s in subelement_ids if s != 0]
        elements[element_id][0].update(subelement_ids)
        for subelement_id in subelement_ids:
            elements[subelement_id][1].add(element_id)
    elements = dict((k, (list(v[0]), list(v[1]))) for k, v in elements.items())
    return elements

def main(from_dir, to_dir):
    elements = load_elements(from_dir)

    with open(os.path.join(to_dir, "elements.json"), "w") as f:
        f.write("var elements = %s;" % json.dumps(elements))

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
