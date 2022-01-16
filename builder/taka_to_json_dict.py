#!/usr/bin/python

from collections import defaultdict
from xml.etree import ElementTree
import xml.parsers
import os
import json
import sys

def load_characters(from_dir):
    elements = {}
    for filename in os.listdir(os.path.join(from_dir, "xml/character")):
        with open(os.path.join(from_dir, "xml/character/%s" % filename)) as f:
            try:
                x = ElementTree.fromstring(f.read().encode("utf-8"))
            except UnicodeDecodeError:
                print("failed to decode: %s" % filename)
                continue

        element_id = int(x.find("jaElementId").text)
        character = chr(int(x.find("jaUcsCode").text))
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

def main(from_dir, to_dir):
    elements = load_characters(from_dir)

    if not os.path.exists(os.path.join(to_dir, "dict")):
        os.mkdir(os.path.join(to_dir, "dict"))

    for element_id in range(1, max(elements) + 1):
        with open(os.path.join(to_dir, "dict/%s.json" % element_id), "w") as f:
            f.write(json.dumps(elements.get(element_id, {})))

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
