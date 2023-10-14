# SMW Central Browser

![SMW Central Browser Logo](media/images/logo.png)

- [SMW Central Browser](#smw-central-browser)
  - [What is this?](#what-is-this)
  - [Install](#install)
    - [Precompiled binaries](#precompiled-binaries)
  - [Example 'config.json'](#example-configjson)
  - [Future ideas](#future-ideas)
  - [Wanna help?](#wanna-help)
  - [Urgent TODOs](#urgent-todos)
  - [FAQ](#faq)

## What is this?

Depending on your perspective, this can be several. Mostly, its a handy tool to browser and search for [SMW hacks](https://www.smwcentral.net/?p=section&s=smwhacks) on [SMW Central](https://www.smwcentral.net/). This tool allows you to browse through all SMW hacks submissions, search with specific filters, lets you download and patch your SMW SFC file and launches the patched ROM with your favorite emulator!

From another perspective, a part of this project is a crawler (for the submession table-like pages as of right now), which allows you to interact with the submessions on a more developer friendly way. Maybe you want to build your own browser, then you might want to check out [this subfolder](source/smwc)!

## Install

There are two way for you to install this. You can download precompiled binaries or clone this repo and run it from the source code!

### Precompiled binaries

## Example 'config.json'

```json
{
 "library_path": "/path/to/your/location/where/to/save/patched/file/",
 "launch_program": "/path/to/application/to/launch/patched/file/with"
}
```

## Future ideas

*In order of importance:*

- File browser for unzipped hack, if there are multiple patch files
  - Should include an option to show all files and apply them as patches if the user wishes so
- Wrapper and screen for hack entry site
- Wrapper for hack screenshots and display in browser
- Save filter parameter
- Maybe a way to delete downloaded hacks from library?
- Support for SMW2:YI and SM64
- Language support

## Wanna help?

This project entirely in my free time next to my full time job. Soon, ill write my bachelor thesis and will have much less time for this project. So, if you wanna contribute and help with any feature, you're welcome! We need tests, bug fixes and new features would be nice as well. I much appreciate your consideration! :slightly_smiling_face:

Constructive criticism and ideas for improvements are also always welcome!

## Urgent TODOs

- linting (and a lil bit refactoring)
- better gamepad support and scrolling

## FAQ

> Will there be support for SMW2:YI and SM64?
Maybe one day! Its certainly a nice idea and in theory not to hard to implement