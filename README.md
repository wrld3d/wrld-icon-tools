1. (Optional) Create a Python virtual environment.

virtualenv IconToolsVenv
source IconToolsVenv/bin/activate

2. Install Inkscape

Download and installation instructions for various platforms are here: https://inkscape.org/en/download/

Here at eeGeo we install using MacPorts on Mac OS-X and Choclatey on Windows.

3. Install python dependencies.

pip install -r pip_requirements

4. Build the icons for inclusion in mobile apps.

5. Building icons for inclusions in a web app.

Troubleshooting 

If you can encounter an error similar to this on Mac platforms:

Dynamic session lookup supported but failed: launchd did not provide a socket path, verify that org.freedesktop.dbus-session.plist is loaded!

You might need to start dbus with:

launchctl load -w /Library/LaunchAgents/org.freedesktop.dbus-session.plist




