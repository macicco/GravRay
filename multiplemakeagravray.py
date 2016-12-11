#!/usr/bin/env python
from gravray import *
from os import path,system

#############################################################
#USAGE
#############################################################
usage="""Make multiple Parallel GRT analysis of a whole geographic region.

   python multipleparallelgravray.py <nprocs> <dates_file> <deg|rad> <locations_file> <deg|rad> <directions_file> <velocities_file> [<height> <rundir>]

Where:

   <nprocs>: number of processors used for the analysis.

   <dates_file>: File the date of the analysis

   <deg|rad>: indicate if directions are in degrees or radians.

   <locations_file>: file with the geographical locatins (generated
                     using eg. generatedirections.py)

   <directions_file>: file with the impacting directons (generated
                     using eg. generatedirections.py)

   <velocities_file>: file with initial velocities (generated
                      using eg. generatevelocities.py)

   <altitude>: altitude where the rays start in meters (default:
               80,000 m)

   <rundir>: Directory with the launch scripts will be created.
"""

#############################################################
#PREPARE RUN
#############################################################
iarg=1
try:
    nprocs=int(argv[iarg]);iarg+=1

    datesfile=argv[iarg];iarg+=1

    degloc=argv[iarg];iarg+=1
    locfile=argv[iarg];iarg+=1

    degdir=argv[iarg];iarg+=1
    dirfile=argv[iarg];iarg+=1

    qvel=0
    velfile=argv[iarg];iarg+=1
except:
    print usage
    exit(1)

#ALTITUDE
try:h=float(argv[iarg]);iarg+=1
except:h=8e4

#DIRECTORY
try:rundir=argv[iarg];iarg+=1
except:rundir="."

#############################################################
#PREPARE
#############################################################
System("make")

#############################################################
#READ DATES FILE
#############################################################
f=open(datesfile)
dates=[]
for date in f:
    dates+=[date.replace("\n","")]

#############################################################
#CREATE RUNS
#############################################################
i=1
for date in dates:
    makefile="%s/makeagravray-%d.sh"%(rundir,i)
    name='Run %s'%date
    print "Creating parallel gravray %d in %s..."%(i,makefile)
    cmd="python parallelgravray.py %d '%s'  %s %s   %s %s   %s %s   '%s'   %f   %s   0"%(nprocs,date,degloc,locfile,degdir,dirfile,qvel,velfile,name,h,makefile)
    print "\tCommand: ",cmd
    system(cmd)
    i+=1