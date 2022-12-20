#!/bin/bash
function print_separator {
    echo "------------------------------------------------------------"
}

# Basic help test
ppp -h
print_separator
ppp --help
print_separator
# Process command test
ppp process -h
print_separator
ppp process --help
print_separator
ppp process -s ./data/particles.nc --topo ./data/topo.nc -o ./data/output.nc
print_separator
# Should fail (file exists)
ppp process -s ./data/particles.nc --topo ./data/topo.nc -o ./data/output.nc
print_separator
ppp process -O -s ./data/particles.nc --topo ./data/topo.nc -o ./data/output.nc