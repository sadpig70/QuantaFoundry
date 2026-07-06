OPENQASM 3.0;
include "stdgates.inc";
qubit[3] q;

h q[0];
cz q[0], q[1];
cz q[0], q[2];
x q[0];
cx q[0], q[1];
cx q[0], q[2];
x q[0];
h q[0];
