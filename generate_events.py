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
import os
import sys
import shutil
import numpy as np

import logging

# Generate the Feynman rules from the model
def generate_model(**kwargs):
    """Generate the UFO model for a given set of parameters"""

    logger = logging.getLogger(__name__)
    logger.info('Begin generation of UFO model')

    # Get the lines from the model template
    templ_lines = read_template(options.model_templ)

    # Replace each instance of the parameter name with it's value
    if kwargs is not None:
        logger.info('Model parameters: %s' % kwargs)
        for param_name, param_value in kwargs.iteritems():
            # In the future, use a smarter regex instead of a replacement
            templ_lines = re.sub(param_name.upper() + '_REPLACE', modelify_parameter(param_value),
                                 templ_lines)

    # Write out model file for FeynRules
    logger.info('Writing model file to: %s' % options.model)

    write_lines(options.model, templ_lines)

    # Call FeynRules to create UFO model
    subprocess.call(['MathKernel', '-script', options.model_script])

    # Remove the model file and just leave the template
    os.remove(os.path.abspath(options.model))

    # Move the resulting UFO model file to MadGraph5
    move_UFO()

def read_template(template):
    """Read in the lines from the template file"""

    logger = logging.getLogger(__name__)
    logger.debug('Opening template file: %s' % template)

    with open(template, 'r') as f:
        lines = f.read()
        return lines

def write_lines(filename, lines):
    """Write out lines to filename"""

    with open(filename, 'w') as f:
        f.write(lines)

def modelify_parameter(x):
    """Return the numeric parameter x as a string that can be used by
    FeynRules"""

    # Set the numpy print format to have a width of 6 with scientific notation
    # and with 3 digits after the decimal place
    np.set_printoptions(formatter={'float': lambda y: format(y, '6.3E')})

    return re.sub('e', '*^', repr(x))

def delete_line_containing(param, string):
    """Delete a line containing <param> in string"""

    # Split on line separator and toss line if it contains param
    fixed_lines = [line for line in string.split(os.linesep) if param not in line]
    return os.linesep.join(fixed_lines)

def move_UFO():
    """Move the newly created model to the MadGraph5 models directory"""

    logger = logging.getLogger(__name__)
    logger.debug('Removing old model directory: %s' % options.model_dest)

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
        else:
            generate_param_card(os.path.basename(options.model_dest), os.path.join(options.bkg_dir, 'Cards', 'param_card.dat'))

    if sig:
        if not os.path.isdir(options.sig_dir):
            generate_sig_cards()
        else:
            generate_param_card(os.path.basename(options.model_dest), os.path.join(options.sig_dir, 'Cards', 'param_card.dat'))

def generate_param_card(modelname, output):
    """Generate param_card.dat for our model which we may need
    if the model is updated and we haven't recreated our event directories"""

    # Modify sys.path so we can import the below objects
    # See: http://stackoverflow.com/questions/279237/import-a-module-from-a-relative-path/6098238#6098238
    cmd_folder = os.path.realpath(os.path.abspath(options.mg5_dir))
    if cmd_folder not in sys.path:
        sys.path.insert(0, cmd_folder)

    import madgraph.core.base_objects as base_objects
    import models.import_ufo as import_ufo
    import models.write_param_card as writer

    logger = logging.getLogger(__name__)
    logger.debug('Writing out updated param_card to %s' % output)
    model = import_ufo.import_model(modelname)
    writer = writer.ParamCardWriter(model)
    writer.define_output_file(output)
    writer.write_card()

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

def generate_events(bkg=True, sig=True):
    """Generate Monte-Carlo events for given background and signal processes"""
    
    if bkg:
        generate_bkg_events()

    if sig:
        generate_sig_events()

def generate_bkg_events():
    """Generate Monte-Carlo events for a given background process"""

    logger = logging.getLogger(__name__)
    logger.info('Generating background events')

    # Call MadEvent from the generated cards from MadGraph
    madevent = os.path.join(options.bkg_dir, 'bin', 'madevent')
    subprocess.call([madevent, options.me5_script])
    
def generate_sig_events():
    """Generate Monte-Carlo events for a given signal process"""

    logger = logging.getLogger(__name__)
    logger.info('Generating signal events')

    # Call MadEvent from the generated cards from MadGraph
    madevent = os.path.join(options.sig_dir, 'bin', 'madevent')
    subprocess.call([madevent, options.me5_script])

def generate_report(bkg=True, sig=True):
    """Use MadAnalysis5 to generate a report with a histogram of events
    and a signal-to-background computation. Return the location of
    the reports"""

    logger = logging.getLogger(__name__)
    logger.info('Building MadAnalysis5 report')

    # Read in the MadAnalysis5 commands
    mascript = read_template(options.ma5_templ)

    if bkg:
        # Replace each instance of the parameter name with it's value
        event_dir = os.path.join(options.bkg_dir, 'Events')
        run_dir = os.path.join(event_dir, latest_dir(event_dir))
        mascript = re.sub('BKG_RUN_DIR_REPLACE', run_dir, mascript)
    else:
        # Remove the relevant line
        mascript = delete_line_containing('BKG_RUN_DIR_REPLACE', mascript)

    if sig:
        # Replace each instance of the parameter name with it's value
        event_dir = os.path.join(options.sig_dir, 'Events')
        run_dir = os.path.join(event_dir, latest_dir(event_dir))
        mascript = re.sub('SIG_RUN_DIR_REPLACE', run_dir, mascript)
    else:
        # Remove the relevant line
        mascript = delete_line_containing('SIG_RUN_DIR_REPLACE', mascript)

    # Replace the output directory
    mascript = re.sub('OUTPUT_DIR_REPLACE', options.analysis_dir, mascript)

    # Write out model file for FeynRules
    logger = logging.getLogger(__name__)
    logger.info('Writing MadAnalysis script to: %s' % options.ma5_script)

    write_lines(options.ma5_script, mascript)

    # Call MadAnalysis5
    subprocess.call([options.ma5, '--script', options.ma5_script])

    # Remove our script
    logger.debug('Removing MadAnalysis script: %s' % options.ma5_script)
    os.remove(os.path.abspath(options.ma5_script))

    options.pdf_report = os.path.join(run_dir, 'report.pdf')
    options.html_report = os.path.join(run_dir, 'report.html')
    options.param_card = os.path.join(run_dir, 'param_card.dat')

    logger.debug('Copying PDF report to: %s' % options.pdf_report)
    logger.debug('Copying HTML report to: %s' % options.html_report)

    # Copy the reports
    shutil.copy2(os.path.join(options.analysis_dir, 'PDF', 'main.pdf'), options.pdf_report)
    shutil.copy2(os.path.join(options.analysis_dir, 'HTML', 'index.html'), options.html_report)

def latest_dir(directory):
    """Return the most recently modified subdirectory within directory"""

    if not os.path.isdir(directory):
        logger = logging.getLogger(__name__)
        logger.error('Could not open as a directory: %s' % directory)
        exit()

    # List all directories and return the one with the latest modified
    # timestamp
    all_subdirs = [os.path.join(directory, subdir) for subdir in os.listdir(directory)
                   if os.path.isdir(os.path.join(directory, subdir))]
    return max(all_subdirs, key=os.path.getmtime)

def write_results(outfile, bkg=True, sig=True):
    """Write out the results with model parameters"""

    logger = logging.getLogger(__name__)
    logger.info('Writing out results to: %s' % outfile)

    # Store our results in a dictionary
    outs = {}
    outs['sb'] = np.nan

    if sig and bkg:
        # Extract the signal vs background computation
        from bs4 import BeautifulSoup
        html = open(options.html_report, 'r').read()
        soup = BeautifulSoup(html)

        # We need the last column and last row from the last table
        table = soup.find_all('table')[-1]
        tr = table.find_all('tr')[-1]
        td = tr.find_all('td')[-1]

        # This is the signal vs. background
        outs['sb'] = td.get_text().strip()

    param_card = open(options.param_card, 'r').read()

    # TODO: Make this general so it's not stuck with our model
    regex = re.compile('1\s+(.*)\s+\#\s+gsm')
    outs['gsm'] = regex.search(param_card).group(1)
    regex = re.compile('2\s+(.*)\s+\#\s+gse')
    outs['gse'] = regex.search(param_card).group(1)
    regex = re.compile('9000005\s+(.*)\s+\#\s+Mphi')
    outs['Mphi'] = regex.search(param_card).group(1)
    regex = re.compile('DECAY\s+9000005\s+(.*)')
    outs['Wphi'] = regex.search(param_card).group(1)

    with open(outfile, 'w') as file:
        for param, value in outs.items():
            file.write('%s: %s' % (param, value) + os.linesep)

def clean():
    """Clean the output directories"""

    logger = logging.getLogger(__name__)
    logger.info('Cleaning output directories')

    if os.path.isdir(options.bkg_dir):
        shutil.rmtree(options.bkg_dir)
    if os.path.isdir(options.sig_dir):
        shutil.rmtree(options.sig_dir)
    if os.path.isdir(options.analysis_dir):
        shutil.rmtree(options.analysis_dir)

def main():
    # Generate both signal and background
    bkg = True
    sig = True
    
    # Our ranges for our parameters
    mphi = np.linspace(1.5e-3, 100e-3, num=20)
    gsm = np.logspace(-6, -3, num=20)
    gse = 1.00e-06

    # Set logging options
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    if not bkg and not sig:
        logger.error('Must set at least one of signal and background to True')
        exit()

    # Purge our directories
    #clean()

    for mphi in mphi:
        for gsm in gsm:
            # Generate the model with given parameters
            generate_model( mphi=mphi, gsm=gsm, gse=gse )

            # Generate cards for MadGraph5
            generate_cards(bkg, sig) 

            # Generate events
            generate_events(bkg, sig)

            # Generate report
            generate_report(bkg, sig)

            # Extract useful variables from report and param_card
            output = os.path.join(os.path.dirname(options.param_card), 'report.dat')
            write_results(output, bkg, sig)

if __name__ == "__main__":
    main()
