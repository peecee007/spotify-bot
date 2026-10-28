[app]

# (str) Title of your app
title = Spotify Bot

# (str) Package name
package.name = spotifybot

# (str) Package domain
package.domain = org.kivy

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) Source files to exclude (let empty to not exclude anything)
source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
source.exclude_dirs = tests, bin

# (list) List of exclusions using pattern matching
source.exclude_patterns = license,images/*/*.jpg

# (str) Icon of the application
icon.filename = %(source.dir)s/data/icon.png

# (str) Supported android version
android.api = 30

# (int) Android min API to use
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 30

# (str) Android NDK version to use
android.ndk = 21

# (str) Android NDK API to use. This is the minimum API your app will support
android.ndk_api = 21