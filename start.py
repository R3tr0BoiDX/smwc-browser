import config
from lib import SMWC

import json
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.headless = True
assert opts.headless
browser = Chrome(options=opts)

romlist = SMWC.get_hack_list(browser)
with open('cache/hacks.json', 'w') as fp:
    json.dump(romlist, fp)
##print(romlist)
browser.close()
quit()
