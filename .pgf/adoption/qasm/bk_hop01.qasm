OPENQASM 3.0;
include "stdgates.inc";
qubit[3] q;

h q[0];
x q[1];
cz q[0], q[2];
z q[0];
h q[0];
