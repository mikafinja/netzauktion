#!/usr/bin/env python3

import xmltodict
from operator import itemgetter
import json
import sys
import os
from colors import colors

auctions = {}
rawAuctions = {}

owndir = os.path.dirname(os.path.realpath(__file__))

companies = {
    'Telekom': 'Telekom',
    'Vodafone': 'Vodafone',
    'TEF DE': 'Telefónica',
    '1und1 DRI': '1 & 1',
}

lastidFile = os.path.join(owndir, 'data', 'lastid')
datadir = os.path.join(owndir, 'data')
try:
    with open(lastidFile, 'r') as fh:
        maxbid = int(fh.read().strip())
except IOError:
    sys.exit(1)

for x in range(1, maxbid):
    print(f'processing bid {x}')
    xmlFileName = '{0:03d}.xml'.format(x)
    dataXmlFile = os.path.join(datadir, xmlFileName)
    try:
        with open(dataXmlFile, 'r') as fh:
            auktion = xmltodict.parse(fh.read())
    except IOError:
        sys.exit(1)

    auction = []
    rawAuction = []
    for group in range(0, 3):
        for bid in auktion['BNetzAMonitor7']['gebotsobjekte']['produktgruppe'][group]['gebotsobjekt']:
            if bid['spalte'][4]['@wert']:
                price = int(bid['spalte'][4]['@wert'].replace('.', '')) * 1000
            else:
                price = 0
            if bid['spalte'][3]['@wert']:
                rawWinner = bid['spalte'][3]['@wert'].strip()
                winner = companies[rawWinner]
            else:
                rawWinner = 'kein Gebot'
                winner = rawWinner
            color = colors[winner]
            details = bid['spalte'][2]['@wert'].strip()
            frequency = bid['spalte'][1]['@wert'].strip()
            band = bid['spalte'][0]['@wert'].strip()
            rawAuction.append({'band': band, 'frequency': frequency,
                               'details': details, 'winner': rawWinner, 'price': price})
            auction.append({'band': band, 'frequency': frequency, 'details': details,
                            'winner': winner, 'price': price, 'color': color})
    auction = sorted(auction, key=itemgetter('price'), reverse=True)
    rawAuction = sorted(rawAuction, key=itemgetter('price'), reverse=True)
    auctions[x] = auction
    rawAuctions[x] = rawAuction

try:
    with open(os.path.join(datadir, 'plotdata.json'), 'w') as fh:
        json.dump(auctions, fh, indent=2, sort_keys=True)

    with open(os.path.join(datadir, '5gAuktion.json'), 'w') as fh:
        json.dump(rawAuctions, fh, sort_keys=True)
except:
    sys.exit(1)
