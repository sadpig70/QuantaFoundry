OPENQASM 3.0;
include "stdgates.inc";
qubit[2] q;

swap q[0], q[1];
cz q[0], q[1];
