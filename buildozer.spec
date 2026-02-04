buildozer_spec = """
[app]
# (str) Titel deiner App
title = Eco Tower Neo Seoul

# (str) Paket-Name (WICHTIG: Keine Leerzeichen!)
package.name = ecotowerneoseoul

# (str) Dein Domain-Name (umgekehrt)
package.domain = org.deinname

# (str) Wo liegt die main.py? (. bedeutet aktueller Ordner)
source.dir = .

# (list) Welche Dateien sollen mit?
source.include_exts = py,png,jpg,kv,atlas

# (str) App-Version
version = 0.1

# (list) Abhängigkeiten (Kivy ist hier Pflicht!)
requirements = python3,kivy==2.2.1

# (str) Orientierung (portrait, landscape oder all)
orientation = portrait

# (bool) Fullscreen ja/nein
fullscreen = 1

# --- Android spezifisch ---

# (int) API Level (33 ist aktuell Pflicht für den Play Store)
android.api = 33

# (int) Minimum API (21 läuft auf fast allen Handys)
android.minapi = 21

# (str) NDK-Version (25b ist sehr stabil)
android.ndk = 25b

# (list) Architekturen (arm64-v8a ist der Standard für moderne Handys)
android.archs = arm64-v8a

# (bool) Akzeptiere Lizenzen automatisch
android.accept_sdk_license = True

# (str) Format für den Play Store (aab) oder zum Testen (apk)
# Für den Play Store später auf aab ändern!
android.release_artifact = apk

[buildozer]
# (int) Log-Level (2 zeigt alle Fehler an)
log_level = 2
warn_on_root = 0
"""

with open("buildozer.spec", "w") as f:
    f.write(buildozer_spec)

print("✅ buildozer.spec wurde erfolgreich im Ordner erstellt!")