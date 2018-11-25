import config

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
opts = Options()
opts.headless = True
assert opts.headless  # Operating in headless mode
browser = Chrome(options=opts)
browser.get("https://www.smwcentral.net/?p=section&s=smwhacks")
print("Opening SMWC to check for new hacks...")
browser.close()
quit()
