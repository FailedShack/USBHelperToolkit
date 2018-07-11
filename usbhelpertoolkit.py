import requests
import json
import os

cdnUrl = "https://cdn.wiiuusbhelper.com/{}"
infoUrl = cdnUrl.format("wiiu/info/US/{}")

def getCdn(path):
	return cdnUrl.format(path)

def downloadFile(url, dest):
	folder = os.path.dirname(dest)
	if not os.path.exists(folder):
		os.makedirs(folder)
	r = requests.get(url)
	if r.status_code == 200:
		with open(dest, "wb") as f:
			f.write(r.content)
		return True
	return False

def downloadAssets(titleId):
	infoPath = os.path.join("wiiu", "info", "US", titleId)
	if downloadFile(infoUrl.format(titleId), infoPath):
		print("Downloaded info.")
	else:
		print("Could not download info, assets will not be downloaded :(")
		return
	
	with open(infoPath) as f:
		info = json.load(f)["title"]
	
	if "custom_cover_url" in info:
		if downloadFile(info["custom_cover_url"], os.path.join("wiiu", "info", "covers", "{}.png".format(titleId))):
			print("Downloaded custom cover.")
		else:
			print("Could not download custom cover.")
	if "banner_url" in info:
		if downloadFile(info["banner_url"], os.path.join("wiiu", "info", "banners", "{}.png".format(titleId))):
			print("Downloaded banner.")
		else:
			print("Could not download banner.")