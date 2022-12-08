#!/bin/bash
#PBS -l select=1:ncpus=10:mpiprocs=10:mem=10GB
#PBS -l walltime=06:00:00
#PBS -q short_cpuQ
#PBS -N production_run
#PBS -o md_log_out
#PBS -e md_log_err


export OMP_NUM_THREADS=1
cd "${HOME}/data/md_input"

INDIR="${HOME}/data/md_input"
OUTDIR="${HOME}/data/md_output"

mkdir -p $OUTDIR

INPUT="${INDIR}/npt.gro"
PARAM="${INDIR}/md.mdp"
TOPOL="${INDIR}/topol.top"
CPT="${INDIR}/npt.cpt"
INDEX="${INDIR}/index.ndx"
CHECKPOINT="${OUTDIR}/state.cpt"

module load gromacs-2021.5

[ -f "${OUTDIR}/md.log" ] || gmx grompp -f $PARAM -c $INPUT -t $CPT -p $TOPOL -n $INDEX -o "${OUTDIR}/md"

[ -f "${OUTDIR}/state.cpt" ] || mpirun -np 10 gmx_mpi mdrun -deffnm "${OUTDIR}/md" -cpt 15 -cpo $CHECKPOINT

mpirun -np 10 gmx_mpi mdrun -cpi $CHECKPOINT

module unload gromacs-2021.5
