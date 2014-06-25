#!/bin/bash

# Nick Lange
# June 13, 2014

# Generate events for a given mass and set of couplings for our scalar
# Note: If these are changed, for now the param_card.dat will have to be updated
#       Maybe we will simply change this to say "Auto" and then trust the width calculated
#       by MadGraph, as long as we tune the accuracy

SCRIPT_DIR="$(dirname "$0")"

WORK_DIR=~/Dropbox/School/muonic-hydrogen
MG5_DIR=$WORK_DIR/MG5_aMC_v2_1_2_beta
FR_DIR=$WORK_DIR/muon-scalar-feynmanrules
MA5_DIR=$MG5_DIR/madanalysis5
BKG_DIR=$WORK_DIR/muon-decay-background
SIG_DIR=$WORK_DIR/muon-decay-newphysics

MG5=$MG5_DIR/bin/mg5_aMC

FR_SCRIPT=$WORK_DIR/muon-scalar-feynmanrules/muon-scalar-feynmanrules.m
MA5_SCRIPT=$SCRIPT_DIR/ma5_cmds.dat
ME5_SCRIPT=$SCRIPT_DIR/me5_cmds.dat
PHIWIDTH_SCRIPT=$SCRIPT_DIR/phi-decay_cmds.dat
BKGGENERATE_SCRIPT=$SCRIPT_DIR/bkg_cmds.dat
SIGGENERATE_SCRIPT=$SCRIPT_DIR/sig_cmds.dat

# Generate the Feynman rules from the model
MathKernel -script $FR_SCRIPT

# Update model in case it has changed
rm -rf $MG5_DIR/models/muon-scalar_UFO
mv $FR_DIR/muon-scalar_UFO $MG5_DIR/models

# Generate our cards if they don't exist
if [ ! -d "$BKG_DIR" ]; then
    $MG5 -f $BKGGENERATE_SCRIPT
fi

if [ ! -d "$SIG_DIR" ]; then
    $MG5 -f $SIGGENERATE_SCRIPT
fi

# TODO: Can we just do this in FeynRules?
# Update the width of the scalar
$MG5_DIR/bin/mg5_aMC -f $PHIWIDTH_SCRIPT
cp $WORK_DIR/phi-decay/Events/run_01/param_card.dat $BKG_DIR/Cards
cp $WORK_DIR/phi-decay/Events/run_01/param_card.dat $SIG_DIR/Cards

# See https://answers.launchpad.net/mg5amcnlo/+question/229140 for more details on running a script in madevent

# Background
$BKG_DIR/bin/madevent $ME5_SCRIPT

# Signal
$SIG_DIR/bin/madevent $ME5_SCRIPT

# Get the most recent run
BKG_RUN=`ls -dt $BKG_DIR/Events/* | grep run | head -1 | awk -F/ '{print $(NF)}'`
SIG_RUN=`ls -dt $SIG_DIR/Events/* | grep run | head -1 | awk -F/ '{print $(NF)}'`

# Copy the template script and insert our variables
# Use sed to replace the variables
sed -e "s;\${BKG_DIR};`echo ${BKG_DIR}`;" -e "s;\${SIG_DIR};`echo ${SIG_DIR}`;" -e "s;\${BKG_RUN};`echo ${BKG_RUN}`;" -e "s;\${SIG_RUN};`echo ${SIG_RUN}`;" $MA5_SCRIPT > $MA5_SCRIPT.tmp

# Generate the plots
$MA5_DIR/bin/ma5 --script $MA5_SCRIPT.tmp

rm $MA5_SCRIPT.tmp
