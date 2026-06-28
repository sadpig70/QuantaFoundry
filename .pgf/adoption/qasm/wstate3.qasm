OPENQASM 3.0;
include "stdgates.inc";
qubit[3] q;

x q[0];
ry(0.955316618125) q[1];
cx q[0], q[1];
ry(-0.955316618125) q[1];
cx q[0], q[1];
cx q[1], q[0];
ry(0.785398163397) q[2];
cx q[1], q[2];
ry(-0.785398163397) q[2];
cx q[1], q[2];
cx q[2], q[1];
