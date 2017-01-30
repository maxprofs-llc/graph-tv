from bs4 import BeautifulSoup
import codecs
import html
import os
import re
from collections import defaultdict
import json

sharedScenes = defaultdict(lambda : defaultdict(int))
characters = defaultdict(int)

f = codecs.open('/Users/ompatel/Dropbox/seinfeld/data/interim/scene_characters.tsv', 'r', encoding='utf-8')
episode = None
scene = None
characterBuffer = []
f.readline()
for line in f:
    [thisEpisode, thisScene, character, noLines] = line.split('\t')
    if (episode is None and scene is None):
        episode = thisEpisode
        scene = thisScene
        characterBuffer = [character]
    elif (thisEpisode != episode) or (thisScene != scene):
        characterBuffer.sort()
        for i in range(0, len(characterBuffer)):
            characters[characterBuffer[i]] += 1
            for j in range(i+1, len(characterBuffer)):
                if characterBuffer[i] != characterBuffer[j]:
                    sharedScenes[characterBuffer[i]][characterBuffer[j]] += 1
        episode = thisEpisode
        scene = thisScene
        characterBuffer = [character]
    else:
        characterBuffer.append(character)
# print(characters)
# print(sharedScenes)

outJSON = {"nodes": [], "links": []}

for key, value in characters.items():
    outJSON["nodes"].append({"id": key, "group": value})

links = []
for key, value in sharedScenes.items():
    for linkKey, linkValue in value.items():
        outJSON["links"].append({"source": key, "target": linkKey, "value": linkValue})

with codecs.open('/Users/ompatel/Dropbox/seinfeld/src/seinfeld_data.json', 'w', encoding='utf-8') as o:
    json.dump(outJSON, o)
