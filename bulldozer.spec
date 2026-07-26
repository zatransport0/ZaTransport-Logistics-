[app]

title = ZaTransport Logistics

package.name = zatransport

package.domain = com.zatransport

source.dir = .

source.include_exts = py,kv,png,jpg,xlsx,json

version = 0.1.0

requirements = python3,kivy,openpyxl,et_xmlfile

orientation = portrait

fullscreen = 0

icon.filename = %(source.dir)s/assets/icon.png

presplash.filename = %(source.dir)s/assets/presplash.png

android.archs = arm64-v8a

android.api = 35

android.minapi = 26

android.accept_sdk_license = True