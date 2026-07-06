OPENQASM 3.0;
include "stdgates.inc";
qubit[3] q;

gate qpgf_ccz q0, q1, q2 { }  // opaque: ccz (3q), golden in registry/modules/ccz.sealed.json

t q[0];
t q[1];
t q[2];
cp(1.57079632679) q[0], q[1];
cp(1.57079632679) q[0], q[2];
cp(1.57079632679) q[1], q[2];
// UNMAPPED ccz [0, 1, 2]  (QASM3 비표준 — opaque)
qpgf_ccz q[0], q[1], q[2];
