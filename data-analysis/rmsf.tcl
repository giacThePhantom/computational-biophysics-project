mol new ../../data/post_processing_output/md.gro
mol addfile ../../data/post_processing_output/md_noPBC.xtc waitfor all first 1
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

set output_file [open "rmsf.csv" w]
set sel [atomselect top "alpha"]
set rmsf [measure rmsf $sel]
puts $output_file "${rmsf}"
$sel delete
close $output_file
