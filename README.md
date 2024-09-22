# ns2-integration
# NS2 Simulation Script
set ns [new Simulator]
set nodes_list {2 5}  ;# Start with fewer nodes for debugging
set simulation_time 50 ;# in seconds

# Read predictions from the CSV file
set prediction_file [open "model_predictions.csv" r]
set prediction_data [read $prediction_file]
close $prediction_file

# Split the predictions data by lines
set predictions_list [split $prediction_data "\n"]

# Iterate through each node count
foreach num_nodes $nodes_list {
    # Create a list to hold the nodes
    set nodes {}

    # Create nodes and set routing protocols
    for {set i 0} {$i < $num_nodes} {incr i} {
        set node [$ns node]
        lappend nodes $node  ;# Store each node in the nodes list
    }

    # Create links between nodes
    for {set i 0} {$i < $num_nodes} {incr i} {
        for {set j 0} {$j < $num_nodes} {incr j} {
            if {$i != $j} {
                $ns duplex-link [lindex $nodes $i] [lindex $nodes $j] 1Mb 10ms DropTail
            }
        }
    }

    # Create a UDP agent and attach to a source and destination
    set udp_src [new Agent/UDP]
    set udp_sink [new Agent/Null]
    
    # Attach the agents to nodes
    $ns attach-agent [lindex $nodes 0] $udp_src
    $ns attach-agent [lindex $nodes 1] $udp_sink
    
    # Connect the agents
    $ns connect $udp_src $udp_sink

    # Schedule packets to send
    $udp_src send 1000  ;# Send 1000 bytes at a time
    $ns at 1.0 "$udp_src start"

    # Determine prediction for the current node count
    set prediction_index [expr {$num_nodes / 10}]  ;# Adjust based on your prediction structure
    set prediction_value [lindex $predictions_list $prediction_index]

    # Implement logic based on the prediction
    if { $prediction_value == "2" } {
        puts "Simulation with $num_nodes nodes: Normal operation."
    } elseif { $prediction_value == "1" } {
        puts "Simulation with $num_nodes nodes: Gray hole detected."
    } elseif { $prediction_value == "0" } {
        puts "Simulation with $num_nodes nodes: Black hole detected."
    }

    # Finish the simulation
    $ns at $simulation_time "finish"

    # Run the simulation
    puts "Running simulation with $num_nodes nodes..."
    $ns run
}

proc finish {} {
    global ns
    $ns flush-trace
    puts "Simulation finished."
    exit 0
}
