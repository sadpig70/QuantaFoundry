OPENQASM 3.0;
include "stdgates.inc";
qubit[3] q;

gate qpgf_ccz q0, q1, q2 { }  // opaque: ccz (3q), golden in registry/modules/ccz.sealed.json

x q[0];
x q[1];
x q[2];
// UNMAPPED ccz [0, 1, 2]  (QASM3 비표준 — opaque)
qpgf_ccz q[0], q[1], q[2];
x q[0];
x q[1];
x q[2];
