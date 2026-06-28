OPENQASM 3.0;
include "stdgates.inc";
qubit[2] q;

swap q[0], q[1];
h q[1];
cp(-1.57079632679) q[1], q[0];
h q[0];
