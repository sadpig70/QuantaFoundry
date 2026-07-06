OPENQASM 3.0;
include "stdgates.inc";
qubit[8] q;

h q[0];
cx q[0], q[1];
cx q[0], q[4];
cx q[0], q[6];
h q[5];
cx q[5], q[0];
cx q[5], q[1];
cx q[5], q[7];
h q[2];
cx q[2], q[3];
cx q[2], q[4];
cx q[2], q[6];
