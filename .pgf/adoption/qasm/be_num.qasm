OPENQASM 3.0;
include "stdgates.inc";
qubit[2] q;

x q[1];
h q[0];
cz q[0], q[1];
h q[0];
x q[1];
