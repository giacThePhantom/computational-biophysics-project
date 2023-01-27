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
set output_file [open "../../../data/8K4D/vmd_data/rgyr.csv" w]
for {set i 0} {$i < $nf} {incr i} {
    set first_frame [atomselect top "alpha" frame $i]
    set rog [measure rgyr $first_frame]
    puts $output_file "${rog}"
    $first_frame delete
}
close $output_file
