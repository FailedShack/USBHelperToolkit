from usbhelpertoolkit import getCdn, downloadFile, downloadAssets
import requests
import json
import os
import re

templateUrl = getCdn("res/{}/template/{}/{}")
platformUrl = { 655: "nintendont", 656: "Wii", 657: "SNES", 658: "N64" }
platforms = { 655: "GameCube", 656: "Wii", 657: "SNES", 658: "N64" }
files = { "bootDrcTex.tga", "bootTvTex.tga", "iconTex.tga", "bootSound.btsnd" }

def tryGetTemplateValue(platformId, id, key):
    r = getTemplateResource(platformId, id, key)
    val = None
    if r.status_code == 200:
        val = r.text
    return val

def getTemplateBoolean(platformId, id, key, default):
    r = getTemplateResource(platformId, id, key)
    val = default
    if r.status_code == 200:
        val = not val
    return val

def downloadTemplateResource(platformId, id, fileName):
    r = getTemplateResource(platformId, id, fileName)
    path = getLocalTemplatePath(platformId, id, fileName)
    if r.status_code == 200:
        with open(path, "wb") as f:
            f.write(r.content)
        return True
    return False

def getTemplateResource(platformId, id, fileName):
    r = requests.get(templateUrl.format(platformUrl[platformId], id, fileName))
    return r

def getLocalTemplatePath(platformId, id, fileName):
    folder = os.path.join("res", platformUrl[platformId], "template", id)
    if not os.path.exists(folder):
        os.makedirs(folder)
    return os.path.join(folder, fileName)

with open('injections.json') as f:
    injections = json.load(f)
    print("Injections file loaded, {} entries found.".format(len(injections)))

i = 0
for entry in injections:
    id = injections[i]["ProductCode"]
    platform = injections[i]["Platform"]
    if platform not in platforms:
        print("Skipped title {} for platform {}.".format(id, platform))
        i += 1
        continue
    
    print("Fetching data for {} title {} ({})...".format(platforms[platform], injections[i]["Name"], id))
    data = {}
    data["name"] = tryGetTemplateValue(platform, id, "name")
    data["config"] = tryGetTemplateValue(platform, id, "config")
    data["music"] = tryGetTemplateValue(platform, id, "music")
    data["product_codes"] = tryGetTemplateValue(platform, id, "product_codes")
    data["template"] = tryGetTemplateValue(platform, id, "template")
    data["hash"] = tryGetTemplateValue(platform, id, "hash")
    data["twodiscs"] = getTemplateBoolean(platform, id, "twodiscs", False)
    data["notcompress"] = getTemplateBoolean(platform, id, "notcompress", True)
    if platform == 656:
        data["gamepad"] = getTemplateBoolean(platform, id, "gamepad", False)
        data["vertical"] = getTemplateBoolean(platform, id, "vertical", False)
        data["horizontal"] = getTemplateBoolean(platform, id, "horizontal", False)
        data["online"] = getTemplateBoolean(platform, id, "online", False)
        data["patch"] = tryGetTemplateValue(platform, id, "patch")
    
    if data["config"] is not None:
        for line in data["config"].split("\r\n"):
            m = re.search("PDFURL = \"(.*)\"", line)
            if m is not None:
                if downloadFile(m.group(1), os.path.join("wiiu", "info", "manuals", "{}.pdf".format(id))):
                    print("Downloaded manual.")
                else:
                    print("Could not download manual.")
    
    titleId = injections[i]["TitleId"];
    downloadAssets(titleId)
    with open(getLocalTemplatePath(platform, id, "data.json"), "w") as f:
        json.dump(data, f)
    for file in files:
        if not downloadTemplateResource(platform, id, file):
            print("Could not download file: {}".format(file))
    i += 1