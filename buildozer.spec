[app]
title = TeaCash
package.name = teacash
package.domain = org.teacash
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

requirements = python3,kivy==2.3.0,plyer
android.api = 33
android.ndk = 25b
android.sdk = 24
android.accept_sdk_license = True
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.skip_update = True

[buildozer]
log_level = 2
warn_on_root = 1
