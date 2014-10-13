#!/usr/bin/env python3

# This is the release v0.2.0 of runpred
#
# Created by P. Groningsson, 2014-10-13

## import libs
import sys, getopt, time, datetime
from math import exp

## Print help
def usage():
    print ("Usage: runpred [Options]... [ARGS]...\n\
Prediction of running performance by calculating V02max.\n\n\
Options:\n\
 -h, --help      : Show this help message and exit\n\
 -d, --distance  : Running distance (km)\n\
 -dp,--dpred     : Distance for prediction (km)\n\
 -t, --time      : Running time (hh:mm:ss)\n\
 -w, --weight    : Weight (% of difference)")
    return#--------Main program--------------
def main():
  ## Get input from command line
  argv = sys.argv[1:] #input arguments

  try:
    optlist, args = getopt.gnu_getopt(argv, "hd:t:w:", ["help", "distance=",\
    "dpred=", "time=", "weight="])
  except getopt.GetoptError as err:
    print (str(err)) #Print error msg
    print ("type 'runpred --help' for more information")
    sys.exit(2)

  distance = False
  pred_distance = False
  runtime = False
  weight = False
  for opt, arg in optlist:
    if opt in ("-h", "--help"):
      usage()
      sys.exit()
    elif opt in ("-d", "--distance"):
      distance = float(arg)
    elif opt in ("--dpred"):
      pred_distance = float(arg)
    elif opt in ("-t", "--time"):
      runtime = arg
    elif opt in ("-w", "--weight"):
      weight = float(arg)

  if not runtime:
    print ("Running time must specified")
    print ("type 'runpred --help' for more information")
    sys.exit(2)
  else: # Convert time string to minutes:
    a=time.strptime(runtime, "%H:%M:%S")
    runtime_min=datetime.timedelta(hours=a.tm_hour, minutes=a.tm_min, \
    seconds=a.tm_sec).seconds/60

  if not distance:
    print ("Running distance must be specified")
    print ("type 'runpred --help' for more information")
    sys.exit(2)
  #else: # Calculate speed in km/min
    #speed_m_min = float(distance)*1000/runtime_min

  # Calculate running pace
  pace = runtime_min/distance # min/km
  minutes = str(int(pace))
  seconds = pace % 1 * 60
  if seconds < 10: seconds = "0"+str(round(seconds))
  else: seconds = str(round(seconds))

  print ("Pace = {0}:{1} [m:ss]/km".format(minutes,seconds))
  # Calculate VO2max
  VO2max = VO2max_fun(distance,runtime_min)
  print ("VO2max = {0}".format(round(VO2max, 2)))

  if not pred_distance:
    sys.exit()
  # -----------Prediction---------------------
  print ("----------Prediction-----------")
  if weight: # Ajust VO2max for weight change
    VO2max = VO2max/(1.0+weight)
  pred_time = runtime_min*pred_distance/distance
  time_lo = pred_time*0.5
  time_hi = pred_time*2.0
  delta = abs(VO2max_fun(pred_distance, pred_time) - VO2max)
  while delta > 1e-6:
    pred_VO2max = VO2max_fun(pred_distance, pred_time)
    if pred_VO2max < VO2max:
      time_hi = pred_time
    else:
      time_lo = pred_time
    pred_time = (time_lo+time_hi)/2.0
    delta = abs(pred_VO2max-VO2max)

  hours = pred_time/60
  minutes = hours%1*60
  seconds = minutes%1*60
  hours = str(int(hours))
  if minutes < 10: minutes = "0"+str(int(minutes))
  else: minutes = str(int(minutes))
  if seconds < 10: seconds = "0"+str(round(seconds))
  else: seconds = str(round(seconds))
  print ("Time = {0}:{1}:{2} [h:mm:ss]".format(hours, minutes, seconds))

  pred_pace = pred_time/pred_distance
  minutes = str(int(pred_pace))
  seconds = pred_pace % 1 * 60
  if seconds < 10: seconds = "0"+str(round(seconds))
  else: seconds = str(round(seconds))
  print ("Pace = {0}:{1} [m:ss]/km".format(minutes,seconds))

def VO2max_fun(distance, runtime_min):
  # VO2max according to Jack Daniels formula
  speed_m_min = distance*1000/runtime_min
  VO2 = -4.6+0.182258*speed_m_min+0.000104*speed_m_min**2
  percent_max = 0.8+0.1894393*exp(-0.012778*runtime_min) \
  + 0.2989558*exp(-0.1932605*runtime_min)
  VO2max = VO2/percent_max
  return VO2max

if __name__ == "__main__":
  main()
