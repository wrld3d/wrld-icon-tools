#!/bin/bash

function process_failure {
   echo "INSTALL FAILED AT setup-git.sh:$1"
   exit 1
}

echo "Beginning Example App asset packaging..."

trap 'process_failure $LINENO' ERR

rm -rf output/ios
rm -rf output/android
rm -rf output/windows
rm -rf output/js

echo
echo
echo
echo "Packaging assets for iOS"
mkdir output/ios
mkdir output/ios/Resources
mkdir output/ios/Resources/SearchResultOnMap
python ./src/icons/icon_packer.py -i output/1x,output/2x,output/3x -o output/ios/Resources -f ios --json_pin_sheet output/1x/pin_sheet.json --json_icons output/1x/icons.json
cp data/search_tags.json output/ios/Resources/search_tags.json
cp ./update_ios.sh output/ios/update_ios.sh

echo
echo
echo
echo "Packaging assets for Android"
mkdir output/android
mkdir output/android/assets
mkdir output/android/assets/SearchResultOnMap
mkdir output/android/res
mkdir output/android/res/drawable-ldpi
mkdir output/android/res/drawable-mdpi
mkdir output/android/res/drawable-hdpi
mkdir output/android/res/drawable-xhdpi
mkdir output/android/res/drawable-xxhdpi
python ./src/icons/icon_packer.py -i output/0_75x,output/1x,output/1_5x,output/2x,output/3x -o output/android -f android --json_pin_sheet output/1x/pin_sheet.json --json_icons output/1x/icons.json
cp data/search_tags.json output/android/assets/search_tags.json
cp ./update_android.sh output/android/update_android.sh

echo
echo
echo
echo "Packaging assets for Windows"
mkdir output/windows
mkdir output/windows/Resources
mkdir output/windows/Resources/SearchResultOnMap
python ./src/icons/icon_packer.py -i output/1x,output/1_5x,output/2x -o output/windows/Resources -f windows --json_pin_sheet output/1x/pin_sheet.json --json_icons output/1x/icons.json
cp data/search_tags.json output/windows/Resources/search_tags.json

echo
echo
echo
echo "Packaging assets for Javascript"
mkdir output/js
python ./src/icons/icon_packer.py -i output/1x -o output/js -f js --json_pin_sheet output/1x/pin_sheet.json --json_icons output/1x/icons.json

echo
echo
echo
echo "Example App packaging completed!"
