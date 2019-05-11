#!/usr/bin/python3

import matplotlib.pyplot as plt
import matplotlib
from matplotlib.lines import Line2D
import matplotlib.font_manager as font_manager
import json
from operator import itemgetter
from colors import colors
import os
import sys

owndir = os.path.dirname(os.path.realpath(__file__))
datadir = os.path.join(owndir, 'data')

try:
    with open(os.path.join(datadir, 'plotdata.json'), 'r') as fh:
        auctions = json.load(fh)

    with open(os.path.join(datadir, 'lastid'), 'r') as fh:
        lastid = int(fh.read().strip())
except:
    sys.exit(1)

maxprice = auctions[str(lastid-1)]
getmaxprice = itemgetter('price')
maxprice = list(map(getmaxprice, maxprice))

maxprice = max(maxprice) + 1e7

for bidRound in range(1, lastid):
    data = auctions[str(bidRound)]
    print('generating chart for round {}'.format(bidRound))
    plt.rcdefaults()
    fig, ax = plt.subplots()

    fig.set_size_inches(13, 7)

    getfreq = itemgetter('frequency')
    freq = list(map(getfreq, data))

    getprice = itemgetter('price')
    price = list(map(getprice, data))

    getcolor = itemgetter('color')
    color = list(map(getcolor, data))

    sums = {
        'Telekom': 0,
        'Vodafone': 0,
        'Telefónica': 0,
        '1 & 1': 0,
    }

    # calculate spendings
    for bid in data:
        if bid['winner'] == 'kein Gebot':
            continue
        sums[bid['winner']] += bid['price']

    ax.bar(freq, price, align='center', color=color)
    ax.set_xticks(freq)
    ax.set_xticklabels(freq, rotation='vertical')
    ax.set_xlabel('frequency')
    ax.set_ylabel('best offer')
    ax.set_title('Results of bidding round {0:03d}'.format(bidRound))
    ax.ticklabel_format(style='plain', axis='y')
    ax.yaxis.set_major_formatter(
        matplotlib.ticker.StrMethodFormatter('{x:,.0f} €'))

    # prepare data for legend
    for winningBid in sums:
        sums[winningBid] = sums[winningBid] / 1000000.
        sums[winningBid] = '{:10.2f} Mio €'.format(sums[winningBid])

    grandTotal = sum(price) / 1000000.
    grandTotal = '{:10.2f} Mio €'.format(grandTotal)

    # legend
    legend_elements = [
        Line2D([0], [0], color=colors['Vodafone'], lw=4,
               label='{}{}'.format('Vodafone'.ljust(11), sums['Vodafone'])),
        Line2D([0], [0], color=colors['Telekom'], lw=4,
               label='{}{}'.format('Telekom'.ljust(11), sums['Telekom'])),
        Line2D([0], [0], color=colors['Telefónica'], lw=4, label='{}{}'.format(
            'Telefónica'.ljust(11), sums['Telefónica'])),
        Line2D([0], [0], color=colors['1 & 1'], lw=4,
               label='{}{}'.format('1 & 1'.ljust(11), sums['1 & 1'])),
        Line2D([0], [0], color='w', lw=0, label='{}{}'.format(
            'TOTAL:'.ljust(11), grandTotal)),
    ]

    # legend font settings
    font = font_manager.FontProperties(family='DejaVu Sans Mono',
                                       weight='regular',
                                       style='normal',
                                       size=13,
                                       )
    ax.legend(handles=legend_elements, prop=font)
    ax.yaxis.set_units('€')
    plt.tight_layout()
    exportFileName = '{0:03d}.png'.format(bidRound)
    plt.savefig(os.path.join(owndir, 'export', exportFileName), dpi=160)
    plt.close()
