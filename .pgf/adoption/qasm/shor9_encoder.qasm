OPENQASM 3.0;
include "stdgates.inc";
qubit[9] q;

cx q[0], q[3];
cx q[0], q[6];
h q[0];
h q[3];
h q[6];
cx q[0], q[1];
cx q[0], q[2];
cx q[3], q[4];
cx q[3], q[5];
cx q[6], q[7];
cx q[6], q[8];
