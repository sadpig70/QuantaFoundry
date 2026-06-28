OPENQASM 3.0;
include "stdgates.inc";
qubit[3] q;

h q[0];
cp(1.57079632679) q[1], q[0];
cp(0.785398163397) q[2], q[0];
h q[1];
cp(1.57079632679) q[2], q[1];
h q[2];
swap q[0], q[2];
