#!/bin/bash

function process_failure {
   echo "INSTALL FAILED AT setup-git.sh:$1"
   exit 1
}

echo "Beginning asset creation..."

trap 'process_failure $LINENO' ERR

rm -rf output

mkdir -p output/1x
python ./src/icons/icon_renderer.py -i data/icons/pin_sheet_input.json -s 1 -o output/1x/pin_sheet -j output/1x/pin_sheet.json
python ./src/icons/icon_renderer.py -i data/icons/icons_input.json -s 1 -o output/1x/icon1_ -j output/1x/icons.json

mkdir -p output/2x
python ./src/icons/icon_renderer.py -i data/icons/pin_sheet_input.json -s 2 -o output/2x/pin_sheet -j output/2x/pin_sheet.json
python ./src/icons/icon_renderer.py -i data/icons/icons_input.json -s 2 -o output/2x/icon1_ -j output/2x/icons.json

mkdir -p output/3x
python ./src/icons/icon_renderer.py -i data/icons/pin_sheet_input.json -s 3 -o output/3x/pin_sheet -j output/3x/pin_sheet.json
python ./src/icons/icon_renderer.py -i data/icons/icons_input.json -s 3 -o output/3x/icon1_ -j output/3x/icons.json

mkdir -p output/0_75x
python ./src/icons/icon_renderer.py -i data/icons/pin_sheet_input.json -s 0.75 -o output/0_75x/pin_sheet -j output/0_75x/pin_sheet.json
python ./src/icons/icon_renderer.py -i data/icons/icons_input.json -s 0.75 -o output/0_75x/icon1_ -j output/0_75x/icons.json

mkdir -p output/1_5x
python ./src/icons/icon_renderer.py -i data/icons/pin_sheet_input.json -s 1.5 -o output/1_5x/pin_sheet -j output/1_5x/pin_sheet.json
python ./src/icons/icon_renderer.py -i data/icons/icons_input.json -s 1.5 -o output/1_5x/icon1_ -j output/1_5x/icons.json

echo "Assets created for required resolutions in /output/"