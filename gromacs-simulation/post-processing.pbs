#!/bin/bash

export OMP_NUM_THREADS=1

INDIR="${HOME}/data/post_processing_input"
OUTDIR="${HOME}/data/post_processing_output"

mkdir -p $OUTDIR

TPR="${INDIR}/md.tpr"
XTC="${INDIR}/md.xtc"
MIDOUTNAME="${OUTDIR}/md_nojump.xtc"
OUTNAME="${OUTDIR}/md_noPBC.xtc"
FIRSTFLAGS="-pbc nojump -center"
SECONDFLAGS="-pbc mol -center"

module load gromacs-2021.5

gmx trjconv -s $TPR -f $XTC -o $MIDOUTNAME $FIRSTFLAGS
gmx trjconv -s $TPR -f $MIDOUTNAME -o $OUTNAME $SECONDFLAGS

module unload gromacs-2021.5
