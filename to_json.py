#!/usr/bin/python

from collections import defaultdict
import os
import simplejson
import sys
import xml.parsers
from xml.dom import minidom

def load_elements():
    elements = defaultdict(lambda: ([], []))
    for e in os.listdir("takadb/xml/element"):
        try:
            x = minidom.parse("takadb/xml/element/%s" % e)
        except xml.parsers.expat.ExpatError:
            continue
        element_id = int(x.getElementsByTagName('elementId')[0].childNodes[0].nodeValue)
        subelement_ids = [int(se.childNodes[0].nodeValue) for se in x.getElementsByTagName('pElementId')[0].getElementsByTagName('int')]
        subelement_ids = [s for s in subelement_ids if s != 0]
        elements[element_id][0].extend(subelement_ids)
        for subelement_id in subelement_ids:
            elements[subelement_id][1].append(element_id)
    return elements

def main():
    elements = load_elements()

    import pdb;pdb.set_trace()

    with file("web/elements.js", "w"):
        f.write(simplejson.dumps(elements))

if __name__ == '__main__':
    main()
