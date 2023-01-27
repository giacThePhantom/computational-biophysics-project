mol new ../../../data/8K4D/400ns/md.gro
mol addfile ../../../data/8K4D/400ns/md_noPBC.xtc waitfor all

set nf [molinfo top get numframes]
set all [atomselect top "all"]
set ref_0 [atomselect top "protein and name CA" frame 0]
set ref [atomselect top "protein and name CA"]
for {set f 0 } {$f < $nf} {incr f} {
    $ref frame $f
    $all frame $f
    set M [measure fit $ref $ref_0]
    $all move $M
}

set nf [molinfo top get numframes]

set output_file [open "rmsd.csv" w]
set first_frame [atomselect top "alpha"]
set second_frame [atomselect top "alpha"]


for {set i 0} {$i < $nf} {incr i} {
    $first_frame frame $i
    for {set j [expr 0] } {$j < $nf} {incr j} {
        $second_frame frame $j
        set rmsd [measure rmsd $first_frame $second_frame]
        puts $output_file "${i},${j},${rmsd}"
    }
}
close $output_file
