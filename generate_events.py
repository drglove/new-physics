#! /usr/bin/env python

################################################################################
# Nick Lange
# June 29, 2014
#
# Generate events for a given mass and set of couplings for our scalar
#
################################################################################

import options

import subprocess
import re
import numpy as np

import logging

# Generate the Feynman rules from the model
def generate_model(**kwargs):
    """Generate the UFO model for a given set of parameters"""

    logger = logging.getLogger(__name__)
    logger.info('Begin generation of UFO model')

    # Get the lines from the model template
    templ_lines = read_model_template(options.model_templ)

    # Replace each instance of the parameter name with it's value
    if kwargs is not None:
        logger.info('Model parameters: %s' % kwargs)
        for param_name, param_value in kwargs.iteritems():
            templ_lines = replace_parameter(param_name, param_value,
                                            templ_lines)

    # Write out model file for FeynRules
    write_model(options.model, templ_lines)

    # Call FeynRules to create UFO model
    subprocess.call(['MathKernel', '-script', options.model_script])

    # Move the resulting UFO model file to MadGraph5
    move_UFO()

def read_model_template(model_template):
    """Read in the lines from the template model file"""

    logger = logging.getLogger(__name__)
    logger.info('Opening model template file: %s' % model_template)

    with open(model_template, 'r') as f:
        lines = f.read()
        return lines

def write_model(filename, lines):
    """Write out model lines to filename"""

    logger = logging.getLogger(__name__)
    logger.info('Writing model file to: %s' % filename)

    with open(filename, 'w') as f:
        f.write(lines)

def replace_parameter(param_name, param_value, string):
    """Replace upper(<param_name>)_REPLACE with <param_value> in string"""
    #TODO: In the future, replace our regex so we don't need a placeholder

    return re.sub(param_name.upper() + '_REPLACE', modelify_parameter(param_value),
           string)

def modelify_parameter(x):
    """Return the numeric parameter x as a string that can be used by
    FeynRules"""

    # Set the numpy print format to have a width of 6 with scientific notation
    # and with 3 digits after the decimal place
    np.set_printoptions(formatter={'float': lambda y: format(y, '6.3E')})

    return re.sub('e', '*^', repr(x))

def move_UFO():
    """Move the newly created model to the MadGraph5 models directory"""

    logger = logging.getLogger(__name__)
    logger.debug('Removing old model directory: %s' % options.model_dest)

    import shutil
    # Remove the old model
    if os.path.isdir(options.model_dest):
        shutil.rmtree(options.model_dest, ignore_errors=True)

    # Move the new model in place
    shutil.move(options.model_src, options.model_dest)

def generate_cards(bkg=True, sig=True):
    """Generate MadGraph5 cards for signal and events"""

    
    if bkg:
        if not os.path.isdir(options.bkg_dir):
            generate_bkg_cards()

    if sig:
        if not os.path.isdir(options.sig_dir):
            generate_sig_cards()


def generate_bkg_cards():
    """Generate MadGraph5 cards for background events"""

    logger = logging.getLogger(__name__)
    logger.info('Generating new MadGraph5 skeleton for background')

    subprocess.call([options.mg5, '-f', options.bkg_generate_script])

def generate_sig_cards():
    """Generate MadGraph5 cards for signal events"""

    logger = logging.getLogger(__name__)
    logger.info('Generating new MadGraph5 skeleton for signal')

    subprocess.call([options.mg5, '-f', options.sig_generate_script])

def main():
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    generate_model( mphi=15.0e-03, gsm=1.00e-03, gse=1.00e-06 )
    generate_cards() 

if __name__ == "__main__":
    main()
