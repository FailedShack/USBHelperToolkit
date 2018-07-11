from usbhelpertoolkit import getCdn, downloadAssets
from FunKiiU import process_title_id
import json

downloadUrl = getCdn("wiiu/download/{}")

with open('customs.json') as f:
    customs = json.load(f)
    print("Customs file loaded, {} entries found.".format(len(customs)))

i = 0
for entry in customs:
    name = customs[i]["Name"]
    id = customs[i]["ProductCode"]
    titleId = customs[i]["TitleId"]
    region = customs[i]["Region"]
    print("Now downloading: {} ({})".format(name, id))
    downloadAssets(titleId)
    process_title_id(titleId, None, name, region, "", 3, False, False, False, False, False, downloadUrl, True, True)
    i += 1