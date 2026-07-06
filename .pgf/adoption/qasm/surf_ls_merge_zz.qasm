OPENQASM 3.0;
include "stdgates.inc";
qubit[9] q;

h q[0];
cz q[0], q[1];
cz q[0], q[2];
cz q[0], q[5];
cz q[0], q[6];
h q[0];
