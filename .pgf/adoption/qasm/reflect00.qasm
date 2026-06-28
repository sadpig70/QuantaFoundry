OPENQASM 3.0;
include "stdgates.inc";
qubit[2] q;

x q[0];
x q[1];
cz q[0], q[1];
x q[0];
x q[1];
