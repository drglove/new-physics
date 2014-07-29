#!/bin/bash
###############################################################################
# 
# Nick Lange
# June 29, 2014
#
# Generate events for all our couplings and process the results
#
###############################################################################

source variables.sh

python $UPDATE_MODEL_PARAMS

./generate_events.sh

