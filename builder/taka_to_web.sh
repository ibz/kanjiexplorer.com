#!/bin/bash

echo "JSON..."

python3 builder/taka_to_json.py $1 $2

echo "JSON dict..."
python3 builder/taka_to_json_dict.py $1 $2

echo "SVG..."
python3 builder/taka_to_svg.py $1 $2
