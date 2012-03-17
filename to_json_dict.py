#!/usr/bin/python

from collections import defaultdict
from xml.etree import ElementTree
import xml.parsers
import os
import simplejson
import sys

def load_characters():
    elements = {}
    for filename in os.listdir("takadb/xml/character"):
        with file("takadb/xml/character/%s" % filename) as f:
            x = ElementTree.fromstring(f.read().decode("utf-8", "ignore").encode("utf-8"))

        element_id = int(x.find("jaElementId").text)
        character = unichr(int(x.find("jaUcsCode").text))
        readings = [(r.find("jpReadingType").text, r.find("sourceReading").text) for r in x.findall("readings/SLCMap/entry/map/entry/reading")]
        meanings = "; ".join(e.find("meaning/destMeaning").text for e in x.findall("meanings/identifierMap/entry") if e.find('identifier/destLanguageCode').text == "en" and e.find("meaning/destMeaning").text)

        if element_id not in elements:
            elements[element_id] = {'readings': readings, 'meanings': meanings, 'character': character}
        else:
            elements[element_id]['readings'].extend(readings)
            elements[element_id]['meanings'] += "; " + meanings
            elements[element_id]['character'] += "; " + character

    for element_id in elements:
        readings_dict = {}
        for type, reading in elements[element_id]['readings']:
            if type not in readings_dict:
                readings_dict[type] = reading
            else:
                readings_dict[type] += "; " + reading
        elements[element_id]['readings'] = readings_dict

    return elements

def main():
    elements = load_characters()

    for element_id, element in elements.iteritems():
        with file("web/dict/%s.json" % element_id, "w") as f:
            f.write(simplejson.dumps(element))

if __name__ == '__main__':
    main()
