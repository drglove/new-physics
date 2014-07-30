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
sig_dir = join(work_dir, 'muon-decay-newphysics')

mg5_dir = join(work_dir, 'MG5_aMC_v2_1_2_beta')
ma5_dir = join(work_dir, 'madanalysis5')

mg5 = join(mg5_dir, 'bin', 'mg5_aMC')
ma5 = join(ma5_dir, 'bin', 'ma5')

model_dir = join(work_dir, 'muon-scalar-feynmanrules')

model = join(model_dir, 'muon-scalar.fr')
model_templ = join(model_dir, 'muon-scalar.fr.template')
model_src = join(work_dir, os.path.basename(model).replace('.fr', '_UFO'))
model_dest = join(mg5_dir, 'models', os.path.basename(model).replace('.fr', '_UFO'))
model_script = join(model_dir, 'muon-scalar-feynmanrules.m')
ma5_script = join(work_dir, 'ma5_cmds.dat')
me5_script = join(work_dir, 'me5_cmds.dat')

bkg_generate_script = join(work_dir, 'bkg_cmds.dat')
sig_generate_script = join(work_dir, 'sig_cmds.dat')

update_param_card = join(mg5_dir, 'update_param_card.py')
update_model_params = join(work_dir, 'update_model_params.py')
parse_html = join(work_dir, 'output_results.py')

