#!/usr/bin/env python3

# This is the release v0.1.0 of runpred
#
# Created by P. Groningsson, 2014-10-10

## import libs
import sys, getopt

## Print help
def usage():
    print ("Usage: runpred [Options]... [ARGS]...\n\
Prediction of running performance by calculating V02max.\n\n\
Options:\n\
 -h, --help      : Show this help message and exit\n\
 -d, --distance  : Running distance\n\
 -t, --time      : Running time")
    return


## Get input from command line
argv = sys.argv[1:] #input arguments

try:
  optlist, args = getopt.gnu_getopt(argv, "hd:t:", ["help", "distance=", "time="])
  #print (args)
except getopt.GetoptError as err:
  print (str(err)) #Print error msg
  print ("type 'runpred --help' for more information")
  sys.exit(2)

for opt, arg in optlist:
    if opt in ("-h", "--help"):
        usage()
        sys.exit()
    elif opt in ("-d", "--distance"):
        distance = arg
    elif opt in ("-t", "--time"):
        time = arg
