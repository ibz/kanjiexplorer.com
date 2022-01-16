#!/bin/bash

echo "JSON..."

python /builder/taka_to_json.py /taka /web

echo "JSON dict..."
python /builder/taka_to_json_dict.py /taka /web

echo "SVG..."
python /builder/taka_to_svg.py /taka /web
