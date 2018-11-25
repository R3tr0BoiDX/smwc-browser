from datetime import datetime
import time
from urllib.parse import urlparse, parse_qs

hacklist = []

def set_hack_list(hl):
	global hacklist
	hacklist = hl

def get_hack_list(browser,first = True,url = "https://www.smwcentral.net/?p=section&s=smwhacks"):
	global hacklist
	if first:
		hacklist = []
		print("Opening SMWC to check for new hacks...")

	browser.get(url)
	print("Trying "+url)
	hackrows = browser.find_elements_by_xpath("//div[@id='list_content']//table//tr[position()>1]")

	for row in hackrows:
		firsttd = row.find_element_by_xpath(".//td[1]")
		infolink = firsttd.find_element_by_xpath(".//a").get_attribute('href')
		downloadlink = row.find_element_by_xpath(".//td[last()]//a").get_attribute('href')
		title = firsttd.find_element_by_xpath(".//a").text
		hack = {
			"id":parse_qs(urlparse(infolink).query).get('id')[0],
			"title": title,
			"added": datetime.strptime(firsttd.find_element_by_xpath(".//span//time").text,"%Y-%m-%d %I:%M:%S %p").strftime('%s'),
			"download-link": downloadlink,
			"detail-link":infolink
		}
		print("Found "+title)
		hacklist.append(hack)

	nextpage = browser.find_element_by_xpath("//td[@id='menu2']//td[1]//a[last()]")
	try:
		imgtest = nextpage.find_element_by_xpath('.//img')
		nextpage = nextpage.get_attribute('href')
		print('Found another page, trying page '+parse_qs(urlparse(nextpage).query).get('n')[0])
		return get_hack_list(browser,False,nextpage)
	except Exception as e:
		print("")

	return {"updated":time.time(), "hack_list": hacklist}

def get_titles_from_json():
	global hacklist
	titles = []
	for h in hacklist:
		titles.append(h['title'])
	return titles

def get_entry_from_title(title):
	global hacklist
	for h in hacklist:
		if h['title'] == title:
			return h