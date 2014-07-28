#!/bin/bash

# Nick Lange
# June 13, 2014

# Generate events for a given mass and set of couplings for our scalar
# Note: If these are changed, for now the param_card.dat will have to be updated
#       Maybe we will simply change this to say "Auto" and then trust the width calculated
#       by MadGraph, as long as we tune the accuracy

source variables.sh

# Generate the Feynman rules from the model
MathKernel -script $MODEL_SCRIPT

# Update model in case it has changed
rm -rf $MG5_DIR/models/muon-scalar_UFO
mv $SCRIPT_DIR/muon-scalar_UFO $MG5_DIR/models

# Generate our cards if they don't exist
if [ ! -d "$BKG_DIR" ]; then
    $MG5 -f $BKGGENERATE_SCRIPT
fi

if [ ! -d "$SIG_DIR" ]; then
    $MG5 -f $SIGGENERATE_SCRIPT
fi

# Update our param_card.dat from the model
# Note: param_card_default.dat does not change and the param_card.dat used in each run
#       is output alongside the events with the parameters used from our patch
python $UPDATE_PARAM_CARD
cp ./param_card.dat $BKG_DIR/Cards
cp ./param_card.dat $SIG_DIR/Cards
rm param_card.dat

# Update the width of the scalar
# FeynRules does this now, since there is just one 1->2 decay
# Below is how we used to do this, by generating decay events for the phi
#$MG5_DIR/bin/mg5_aMC -f $PHIWIDTH_SCRIPT
#cp $WORK_DIR/phi-decay/Events/run_01/param_card.dat $BKG_DIR/Cards
#cp $WORK_DIR/phi-decay/Events/run_01/param_card.dat $SIG_DIR/Cards

# See https://answers.launchpad.net/mg5amcnlo/+question/229140 for more details on running a script in madevent

# Background
$BKG_DIR/bin/madevent $ME5_SCRIPT

# Signal
$SIG_DIR/bin/madevent $ME5_SCRIPT

# Get the most recent run
BKG_RUN=`ls -dt $BKG_DIR/Events/* | grep run | head -1 | awk -F/ '{print $(NF)}'`
SIG_RUN=`ls -dt $SIG_DIR/Events/* | grep run | head -1 | awk -F/ '{print $(NF)}'`

# Latest directory (export so these can be seen in Python below)
export BKG_RUN_DIR=$BKG_DIR/Events/$BKG_RUN
export SIG_RUN_DIR=$SIG_DIR/Events/$SIG_RUN

# Copy the template script and insert our variables
# Use sed to replace the variables
sed -e "s;\${BKG_DIR};`echo ${BKG_DIR}`;" -e "s;\${SIG_DIR};`echo ${SIG_DIR}`;" -e "s;\${BKG_RUN};`echo ${BKG_RUN}`;" -e "s;\${SIG_RUN};`echo ${SIG_RUN}`;" $MA5_SCRIPT > $MA5_SCRIPT.tmp

# Generate the plots
$MA5_DIR/bin/ma5 --script $MA5_SCRIPT.tmp

rm $MA5_SCRIPT.tmp

# Keep the report with the signal events
cp newphysics-analysis/PDF/main.pdf $SIG_RUN_DIR/report.pdf
cp newphysics-analysis/HTML/index.html $SIG_RUN_DIR/report.html

# Extract the signal vs. background from report.html
python $PARSE_HTML
