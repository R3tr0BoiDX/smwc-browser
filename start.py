#My Stuff
from lib import ips
from lib import SMWC

#Deps
import json
import tempfile
import shutil
from pathlib import Path
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.headless = True
assert opts.headless

hack_path = "./cache/hacks.json"
source_path = "./source/Super Mario World (USA).sfc"
temp_path = tempfile.mkdtemp();
output_path = "./output/"

hacklist = Path(hack_path)
if not hacklist.is_file():
	browser = Chrome(options=opts)
	hacklist = SMWC.get_hack_list(browser)
	with open('cache/hacks.json', 'w') as fp:
	    json.dump(hacklist, fp)
	browser.close()
	print('Got the list! Run again to choose')
	quit()
else:
	with open(hack_path) as f:
	    hacklist = json.load(f)

SMWC.set_hack_list(hacklist['hack_list'])
hack = SMWC.draw_table()
download = SMWC.download_hack(hack,temp_path)
unzip = SMWC.unzip_hack(download,temp_path)
output_file = output_path+hack.get('title')+'.sfc'
for f in unzip:
	if f.endswith('.bps'):
		print('Patching '+hack.get('title')+' on to '+source_path)
		SMWC.apply_bps(f,source_path,output_file)
		print('Outputted file to: ' + output_file)
	elif f.endswith('.ips'):
		SMWC.apply_ips(f,source_path,output_file)
		print('Outputted file to: ' + output_file)
quit()