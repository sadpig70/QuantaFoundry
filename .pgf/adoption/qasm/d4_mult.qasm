OPENQASM 3.0;
include "stdgates.inc";
qubit[6] q;

cx q[2], q[5];
ccx q[2], q[4], q[3];
ccx q[1], q[4], q[3];
cx q[1], q[4];
cx q[0], q[3];
