import config

from datetime import datetime
from urllib.parse import urlparse, parse_qs

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.headless = True
assert opts.headless  # Operating in headless mode
browser = Chrome(options=opts)
browser.get("https://www.smwcentral.net/?p=section&s=smwhacks")

romlist = []

print("Opening SMWC to check for new hacks...")
for row in browser.find_elements_by_css_selector("#list_content tr:not(:first-child)"):
	infolink = row.find_element_by_css_selector("td:first-child a").get_attribute('href')
	downloadlink = row.find_element_by_css_selector("td:last-child").find_element_by_tag_name('a').get_attribute('href')
	rom = {
		"id":parse_qs(urlparse(infolink).query).get('id')[0],
		"title": row.find_element_by_css_selector("td:first-child a").text,
		"added": datetime.strptime(row.find_element_by_css_selector("td:first-child span time").text,"%Y-%m-%d %I:%M:%S %p"),
		"download-link": downloadlink,
		"detail-link":infolink
	}
	romlist.append(rom)
print(romlist)
browser.close()
quit()
