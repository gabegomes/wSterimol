#!/usr/bin/python
from __future__ import print_function, absolute_import
import os, sys, timeit
from datetime import timedelta

#Pymol API
from pymol import cmd

# Weighted Sterimol Program version
version = 1.03

########################################
########## w S T E R I M O L ###########
########################################

# Generate the wSterimol parameters from the optimised structures
# Use in Pymol command prompt:
# run wSterimol.py
# wSterimol dihedrals, atomid1, atomid2, (radii, walltime, directory, setup_path, verbose, force)

def wSterimol(dihedrals, atomid1 = 1, atomid2 = 2, directory = "temp", setup_path = '.', walltime = 300,  verbose = "False", force = False):
    # Log generation
    log_path = "log-%s" % (datetime.date.today())
    if os.path.exists(log_path+".pylog"):
        print("Warning: Continuing previous log file [%s.pylog]" % log_path)
    wlog = Log(log_path,"pylog")
    # Do weighted Sterimol
    generate(dihedrals, directory, setup_path, verbose, force)
    filter_gen(directory, setup_path, verbose)
    prepare_file(directory, setup_path, verbose)
    optimisation(directory, walltime, verbose, setup_path)
    filter_opt(directory, setup_path, verbose)
    Sterimol(atomid1, atomid2, directory, setup_path, verbose)
    weight(setup_path, verbose)
    wlog.write("---- wSterimol finished ----\n")
    wlog.finalize()
cmd.extend("wSterimol",wSterimol)


class Log:
    def __init__(self,filein,suffix):
        # Create the log file at the input path
        self.start_time = timeit.default_timer()
        self.log = open(filein+"."+suffix, 'a+' )

    # Write a message to the log and the terminal by default
    def write(self, message, verbose = True):
        # Print the message
        if verbose: print(message) # versatile, depend on the called function
        # Write to log
        self.log.write(message + "\n")

    # Write a fatal error, finalize and terminate the program
    def fatal(self, message):
        # Print the message
        print(message+"\n")
        # Write to log
        self.log.write(message + "\n")
        # Finalize the log
        self.finalize()
        # End the program
        sys.exit(1)

    # Finalize the log file
    def finalize(self):
        self.end_time = timeit.default_timer()
        self.log.write("Time elapsed during script execution: %s \n" % timedelta(seconds=self.end_time - self.start_time))
        self.log.close()
