[app]
title = TeaCash
package.name = teacash
package.domain = org.teacash
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

requirements = python3,kivy,plyer

android.api = 33
android.ndk = 25b
android.sdk = 24
android.accept_sdk_license = True
android.permissions = INTERNET,ACCESS_NETWORK_STATE,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

[buildozer]
log_level = 2
warn_on_root = 1
