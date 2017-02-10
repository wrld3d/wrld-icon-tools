#!/bin/bash

function process_failure {
   echo "INSTALL FAILED AT setup-git.sh:$1"
   exit 1
}

echo "Beginning asset creation..."

trap 'process_failure $LINENO' ERR

rm -rf output/numbers

mkdir -p output/numbers/1x
python ./src/icons/icon_renderer.py -i data/icons/number_pins_input.json -s 1 -o output/numbers/1x/pin_sheet -j output/numbers/1x/pin_sheet_numbers.json
python ./src/icons/icon_renderer.py -i data/icons/number_icons_input.json -s 1 -o output/numbers/1x/icon1_ -j output/numbers/1x/icons_numbers.json

mkdir -p output/numbers/2x
python ./src/icons/icon_renderer.py -i data/icons/number_pins_input.json -s 2 -o output/numbers/2x/pin_sheet -j output/numbers/2x/pin_sheet_numbers.json
python ./src/icons/icon_renderer.py -i data/icons/number_icons_input.json -s 2 -o output/numbers/2x/icon1_ -j output/numbers/2x/icons_numbers.json

mkdir -p output/numbers/3x
python ./src/icons/icon_renderer.py -i data/icons/number_pins_input.json -s 3 -o output/numbers/3x/pin_sheet -j output/numbers/3x/pin_sheet_numbers.json
python ./src/icons/icon_renderer.py -i data/icons/number_icons_input.json -s 3 -o output/numbers/3x/icon1_ -j output/numbers/3x/icons_numbers.json

echo "Assets created for required resolutions in /output/"
echo "Packaging assets"

rm -rf output/numbers/ios

echo "Packaging assets for iOS"
mkdir output/numbers/ios
mkdir output/numbers/ios/SearchResultOnMap
python ./src/icons/icon_packer.py -i output/numbers/1x,output/numbers/2x,output/numbers/3x -o output/numbers/ios -f ios --json_pin_sheet output/numbers/1x/pin_sheet_numbers.json --json_icons output/numbers/1x/icons_numbers.json