# SMW Central Browser

<div style="text-align:center">

  ![SMW Central Browser Logo](media/images/logo.png)
</div>

- [SMW Central Browser](#smw-central-browser)
  - [What is this?](#what-is-this)
  - [Screenshots](#screenshots)
  - [Install](#install)
    - [Precompiled binaries](#precompiled-binaries)
    - [Run from source](#run-from-source)
    - [Build from source](#build-from-source)
  - [Setup the `config.json`](#setup-the-configjson)
  - [Command line arguments](#command-line-arguments)
  - [Steam Grid images](#steam-grid-images)
  - [Future ideas](#future-ideas)
  - [Urgent TODOs](#urgent-todos)
  - [Wanna help?](#wanna-help)
  - [Credits](#credits)
  - [Other SMW (US) checksums](#other-smw-us-checksums)
  - [FAQ](#faq)

## What is this?

Depending on your perspective, this can be several. Mostly, its a handy tool to browser and search for [SMW hacks](https://www.smwcentral.net/?p=section&s=smwhacks) on [SMW Central](https://www.smwcentral.net/). This tool allows you to browse through all SMW hacks submissions, search with specific filters, lets you download and patch your SMW SFC file and launches the patched ROM with your favorite emulator!

From another perspective, a part of this project is a crawler (for the submession table-like pages as of right now), which allows you to interact with the submessions on a more developer friendly way. Maybe you want to build your own browser, then you might want to check out [this subfolder](source/smwc)!

This project was mainly created with the Steam Deck in mind, but should work on any platform, that supports Python!

## Screenshots

<div style="text-align:center">

  **SMW Central Browser main screen**
  ![SMW Central Browser main screen](.github/user/screen_main.png)

  **SMW Central Browser filter screen**
  ![SMW Central Browser filter screen](.github/user/screen_filter.png)
</div>

## Install

There are two way for you to install this. You can download precompiled binaries or clone this repo and run it from the source code!

### Precompiled binaries

You can get the [latest precompiled binaries](https://github.com/R3tr0BoiDX/smwc-browser/releases/latest) from the releases section. Just download them and execute them! It's nearly that easy!

<div style="text-align:center">

  [![Download](.github/user/download_button.png)]([URL_TO_LINK](https://github.com/R3tr0BoiDX/smwc-browser/releases/latest))
</div>

### Run from source

If you prefer to run the program from the source, the run the following commands:

```bash
# Install python3 and python3-venv
apt install python3 python3-venv

# Clone repository
git pull https://github.com/R3tr0BoiDX/smwc-browser.git

# Change into folder with source
cd smwc-browser

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt -r requirements-dev.txt

# Run the browser
python3 -m source.main
```

> :warning: These instructions are intended for Linux-based systems. If you're using Windows, you can achieve similar results with PowerShell. You cannot use the `apt` command, so you'll need to manually [install Python](https://www.python.org/downloads/windows/) and change the `source.venv/bin/activate` command with `.\.venv\Scripts\Activate.ps1`.

### Build from source

If you want to take this even further and compile your own executable, you can either run the appropriate build script ([`build.linux.sh`](build.linux.sh) or [`build.windows.ps1`](build.windows.ps1)) or you follow their instructions on your own.

## Setup the `config.json`

No matter if you run from source or you prefer the precompiled binaries, both come with the [`config.example.json`](https://github.com/R3tr0BoiDX/smwc-browser/blob/master/config.example.json). You will need to **rename** this to `config.json` and fill out all the entries. It will look something like this:

```json
{
 "sfc_path": "home/user/Games/baserom.us.sfc",
 "library_path": "/home/user/Games/",
 "launch_program": "emulatorGX"
}
```

Let's take a look at all the entries:

- **`sfc_path`**: This is the path to find your SMW (US) SFC file. It **must** have a CRC32 code of `B19ED489`, or else you have the incorrect ROM and the SMW Central Browser won't launch. A built-in checksum test verifies if you have the right ROM. Different checksums are listed [below](#other-smw-us-checksums).
- **`library_path`**: This is where the patched ROMs files will be saved. If you use RetroArch or a similar program and want the patched games to show up in your collection, this is for you!
- **`launch_program`**, optional: After the ROMs have been patched, you can open them automatically with a program of your choice, allowing you to play right away! If you remove this key from the config file, no program will launch after patching.

> :warning: Windows handles its paths differently than Linux, and you will need to escape your paths! They will look something like this: `"sfc_path": "C:\\Users\\User\\Games\\baserom.us.sfc`

## Command line arguments

There aren't many command line arguments, but there a some. Right now there are:

- **`-l`, `--no-launch`**: Don't launch the patched file using the program defined in the configuration file once patching is complete. If no program is defined, no program will be launched anyway.
- **`-f`, `--no-fullscreen`**: Don't start the browser in fullscreen mode.
- **`-h`**: Displays a help screen

## Steam Grid images

There are all the [image resources](resources/steam-grid) you need if you want to add the SMW Central Browser to your Steam library. You can [download those as ZIP file here.](https://download-directory.github.io/?url=https%3A%2F%2Fgithub.com%2FR3tr0BoiDX%2Fsmwc-browser%2Ftree%2Fmaster%2Fresources%2Fsteam-grid)

## Future ideas

*In order of significance:*

- Wrapper and screen for hack entry site
- Wrapper for hack screenshots and display in browser
- Save filter parameter
- File browser for unzipped hack, if there are multiple patch files
  - Should include an option to show all files and apply them as patches if the user wishes so
- Maybe a way to delete downloaded hacks from library?
- Support for SMW2:YI and SM64
- Settings screen
- Argument to disable checksum check
- Language support

**Constructive criticism and ideas for improvements are also always welcome!**

## Urgent TODOs

- Linting (and a lil bit refactoring)
- Better gamepad support and scrolling

## Wanna help?

This project is entirely done in my free time next to my full time job. Soon, I'll write my bachelor thesis and will have much less time for this project. So, if you wanna contribute and help with any feature, you're welcome! We need tests, bug fixes and new features would be nice as well. I much appreciate your consideration! :slightly_smiling_face:

## Credits

This project was based on [adamzwakk's](https://github.com/adamzwakk) alias [Adam Zwakenberg's](https://www.adamzwakk.com/) [smwc-interface](https://github.com/adamzwakk/smwc-interface), but very fast it divergent heavily from his source code. By now, none of it is left, yet, it's what started this.

## Other SMW (US) checksums

If you would rather compare your SFC with a different checksum, below are alternative SMW (US) checksums. If your ROM matches these, it should also pass the CRC32 check.

- **SHA-1**: `6B47BB75D16514B6A476AA0C73A683A2A4C18765`
- **SHA256**: `0838E531FE22C077528FEBE14CB3FF7C492F1F5FA8DE354192BDFF7137C27F5B`
- **MD5**: `CDD3C8C37322978CA8669B34BC89C804`
- **CRC32**: `B19ED489`

## FAQ

**I found a bug! Where can I report it?**

Please [open a new issue](https://github.com/R3tr0BoiDX/smwc-browser/issues/new) and provide as much information about the issue as you can. Preferable the stack trace when Python crashed.

**Will there be support for SMW2:YI and SM64?**

Maybe one day! It's certainly a nice idea and in theory not to hard to implement.

**Why CRC32?**

Because it's fast.

**Will this break when they change SMW Central?**

Depends, but very likely. If they just change the style, there should be no issue, and while its a little bit adaptive, the margin for error if they should change the HTML structure is very small. But it hasn't really changed in a looong while, so fingers crossed!

**I can't find my question!**

Feel free to open a new issue, just please add the *question* label to it :slightly_smiling_face:
