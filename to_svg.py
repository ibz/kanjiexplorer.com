#!/usr/bin/python

from collections import defaultdict
import os
import simplejson
import sys
import xml.parsers
from xml.dom import minidom

def load_elements():
    elements = defaultdict(dict)

    for e in os.listdir("takadb/xml/element"):
        try:
            x = minidom.parse("takadb/xml/element/%s" % e)
        except xml.parsers.expat.ExpatError:
            continue
        element_id = int(x.getElementsByTagName('elementId')[0].childNodes[0].nodeValue)
        subelement_ids = [int(se.childNodes[0].nodeValue) for se in x.getElementsByTagName('pElementId')[0].getElementsByTagName('int')]
        subelement_ids = [s for s in subelement_ids if s != 0]

        pattern = x.getElementsByTagName('pattern')
        if pattern and pattern[0].childNodes:
            pattern = pattern[0].childNodes[0].nodeValue
        else:
            pattern = None

        standalone = x.getElementsByTagName('standalone')[0].childNodes[0].nodeValue == "true"

        strokes = []
        stroke_elements = x.getElementsByTagName('strokes')[0].getElementsByTagName('stroke')
        for e in stroke_elements:
            segments = [{'t': el.getElementsByTagName('type')[0].childNodes[0].nodeValue,
                         'p': [p.childNodes[0].nodeValue for p in el.getElementsByTagName('points')[0].getElementsByTagName('float') if float(p.childNodes[0].nodeValue) != 0]}
                         for el in e.getElementsByTagName('segment')]
            strokes.append(segments)

        elements[element_id] = {'strokes': strokes, 'sub_elements': subelement_ids, 'pattern': pattern, 'standalone': standalone}
    return elements

SVG = """<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg xmlns="http://www.w3.org/2000/svg" version="1.1">
<style type="text/css"><![CDATA[
  .stroke { fill:none; stroke:black; stroke-width:5 }
]]></style>
%s
</svg>
"""

STROKE_SVG = """<path class="stroke" d="%s" />"""

def get_stroke_svg(s):
    return STROKE_SVG % " ".join("%s %s" % (segment['t'], " ".join(segment['p'])) for segment in s)

def get_element_svg(elements, element_id):
    element = elements[element_id]
    if element['standalone']:
        return "\n".join(get_stroke_svg(s) for s in element['strokes'])
    else:
        return "\n\n".join(get_element_svg(elements, subelement_id) for subelement_id in element['sub_elements'])

def get_svg(elements, element_id):
    return SVG % get_element_svg(elements, element_id)

def main():
    elements = load_elements()

    for element_id in elements:
        with file("svg/%s.svg" % element_id, "w") as f:
            f.write(get_svg(elements, element_id))

if __name__ == '__main__':
    main()
