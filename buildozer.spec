[app]
# (str) Title of your application
 title = Oishi Love
# (str) Package name
package.name = oishilove
# (str) Package domain
package.domain = org.omar
# (str) Source code where main.py lives
source.dir = .
# (str) Application version
version = 1.0
# (str) Supported source extensions
source.include_exts = py,png,jpg,jpeg,gif,ppm,pgm,wav,ttf
# (str) Presplash
# presplash.filename = %(source.dir)s/presplash.png
# (str) Icon
# icon.filename = %(source.dir)s/icon.png
# (str) Application requirements
requirements = python3,kivy
# (str) Supported orientation
orientation = portrait
fullscreen = 1
# (list) List of service to start on boot
services =

[buildozer]
# (str) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2
# (str) Warn on root usage
warn_on_root = 1

[app:android]
# (str) Android API target
android.api = 35
android.minapi = 23
android.archs = arm64-v8a,armeabi-v7a
android.accept_sdk_license = True
android.enable_androidx = True

[app:python]
python.minimum_version = 3.8
