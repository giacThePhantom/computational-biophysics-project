#!/bin/bash

jobid=$(qsub ${HOME}/computational-biophysics-project/gromacs-simulation/05_production_run.pbs | awk '{n=split($0,a,".");print(a[1])}')
echo "launched job $jobid"
for i in {1..10} # total number of restarts, change it.
do
  jobidold=$jobid
  jobid=$(qsub -W depend=afterany:${jobidold} ${HOME}/computational-biophysics-project/gromacs-simulation/05_production_run.pbs)
  echo "launched job $jobid -depending on $jobidold"
done
