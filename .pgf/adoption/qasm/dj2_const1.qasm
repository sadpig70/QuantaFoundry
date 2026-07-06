OPENQASM 3.0;
include "stdgates.inc";
qubit[3] q;

x q[2];
h q[2];
h q[0];
h q[1];
x q[2];
h q[0];
h q[1];
