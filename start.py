#My Stuff
from lib import SMWC
hack_path = "./cache/hacks.json"

#Deps
import json
from pathlib import Path
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from pick import pick

opts = Options()
opts.headless = True
assert opts.headless

hacklist = Path(hack_path)
if not hacklist.is_file():
	browser = Chrome(options=opts)
	hacklist = SMWC.get_hack_list(browser)
	with open('cache/hacks.json', 'w') as fp:
	    json.dump(hacklist, fp)
	browser.close()
else:
	with open(hack_path) as f:
	    hacklist = json.load(f)

SMWC.set_hack_list(hacklist['hack_list'])
title, index = pick(SMWC.get_titles_from_json(),"Please select a Hack:")
info = SMWC.get_entry_from_title(title)
print(info)
quit()