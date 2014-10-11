#!/usr/bin/env python3

# This is the release v0.1.0 of runpred
#
# Created by P. Groningsson, 2014-10-10

## import libs
import sys, getopt, time, datetime

## Print help
def usage():
    print ("Usage: runpred [Options]... [ARGS]...\n\
Prediction of running performance by calculating V02max.\n\n\
Options:\n\
 -h, --help      : Show this help message and exit\n\
 -d, --distance  : Running distance (km)\n\
 -t, --time      : Running time (hh:mm:ss)\n\
 -w, --weight    : Weight (kg)")
    return

## Get input from command line
argv = sys.argv[1:] #input arguments

try:  optlist, args = getopt.gnu_getopt(argv, "hd:t:w:", ["help", "distance=",\
 "time=", "weight="])
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
        runtime = arg
    elif opt in ("-w", "--weight"):
        weight = arg

if not "runtime" in locals():
  print ("Running time must specified")
  print ("type 'runpred --help' for more information")
  sys.exit(2)
else: # Convert time string to minutes:
  a=time.strptime(runtime, "%H:%M:%S")
  runtime_min=datetime.timedelta(hours=a.tm_hour, minutes=a.tm_min, \
  seconds=a.tm_sec).seconds/60
  print (runtime_min);
