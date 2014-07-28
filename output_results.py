#!/bin/python
import os
import re
from bs4 import BeautifulSoup

# Get the run directory (set by calling script)
rundir = os.environ.get('SIG_RUN_DIR')
if rundir is None:
    print 'SIG_RUN_DIR not set. Aborting'
    exit()

report = os.path.join(rundir, 'report.html')
if not os.path.isfile(report):
    print 'report.html not found. Aborting'
    exit()

file = open(report, 'r')
html = file.read()
file.close()

soup = BeautifulSoup(html)

# The last table is our signal vs background computations
table = soup.find_all('table')[-1]
# The last row
tr = table.find_all('tr')[-1]
# The last column
td = tr.find_all('td')[-1]

# Get the number for signal vs background
sb = td.get_text().strip()

# Grab the parameters from param_card.dat
param_card = os.path.join(rundir, 'param_card.dat')
if not os.path.isfile(param_card):
    print 'param_card.dat not found. Aborting'
    exit()

file = open(param_card, 'r')
param_card = file.read()
file.close()

regex = re.compile('1\s+(.*)\s+\#\s+gsm')
gsm = regex.search(param_card).group(1)
regex = re.compile('2\s+(.*)\s+\#\s+gse')
gse = regex.search(param_card).group(1)
regex = re.compile('9000005\s+(.*)\s+\#\s+Mphi')
mphi = regex.search(param_card).group(1)
regex = re.compile('DECAY\s+9000005\s+(.*)')
wphi = regex.search(param_card).group(1)

# Write the output
output = os.path.join(rundir, 'results.dat')
file = open(output, 'w')

file.write("Mphi: %s\n" % mphi)
file.write("gse: %s\n" % gse)
file.write("gsm: %s\n" % gsm)
file.write("Wphi: %s\n" % wphi)
file.write("SvsB: %s\n" % sb)

file.close()
