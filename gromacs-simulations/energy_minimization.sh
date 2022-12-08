#!/bin/bash
#PBS -l select=1:ncpus=5:mpiprocs=5:mem=10GB
#PBS -l walltime=00:10:00
#PBS -q short_cpuQ
#PBS -N energy_minimization
#PBS -o ${HOME}/logs/energy_minimization_log_out
#PBS -e ${HOME}/logs/energy_minimization_log_err
OUTDIR="${HOME}/data/energy_minimization/"

mkdir -p $OUTDIR

INPUT="${HOME}/data/energy_minimization/input.gro"
MINIM="${HOME}/data/energy_minimization/minim.mdp"
TOPOL="${HOME}/data/energy_minimization/topol.top"

cp ${HOME}/data/input.gro $INPUT

cp ${HOME}/data/mdp_files/minim.mdp $MINIM

cp ${HOME}/data/topol.top $TOPOL

module load gromacs-2021.5

gmx grompp -f $MINIM -c $INPUT -p $TOPOL -o "${OUTDIR}em.tpr"

gmx mdrun -V -deffnm "${OUTDIR}em"

gmx energy -f "${OUTDIR}em.edt" -o "${OUTDIR}potential.xvg"

module unload gromacs-2021.5
