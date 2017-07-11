#!/bin/bash

echo "Copying files from output ios to ios"
cp -R ./. ../

if [[ -e ../Resources/CMakeLists.txt ]]; then
  echo "Deleting old ../Resources/CMakeLists.txt"
  rm ../Resources/CMakeLists.txt
else
  echo "../Resources/CMakeLists.txt is not present"
fi

echo "Creating new ../Resources/CMakeLists.txt"
touch ../Resources/CMakeLists.txt

echo "Moving out of directory"
cd ..

echo "Removing cloned update_ios.sh"
rm update_ios.sh

echo "Moving back into directory"
cd ios || exit 1

echo "Populating CMakeLists.txt"
echo "set(resources \${resources}" >> ../Resources/CMakeLists.txt

function add_resource {
  echo "Adding: ${1:3}"
  echo "        ${1:3}" >> ../Resources/CMakeLists.txt
}

function loop_through_folder {
  for item in $1*; do
    add_resource $item
    if [ -d $item ]; then
      loop_through_folder "$1${item##*/}/"
    fi
  done
}

loop_through_folder ../Resources/

echo "        ExampleApp/Images.xcassets" >> ../Resources/CMakeLists.txt
echo ")" >> ../Resources/CMakeLists.txt
echo "CMakeLists.txt population complete"

echo "Moving out of directory"
cd ..

echo "Removing ios output folder"
rm -rf ios
