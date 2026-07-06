OPENQASM 3.0;
include "stdgates.inc";
qubit[9] q;

ccx q[2], q[5], q[8];
ccx q[1], q[3], q[8];
ccx q[0], q[4], q[8];
ccx q[2], q[4], q[7];
ccx q[1], q[5], q[7];
ccx q[1], q[3], q[7];
ccx q[0], q[4], q[7];
ccx q[0], q[3], q[7];
ccx q[2], q[3], q[6];
ccx q[1], q[4], q[6];
ccx q[0], q[5], q[6];
ccx q[0], q[3], q[6];
