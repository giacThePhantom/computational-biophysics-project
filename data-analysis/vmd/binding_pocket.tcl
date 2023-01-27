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

set sel [lindex $argv 0]

set binding_pocket [atomselect top "protein and within 10 of resid $sel"]

for {set f 0 } {$f < $nf} {incr f} {
    $binding_pocket frame $f
    $binding_pocket update
    set output [$binding_pocket list]
    puts $output
}
