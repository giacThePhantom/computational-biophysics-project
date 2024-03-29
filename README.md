# comp-bio-project
Project of the course of computational biology, 2022-2023


## Gromacs simulation
A collection of PBS scripts used to perform the molecular simulation:

- 01_energy_minimization.pbs performs the energy minimization step.
- 02_nvt.pbs performs the NVT step.
- 03_npt.pbs performs the NPT step.
- 04_production_run.pbs performs the molecular dynamics simulation.
- 05_post_processing.sh performs the post processing on the molecular dynamics simulation results.
- chain_jobs.sh allows to launch a number of consecutive job to the cluster

## Data analysis
A collection of python and tcl script used to analyse the results of the molecular simulation

### VMD

- alignment.tcl aligns the trajectory preparing it for successive analysis.
- binding_pocket.tcl returns a line containing each residue less than 10 angstrom distant from the ligand for each frame.
- radius-of-gyration.tcl computes the radius of gyration of the protein during the trajectory, writing a csv file containing it for each frame.
- rmsd.tcl computes the all-to-all rmsd writing the results to a csv file
- rmsf.tcl computes the rmsf for the protein, writing the result to a csv file

### Global analysis:
A file containing a collection of functions to plot:

- Potential during em.
- Temperature during nvt.
- Pressure during npt.
- Volume during npt.
- The all-to-all rmsd.
- The radius of gyration.
- The rmsf.
- The contact map.
- Clustering.
- Block analysis.
- Autocorrelation analysis.

### Utility
A collection of variables and functions useful throughout the analysis.

### Plot HBonds
Takes as input the hbond analysis performed by vmd and plots the corresponding number of hidrogen bonds in time.

### Get residues Proximal To Ligand
Takes as input:

- The gro file of the protein.
- The trajectory.
- The tcl script binding_pocket.tcl
- A csv file of output for the first monomer.
- A csv file of output for the second monomer.
- The residue of one of the two ligands

And writes in the two csv files a matrix containing in each line the residues less than 10 angstrom with respect with the ligand given in input. Each line represents a frame.

### Get Binding Pocket
Takes as input the two csv file generated with get_residues_proximal_to_ligand.py and two csv files.
This script will write in the two csv file all the residues that stays proximal to the ligand for 70% of the identified frame in the identified steps of ligand position in the two monomers.

### Ligand Proximity
Ligand proximity takes as input one of the two csv files generated by get_residues_proximal_to_ligand, the name of the output image and the number of the monomer of interest and plots the residues proximal to the ligand in time, highlighting the corresponding binding pocket for the monomer.
