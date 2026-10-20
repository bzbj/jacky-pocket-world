<p align="right"><a href="README.zh_CN.md">简体中文</a> · <strong>English</strong></p>

# Jacky's Pocket World · Static Edition

A minimal, offline FoloToy AI Passport application for reuse as a pocket-card UI.
Target: ESP32-C3, 8 MB flash, no PSRAM, 240×320 display, ESP-IDF **5.5.3**.

[Live preview](https://bzbj.github.io/jacky-pocket-world/preview/) ·
[中文说明](README.zh_CN.md)

| Home | WeChat placeholder | Static settings |
| --- | --- | --- |
| <img src="preview/screens/home.png" width="160" alt="Home with three pixel characters"> | <img src="preview/screens/wechat.png" width="160" alt="Empty QR placeholder"> | <img src="preview/screens/settings.png" width="160" alt="Wi-Fi labels: home, phone, office"> |

Open [preview/index.html](preview/index.html) directly in a browser. It displays
the same three screen images used by the firmware and requires no server,
JavaScript, account or network connection.

## Included screens and controls

- **Home:** Jacky Lin, the reading penguin and three stationary characters.
- **WeChat:** an empty `YOUR QR HERE` placeholder; no encoded contact data.
- **Settings:** static menu artwork. Wi-Fi shows only `home / phone / office`.
  These are labels, not saved networks. No SSIDs, passwords or connection state
  are stored, read or written. Menu items do not launch hardware test functions.

UP/DOWN alternates between Home and WeChat. Hold OK on Home to open Settings.
Hold OK on either other page to return Home. A short OK leaves the screen as is.
The firmware reads actual battery percentage when available; no fake value is
shown. The characters are intentionally static in this edition.

## Build and check

Activate the official ESP-IDF 5.5.3 environment, then run:

```sh
idf.py --version
./tools/validate.sh
```

The Bash gate runs public-file checks, host tests, an isolated firmware build,
merged-image layout checks and matching debug archival. A host C compiler is
needed for tests. `--static` and `--firmware` run either stage separately.
Git Bash on Windows can invoke the same gate with native IDF tools; ordinary
Windows IDF terminals can also run `idf.py build` for an incremental build.

The checked complete image is `build/FoloToy-AI-Passport-full.bin`, for offset
`0x0`. Matching debug files are under `build/firmware/<sha256>/`.
For a blank device or an intentional full refresh, a merged image can replace
stored NVS data. For an existing compatible device where settings matter, use
segmented `idf.py flash` instead. Building never flashes a device.

## Customize and share

`main/navigation.c` defines navigation. `main/main.c` handles the display,
button queue and battery. `tools/build_assets.py` creates the three screen PNGs
and `assets/screens.c`. Generated images/arrays are included, so Pillow is only
required when changing artwork:

```sh
python -m pip install Pillow
python tools/build_assets.py
```

An optional `--font /path/to/font.ttf` uses a local font without bundling it.
Replace the public home name/artwork and QR placeholder to make your own card.
The static layout uses fixed robot positions and no animation tasks.

The source package intentionally excludes live Token statistics, Vibe Tree,
Codex connections, speech, cloud endpoints, device keys, Wi-Fi provisioning,
private QR images, logs, local configuration, build data and Git history.
The blue character is visual artwork only; its presence does not imply a
connection to Codex.

`public-files.json` is the explicit release allowlist. To package reviewed source:

```sh
python tools/package_source.py ../jacky-pocket-world-source.zip
```

The packager checks source and fails if the output exists. It never recursively
copies the working directory or packages firmware/NVS/debug artifacts.

## Attribution

BSP code and firmware verification tools are derived from
[FoloToy AI Passport](https://github.com/folotoy/ai-passport), under the retained
[MIT license](LICENSE). Code in this edition is distributed under that license.
Artwork has separate provenance; see [ASSET-NOTICES.md](ASSET-NOTICES.md).
The characters are original code-drawn substitutes in the original positions;
the desktop-app mascot atlas and third-party logo source images are excluded.

Validation of the source does not establish physical-button behavior, LCD
appearance, battery accuracy or hardware compatibility. Device acceptance is
separate from compilation.
