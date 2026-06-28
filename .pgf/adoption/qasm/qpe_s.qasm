OPENQASM 3.0;
include "stdgates.inc";
qubit[3] q;

h q[0];
h q[1];
cz q[0], q[2];
cp(1.57079632679) q[1], q[2];
swap q[0], q[1];
h q[1];
cp(-1.57079632679) q[1], q[0];
h q[0];
