###########################################################
#
# Nick Lange
# July 23, 2014
#
# Write out param_card.dat with updated parameters
#
##########################################################

import MG5_aMC_v2_1_2_beta.madgraph.core.base_objects as base_objects
import MG5_aMC_v2_1_2_beta.models.import_ufo as import_ufo
import MG5_aMC_v2_1_2_beta.models.write_param_card as writter

model_name = 'muon-scalar_UFO'
output_file = './param_card.dat'

model = import_ufo.import_model(model_name)
writter = writter.ParamCardWriter(model)
writter.define_output_file(output_file)
writter.write_card()

