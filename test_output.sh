#!/bin/bash

function process_failure {
   echo "INSTALL FAILED AT setup-git.sh:$1"
   exit 1
}

echo "Beginning asset creation..."

trap 'process_failure $LINENO' ERR

rm -rf test

mkdir -p test/
python ./src/icons/icon_renderer.py -i data/icons/pin_sheet_input.json -s 2 -o test/pin_sheet -j test/pin_sheet.json
python ./src/icons/icon_renderer.py -i data/icons/icons_input.json -s 2 -o test/icon1_ -j test/icons.json

echo "Assets created for required resolutions in /output/"