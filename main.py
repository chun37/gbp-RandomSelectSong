# -*- coding: utf-8 -*-
import requests as req
from bs4 import BeautifulSoup as bs
import os
import json
import random

currentDir = os.path.dirname(os.path.abspath(__file__))


class RandomSelect:
    def __init__(self):
        self.url = "http://chun37.hatenablog.com/entry/2018/01/01/071811"

    def getUpdatedTime(self):
        r = req.get(self.url)
        self.scrapingData = r.content
        soup = bs(r.content, "lxml")
        dates = soup.find("div", class_="section").find("p").text.split("\n")
        lastUpdate = [i for i in dates if "[" in i][-1][1:-1]
        self.lastUpdate = lastUpdate
        return lastUpdate

    def getSongData(self):
        soup = bs(self.scrapingData, "lxml")
        tabledata = [list(map(lambda x: x.text, i.find_all("td")))
                     for i in soup.find_all("tr")[1:]]
        return tabledata

    def saveJson(self, jsonPath):
        songData = self.getSongData()
        with open(jsonPath, "w") as f:
            json.dump(
                {"LastUpdateDate": self.lastUpdate, "SongData": songData},
                f,
                indent=4
            )
        return songData

    def selectSong(self, songData):
        songData = [i for i in songData if ("NO DATA" or "NO_DATA") not in i]
        return random.choice(songData)


def main():
    m = RandomSelect()
    jsonPath = os.path.join(currentDir, 'data.json')
    lastUpdate = m.getUpdatedTime()
    if os.path.exists(jsonPath):
        with open(jsonPath) as f:
            jsonData = json.loads(f.read())
        if jsonData["LastUpdateDate"] == lastUpdate:
            songData = jsonData["SongData"]
        else:
            print(f'Update: {jsonData["LastUpdateDate"]} -> {lastUpdate}')
            songData = m.saveJson(jsonPath)
    else:
        print(f"Download: {lastUpdate}")
        songData = m.saveJson(jsonPath)
    selectedSong = m.selectSong(songData)
    print(selectedSong[0], selectedSong[2])

if __name__ == '__main__':
    main()
