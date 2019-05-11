#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import sys
import os


baseUrl = 'https://www.bundesnetzagentur.de/_tools/FrequenzXml/Auktion2019_XML/{0:03d}.html'

headers = {'User-Agent': 'Fnord'}

owndir = os.path.dirname(os.path.realpath(__file__))
datadir = os.path.join(owndir, 'data')

try:
    with open(os.path.join(datadir, 'lastid'), 'r') as fh:
        start = int(fh.read().strip())
except:
    start = 1

for biddingRound in range(start, 999):
    response = requests.get(baseUrl.format(biddingRound), headers=headers)
    if response.status_code != 200:
        with open(os.path.join(datadir, 'lastid'), 'w') as fh:
            fh.write(str(biddingRound))
        break
    soup = BeautifulSoup(response.text, 'html.parser')
    meta = soup.findAll('meta', attrs={'name': 'description'})
    xml = meta[0]['content']

    try:
        xmlFileName = '{0:03d}.xml'.format(biddingRound)
        dataXmlFile = os.path.join(datadir, xmlFileName)
        with open(dataXmlFile, 'w') as fh:
            fh.write(xml)
        print('Saved auction {} to file.'.format(biddingRound))
    except BaseException as e:
        print('Unable to write xml to file')
        print(e)
        sys.exit(1)
