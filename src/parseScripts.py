from bs4 import BeautifulSoup
import codecs
import html
import os
import re
from collections import defaultdict
import json


def getTextFromHTML(infile, outfile):
    scriptHTML = ''

    with codecs.open(infile, 'r') as f:
        tableStart = False
        tableEnd = False
        for line in f:
            tableStart = True if 'td class="spacer2"' in line else tableStart
            tableEnd = True if tableStart and ('</td>' in line) else tableEnd
            if tableStart and not tableEnd:
                scriptHTML += html.unescape(line)
            else:
                continue
        scriptHTML += '</td>'

    soup = BeautifulSoup(scriptHTML, 'html.parser')

    scriptText = soup.text
    scriptLines = scriptText.split("\n")
    outfile = codecs.open(outfile, 'w', encoding="utf-8")
    for line in scriptLines:
        outfile.write(line.strip())
        outfile.write('\n')


def parseWikiEpisodeData(infile, outfile):
    f = codecs.open(infile, 'r', encoding="utf-8")
    soup = BeautifulSoup(f, 'html.parser')
    outfile = codecs.open(outfile, 'w', encoding="utf-8")

    episodeTables = soup.find_all('table', class_='wikiepisodetable')
    for table in episodeTables:
        for row in table.find_all('tr'):
            rowData = []
            for element in row.find_all(['th', 'td']):
                rowData.append(' '.join(html.unescape(element.text).split()))
            outfile.write('|'.join(rowData)+'\n')


def parseScript(episode, outfile):
    f = codecs.open(episode, 'r', encoding="utf-8")
    outfile = codecs.open(outfile, 'a', encoding="utf-8")
    scriptDivide = '='*66
    scriptStarted = False
    sceneSetting = ''
    p = re.compile('([A-Z]+):\s([\w\W]+)')
    overallNo = episode[31:-4]
    for line in f:
        # skip blank
        line = line.strip()
        if line:
            if scriptDivide in line:
                scriptStarted = True
                continue
            # scene starts with INT.
            if scriptStarted and line[:4] == 'INT.':
                sceneSetting = line[5:]
                continue
            if scriptStarted and line[0] == '[' and line[-1] == ']':
                sceneSetting = line[1:-1]
                continue
            # actions are in ()
            if scriptStarted and line[0] == '(' and line[-1] == ')':
                outfile.write('|'.join([overallNo, sceneSetting, 'action', line[1:-1]])+'\n')
                continue
            # spoken lines start with character name in all CAPS:
            # finding actions within script lines:
            #   p = re.compile('(\([\w\W]+?\))'
            #   re.findall(p,line)
            m = p.match(line)
            if scriptStarted and m is not None:
                outfile.write('|'.join([overallNo, sceneSetting, m.groups()[0], m.groups()[1]])+'\n')
                continue
        else:
            continue


def dataToJSON():
    sharedScenes = defaultdict(lambda: defaultdict(int))
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


# for file in os.listdir('../data/raw/'):
    # getTextFromHTML('../data/raw/'+file, '../data/interim/'+file[:-5]+'txt')

for file in os.listdir('../data/interim/scripts/'):
    parseScript('../data/interim/scripts/'+file, '../data/processed/script_lines.txt')

# parseScript('../data/interim/script-01.txt')
# parseWikiEpisodeData('../data/raw/List of Seinfeld episodes - Wikipedia.html', '../data/interim/EpisodeMetadata.txt')
