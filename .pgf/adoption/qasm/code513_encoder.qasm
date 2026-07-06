OPENQASM 3.0;
include "stdgates.inc";
qubit[5] q;

cx q[0], q[1];
cx q[0], q[2];
cx q[0], q[3];
cx q[0], q[4];
h q[0];
h q[1];
h q[2];
h q[3];
h q[4];
cz q[0], q[1];
cz q[1], q[2];
cz q[2], q[3];
cz q[3], q[4];
cz q[4], q[0];
