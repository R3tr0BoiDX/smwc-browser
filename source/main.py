import json
import tempfile
import time
from pathlib import Path

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

from source import smwc

opts = Options()
opts.headless = True
assert opts.headless

source_path = "./source/Super Mario World (USA).sfc"
temp_path = tempfile.mkdtemp()
output_path = "./output/"
hacklist = Path(hack_path)

if not hacklist.is_file():
    browser = Chrome(options=opts)
    hacklist = smwc.get_hack_list(browser)
    with open("cache/hacks.json", "w") as fp:
        json.dump(hacklist, fp)
    browser.close()
    print("Got the list! Run again to choose")
    quit()
else:
    with open(hack_path) as f:
        hacklist = json.load(f)

smwc.set_hack_list(hacklist["hack_list"])
hack = smwc.draw_table()
download = smwc.download_hack(hack, temp_path)
unzip = smwc.unzip_hack(download, temp_path)
for f in unzip:
    output_file = (
        output_path + hack.get("title") + " (" + str(int(time.time())) + ").sfc"
    )
    if f.endswith(".bps"):
        print("Patching " + hack.get("title") + " on to " + source_path)
        smwc.apply_bps(f, source_path, output_file)
        print("Outputted file to: " + output_file)
    elif f.endswith(".ips"):
        smwc.apply_ips(f, source_path, output_file)
        print("Outputted file to: " + output_file)
