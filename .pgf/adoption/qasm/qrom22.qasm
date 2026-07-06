OPENQASM 3.0;
include "stdgates.inc";
qubit[4] q;

x q[0];
x q[1];
ccx q[0], q[1], q[3];
x q[0];
x q[1];
x q[0];
ccx q[0], q[1], q[2];
x q[0];
x q[1];
ccx q[0], q[1], q[2];
ccx q[0], q[1], q[3];
x q[1];
