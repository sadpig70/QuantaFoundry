OPENQASM 3.0;
include "stdgates.inc";
qubit[5] q;

cswap q[0], q[3], q[4];
cswap q[0], q[2], q[3];
cswap q[0], q[1], q[2];
cx q[0], q[1];
cx q[0], q[2];
cx q[0], q[3];
cx q[0], q[4];
