#!/bin/bash

echo "Copying files from output android to android"
cp -R ./. ../

echo "Moving out of directory"
cd ..

echo "Removing cloned update_android.sh"
rm update_android.sh

echo "Removing android output folder"
rm -rf android
