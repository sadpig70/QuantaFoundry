OPENQASM 3.0;
include "stdgates.inc";
qubit[2] q;

cx q[0], q[1];
cp(1.57079632679) q[0], q[1];
