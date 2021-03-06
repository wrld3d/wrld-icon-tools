<a href="http://www.wrld3d.com/">
    <img src="http://cdn2.eegeo.com/wp-content/uploads/2017/04/WRLD_Blue.png" align="right" height="80px" />
</a>

# WRLD Icon Conversion Tools

![WRLD](http://cdn2.eegeo.com/wp-content/uploads/2017/04/screenselection01.png)

* [Support](#support)
* [Getting Started](#getting-started)
* [Troubleshooting](#troubleshooting)
* [License](#license)

## Summary

This repository contains the code for preparing icons for use with the [WRLD SDK](http://www.wrld3d.com/), a cross-platform, OpenGL-based library for displaying beautiful, engaging 3D maps.

The code in this repository takes a set of vector icons in SVG format, converts them into bitmap images at resolutions suitable for a wide range of mobile devices and combines into "sheets" like for use by the WRLD SDK.

## Support

If you have any questions, bug reports, or feature requests, feel free to submit to the [issue tracker](https://github.com/wrld3d/wrld-icon-tools/issues) for this repository.

## Getting started

#### 1. Clone [this repo](https://github.com/wrld3d/wrld-icon-tools)

```
git clone https://github.com/wrld3d/wrld-icon-tools.git
```

#### 2. (Optional) Create a Python virtual environment to run the tools in.

Install `virtualenv` if required following [their instructions](https://virtualenv.pypa.io/en/stable/installation/), and then ensure you are in the top of the cloned repository.

```
virtualenv IconToolsVenv
source IconToolsVenv/bin/activate
```
#### 3. Install Inkscape

Download and installation instructions for various platforms are here: https://inkscape.org/en/download/

Here at WRLD we install using [MacPorts](https://www.macports.org/) on Mac OS-X and [Choclatey](https://chocolatey.org/) on Windows.

You may need to [add a path](https://mijingo.com/blog/adding-to-your-system-path) so your terminal has access to Inkscape commands.

#### 4. Install python dependencies.

```
pip install -r pip_requirements
```

#### 5. Build the icons for inclusion in mobile apps.

This tool prepares icon sheets for by the WRLD SDK on mobile devices. See the [WRLD Example App](https://github.com/wrld3d/wrld-example-app) for an example of a mobile app that uses the the WRLD SDK.

```
sh build_icons_for_example_app.sh
```

This will generate the bitmap icons at various resolutions along with icon sheets. You can find them in the output/ directory.

#### 6. Package up the icons for inclusion in mobile builds.

```
sh package_icons.sh
```

This packages up the icons for inclusion in a mobile app such as our [WRLD Example App](https://github.com/wrld3d/wrld-example-app)

Once this script has completed you will find the following directories under output/
* android/ - Contains assets/ and res/ for copying into Android apps, including search_tags.json
* ios/ - Contains assets to copy into the Resources directory of an Apple iOS App including search_tags.json
* windows/ - Contains assets to copy into the Resources directory of a Windows App.

#### 7. Building for [wrld-example-app](https://github.com/wrld3d/wrld-example-app)

If building for android move the android folder from `wrld-icon-tools/output/android` to `wrl-example-app/android`. In `wrl-example-app/android/android`, `sh update_android.sh` will copy the new icons into the directory.

If building for iOS move the ios folder from `wrld-icon-tools/output/ios` to `wrl-example-app/ios`. In `wrl-example-app/ios/ios`, `sh update_ios.sh` will copy the new icons into the directory and update 'CMakeLists.txt'.

#### 8. Building icons for inclusions in a web app.

This tool prepares icons for use by the WRLD SDK in browser based apps. You can find out more about building embeddable 3D mapping apps using Javascript and Leaflet on our website [here](https://docs.wrld3d.com/wrld.js/latest/docs/api/)

```
sh build_icons_for_webgl.sh
```

## Testing

If you wish to create a new WRLD places collection, then a tool has been included to add the contents of `data/search_tags.json` to a new places collection.

```
sh debug_icons_on_map.sh <DEVTOKEN>
```

Running the above command with your own developer token will create markers, and if you have successfully added the icons to your device and given the collection and device the same API Token you will see them at (56°27'50.4"N 2°56'03.0"W).

Adjust the values of `ZERO_LAT` and `ZERO_LON` before running `debug_icons_on_map.sh` if you wish the icons to be generated at different coordinates.

## Troubleshooting

If you can encounter an error similar to this on Mac platforms:

>Dynamic session lookup supported but failed: launchd did not provide a socket path, verify that org.freedesktop.dbus-session.plist is loaded!

You might need to start dbus with:

```
launchctl load -w /Library/LaunchAgents/org.freedesktop.dbus-session.plist
```

## License

The WRLD Icon Tools are  released under the Simplified BSD License. See the [LICENSE.md](https://github.com/wrld3d/wrld-icon-tools/blob/master/LICENSE) file for details.
