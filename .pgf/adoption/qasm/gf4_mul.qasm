OPENQASM 3.0;
include "stdgates.inc";
qubit[6] q;

ccx q[0], q[2], q[4];
ccx q[0], q[3], q[4];
ccx q[1], q[2], q[4];
ccx q[0], q[2], q[5];
ccx q[1], q[3], q[5];
