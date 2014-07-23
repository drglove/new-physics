#!/bin/bash

# Nick Lange
# June 25, 2014
#
# Output variables used

WORK_DIR=~/Dropbox/School/muonic-hydrogen/generate-events
BKG_DIR=$WORK_DIR/muon-decay-background
SIG_DIR=$WORK_DIR/muon-decay-newphysics

MG5_DIR=$WORK_DIR/MG5_aMC_v2_1_2_beta
MA5_DIR=$WORK_DIR/madanalysis5

MG5=$MG5_DIR/bin/mg5_aMC
MODEL_DIR=$WORK_DIR/muon-scalar-feynmanrules

SCRIPT_DIR="$(dirname "$0")"

MODEL_SCRIPT=$MODEL_DIR/muon-scalar-feynmanrules.m
MA5_SCRIPT=$SCRIPT_DIR/ma5_cmds.dat
ME5_SCRIPT=$SCRIPT_DIR/me5_cmds.dat
PHIWIDTH_SCRIPT=$SCRIPT_DIR/phi-decay_cmds.dat
BKGGENERATE_SCRIPT=$SCRIPT_DIR/bkg_cmds.dat
SIGGENERATE_SCRIPT=$SCRIPT_DIR/sig_cmds.dat
UPDATE_PARAM_CARD=$MG5_DIR/update_param_card.py
