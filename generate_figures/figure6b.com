#!/bin/sh
# No touch: one parameter set.

flgeneric=a1
fla=a2
factor=1.0

sed 's/scan=n/scan=e\nT_CELL Av parmin=0.0001 parmax=20.0001 npar=20 nrepeat=10/' tc.n.$flgeneric > tc.n.$fla

../simulation_program/tc.ex $fla

../scripts/mfc.com at $fla $factor


