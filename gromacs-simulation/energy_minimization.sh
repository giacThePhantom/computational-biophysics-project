#!/bin/bash
#PBS -l select=1:ncpus=8:mpiprocs=8:mem=10GB
#PBS -l walltime=00:10:00
#PBS -q short_cpuQ
#PBS -N energy_minimization
#PBS -o energy_minimization_log_out
#PBS -e energy_minimization_log_err


export OMP_NUM_THREADS=1
cd "${HOME}/data/energy_minimization"

INDIR="${HOME}/data/em_input"
OUTDIR="${HOME}/data/em_output"

mkdir -p $OUTDIR

INPUT="${INDIR}/input.gro"
MINIM="${INDIR}/minim.mdp"
TOPOL="${INDIR}/topol.top"


module load gromacs-2021.5

gmx grompp -f $MINIM -c $INPUT -p $TOPOL -o "${OUTDIR}/em.tpr"

gmx mdrun -deffnm "${OUTDIR}/em"

module unload gromacs-2021.5
