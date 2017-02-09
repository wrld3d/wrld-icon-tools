#!/bin/bash

function process_failure {
   echo "INSTALL FAILED AT setup-git.sh:$1"
   exit 1
}

echo "Beginning asset creation..."

trap 'process_failure $LINENO' ERR

rm -rf output_webgl

mkdir -p output_webgl/
python ./src/icons/icon_renderer.py -i data/icons/pin_sheet_input_webgl.json -s 1 -o output_webgl/pin_sheet -j output_webgl/pin_sheet.json

echo "Assets created for required resolutions in /output_webgl/"