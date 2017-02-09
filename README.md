<a href="http://www.eegeo.com/">
    <img src="http://cdn2.eegeo.com/wp-content/uploads/2016/03/eegeo_logo_quite_big.png" alt="eeGeo Logo" title="eegeo" align="right" height="80px" />
</a>

# eeGeo Icon Conversion Tools

![eeGeo](http://cdn2.eegeo.com/wp-content/uploads/2016/03/readme-banner.jpg)

* [Support](#support)
* [Getting Started](#getting-started)
* [Troubleshooting](#troubleshooting)
* [License](#license)

### Summary

This repository contains the code for preparing icons for use with the [eeGeo SDK](http://www.eegeo.com/), a cross-platform, OpenGL-based library for displaying beautiful, engaging 3D maps.

The code in this repository takes a set of vector icons in SVG format, converts them into bitmap images at resolutions suitable for a wide range of mobile devices and combines into "sheets" like for use by the eeGeo SDK.

## Support

If you have any questions, bug reports, or feature requests, feel free to submit to the [issue tracker](https://github.com/eegeo/eegeo-icon-tools/issues) for this repository.

## Getting started

1. Clone this repo: `git clone https://github.com/eegeo/eegeo-icon-tools.git`
2. (Optional) Create a Python virtual environment to run the tools in.
```
virtualenv IconToolsVenv
source IconToolsVenv/bin/activate
```
3. Install Inkscape

Download and installation instructions for various platforms are here: https://inkscape.org/en/download/

Here at eeGeo we install using [MacPorts](https://www.macports.org/) on Mac OS-X and [Choclatey](https://chocolatey.org/) on Windows.

4. Install python dependencies.

```
pip install -r pip_requirements
```

4. Build the icons for inclusion in mobile apps.

5. Building icons for inclusions in a web app.

### Troubleshooting 

If you can encounter an error similar to this on Mac platforms:

>Dynamic session lookup supported but failed: launchd did not provide a socket path, verify that org.freedesktop.dbus-session.plist is loaded!

You might need to start dbus with:

```
launchctl load -w /Library/LaunchAgents/org.freedesktop.dbus-session.plist
````

## License

The eeGeo Icom Tools are  released under the Simplified BSD License. See the [LICENSE.md](https://github.com/eegeo/eegeo-icon-tools/blob/master/LICENSE) file for details.
