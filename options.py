#! /usr/bin/env python

################################################################################
# 
# Nick Lange
# University of Victoria
# June 29, 2014
#
################################################################################
"""Define useful paths to executables"""

import os
join = os.path.join

work_dir = os.path.dirname(os.path.realpath(__file__))

bkg_dir = join(work_dir, 'muon-decay-background')
sig_dir = join(work_dir, 'muon-decay-darkphoton-newphysics')
analysis_dir = join(work_dir, 'newphysics-analysis')

mg5_dir = join(work_dir, 'madgraph5')
ma5_dir = join(work_dir, 'madanalysis5')

mg5 = join(mg5_dir, 'bin', 'mg5_aMC')
ma5 = join(ma5_dir, 'bin', 'ma5')

model_dir = join(work_dir, 'muon-darkphoton-feynmanrules')

model = join(model_dir, 'muon-darkphoton.fr')
model_templ = join(model_dir, 'muon-darkphoton.fr.template')
model_src = join(work_dir, os.path.basename(model).replace('.fr', '_UFO'))
model_dest = join(mg5_dir, 'models', os.path.basename(model).replace('.fr', '_UFO'))
model_script = join(model_dir, 'muon-darkphoton-feynmanrules.m')
ma5_script = join(work_dir, 'ma5_cmds.dat')
ma5_templ = join(work_dir, 'ma5_cmds.dat.templ')
me5_script = join(work_dir, 'me5_cmds.dat')

bkg_generate_script = join(work_dir, 'bkg_cmds.dat')
sig_generate_script = join(work_dir, 'sig_cmds.dat')

pkl_file = join(work_dir, 'seen_params.pkl')

