#!/bin/python
################################################################################
#
# Nick Lange
# July 29, 2014
#
# Update our model parameters
#
################################################################################

import numpy as np
import os
import re

mphi = 16.0e-03 # Mass of scalar (GeV)
gsm  = 1.00e-05 # Muon coupling
gse  = 1.01e-06 # Electrong coupling

print 'Setting model parameters'

# Get the model directory (set by calling script)
modeldir = os.environ.get('MODEL_DIR')
if modeldir is None:
    print 'MODEL_DIR not set. Aborting'
    exit()

# Get the model parameters file
model = os.path.join(modeldir, 'muon-scalar.fr')
modelTemplate = os.path.join(modeldir, 'muon-scalar.fr.template')
if not os.path.isfile(modelTemplate):
    print 'muon-scalar.fr.template not found. Aborting'
    exit()

# Set our output format
np.set_printoptions(formatter={'float': lambda x: format(x, '6.3E')})
# Replace '1.5e-03' -> '1.5*^-03' for the Mathematica notation in FeynRules
mphi = re.sub('e', '*^', repr(mphi))
gsm = re.sub('e', '*^', repr(gsm))
gse = re.sub('e', '*^', repr(gse))

# Read in the model template and replace the parameters
with open(modelTemplate, "r") as f:
    lines = f.read()
    altered_lines = re.sub('MPHI_REPLACE', mphi, lines)
    altered_lines = re.sub('GSM_REPLACE', gsm, altered_lines)
    altered_lines = re.sub('GSE_REPLACE', gse, altered_lines)

# Write out the updated model with parameters
with open(model, "w") as f:
    f.write(altered_lines)

