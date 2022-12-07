#!/bin/bash
#PBS -l select=1:ncpus=10:mpiprocs=10:mem=10GB
#PBS -l walltime=03:00:00
#PBS -q short_cpuQ
#PBS -N nvt
#PBS -o nvt_log_out
#PBS -e nvt_log_err


export OMP_NUM_THREADS=1
cd "${HOME}/data/npt_input"

INDIR="${HOME}/data/npt_input"
OUTDIR="${HOME}/data/npt_output"

mkdir -p $OUTDIR

INPUT="${INDIR}/nvt.gro"
CPT="${INDIR}/nvt.cpt"
PARAM="${INDIR}/npt.mdp"
TOPOL="${INDIR}/topol.top"
INDEX="${INDIR}/index.ndx"


module load gromacs-2021.5

gmx grompp -f $PARAM -c $INPUT -t $CPT -r $INPUT -p $TOPOL -n $INDEX -o "${OUTDIR}/npt.tpr"

mpirun -np 10 gmx_mpi mdrun -deffnm "${OUTDIR}/npt"

module unload gromacs-2021.5
