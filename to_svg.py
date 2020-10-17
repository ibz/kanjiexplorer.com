#!/usr/bin/python

from collections import defaultdict
import os
import json
import sys
import xml.parsers
from xml.dom import minidom

def get_int(e):
    return int(e.childNodes[0].nodeValue)

def get_float(e):
    return float(e.childNodes[0].nodeValue)

def load_elements():
    elements = {}

    for filename in os.listdir("takadb/xml/element"):
        try:
            x = minidom.parse("takadb/xml/element/%s" % filename)
        except xml.parsers.expat.ExpatError:
            continue
        element_id = int(x.getElementsByTagName('elementId')[0].childNodes[0].nodeValue)

        variants = {}
        variant_elements = x.getElementsByTagName('glyphs')[0].getElementsByTagName('variantMap')[0].getElementsByTagName('entry')
        for e in variant_elements:
            variant_id = int(e.getElementsByTagName('int')[0].childNodes[0].nodeValue)
            centre_point = int(e.getElementsByTagName('centrePoint')[0].childNodes[0].nodeValue)
            height = int(e.getElementsByTagName('height')[0].childNodes[0].nodeValue)
            width = int(e.getElementsByTagName('width')[0].childNodes[0].nodeValue)
            standalone = e.getElementsByTagName('standalone')[0].childNodes[0].nodeValue == "true"
            subelement_variants = map(get_int, e.getElementsByTagName('pGlyphVariant')[0].getElementsByTagName('int'))
            subelement_heights = map(get_int, e.getElementsByTagName('pHeight')[0].getElementsByTagName('int'))
            subelement_widths = map(get_int, e.getElementsByTagName('pWidth')[0].getElementsByTagName('int'))
            subelement_xs = map(get_int, e.getElementsByTagName('pX')[0].getElementsByTagName('int'))
            subelement_ys = map(get_int, e.getElementsByTagName('pY')[0].getElementsByTagName('int'))

            strokes = []
            stroke_elements = e.getElementsByTagName('strokes')[0].getElementsByTagName('stroke')
            for se in stroke_elements:
                segments = [{'t': el.getElementsByTagName('type')[0].childNodes[0].nodeValue,
                             'p': [get_float(p) for p in el.getElementsByTagName('points')[0].getElementsByTagName('float') if get_float(p) != 0]}
                            for el in se.getElementsByTagName('segment')]
                strokes.append(segments)

            variants[variant_id] = {'centre_point': centre_point, 'height': height, 'width': width, 'standalone': standalone,
                                    'subelement_variants': subelement_variants, 'subelement_heights': subelement_heights, 'subelement_widths': subelement_widths,
                                    'subelement_xs': subelement_xs, 'subelement_ys': subelement_ys,
                                    'strokes': strokes}

        subelement_ids = map(get_int, x.getElementsByTagName('pElementId')[0].getElementsByTagName('int'))

        elements[element_id] = {'subelements': subelement_ids, 'variants': variants}
    return elements

SVG = """<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="100%%" height="100%%">
<style type="text/css"><![CDATA[
  .stroke { fill:none; stroke:black; stroke-width:2 }
]]></style>
%s
</svg>
"""

STROKE_SVG = """<path class="stroke" d="%s" />"""

def get_stroke_svg(s):
    return STROKE_SVG % " ".join("%s %s" % (segment['t'], " ".join(map(str, segment['p']))) for segment in s)

def transform_stroke(s, transform, transform_arg):
    return [{'t': segment['t'], 'p': [transform(segment['p'][i], transform_arg[i % 2]) for i in range(len(segment['p']))]} for segment in s]

def translate_strokes(strokes, translation):
    return [transform_stroke(s, lambda n, s: n + s, translation) for s in strokes]

def scale_strokes(strokes, scale):
    return [transform_stroke(s, lambda n, s: n * s, scale) for s in strokes]

def get_element_strokes(elements, element_id, variant_id, width, height, outer):
    element = elements[element_id]
    variant = element['variants'][variant_id]

    scale = (float(width) / float(variant['width']), float(height) / float(variant['height']))

    if variant['standalone']:
        strokes = variant['strokes']
    else:
        strokes = []
        for i, subelement_id in enumerate(element['subelements']):
            if subelement_id == 0:
                continue
            subelement_strokes = get_element_strokes(elements, subelement_id, variant['subelement_variants'][i], variant['subelement_widths'][i], variant['subelement_heights'][i], False)
            subelement_strokes = translate_strokes(subelement_strokes, (variant['subelement_xs'][i], variant['subelement_ys'][i]))
            strokes.extend(subelement_strokes)

    if not outer:
        strokes = scale_strokes(strokes, scale)

    return strokes

def get_svg(elements, element_id):
    strokes = get_element_strokes(elements, element_id, 1, 100, 100, True)
    return SVG % "\n".join(get_stroke_svg(s) for s in strokes)

def main():
    elements = load_elements()

    if not os.path.exists("web/svg"):
        os.mkdir("web/svg")

    for element_id in elements:
        with file("web/svg/%s.svg" % element_id, "w") as f:
            f.write(get_svg(elements, element_id))

if __name__ == '__main__':
    main()
