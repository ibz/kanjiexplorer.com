#!/usr/bin/python

from collections import defaultdict
import os
import simplejson
import sys
import xml.parsers
from xml.dom import minidom

def load_elements():
    elements = defaultdict(lambda: (set(), set()))
    for e in os.listdir("takadb/xml/element"):
        try:
            x = minidom.parse("takadb/xml/element/%s" % e)
        except xml.parsers.expat.ExpatError:
            continue
        element_id = int(x.getElementsByTagName('elementId')[0].childNodes[0].nodeValue)
        subelement_ids = [int(se.childNodes[0].nodeValue) for se in x.getElementsByTagName('pElementId')[0].getElementsByTagName('int')]
        subelement_ids = [s for s in subelement_ids if s != 0]
        elements[element_id][0].update(subelement_ids)
        for subelement_id in subelement_ids:
            elements[subelement_id][1].add(element_id)
    elements = dict((k, (list(v[0]), list(v[1]))) for k, v in elements.iteritems())
    return elements

def main():
    elements = load_elements()

    with file("web/elements.json", "w") as f:
        f.write("var elements = %s;" % simplejson.dumps(elements))

if __name__ == '__main__':
    main()
