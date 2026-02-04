[app]
title = Eco Tower Neo Seoul
package.name = ecotowerneoseoul
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 0.1
requirements = python3,kivy,pygame
orientation = portrait
fullscreen = 1
android.archs = arm64-v8a, armeabi-v7a
p4a.branch = master
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

[buildozer]
log_level = 2
warn_on_root = 1
