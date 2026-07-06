OPENQASM 3.0;
include "stdgates.inc";
qubit[3] q;

gate qpgf_ry_pi2 q0 { }  // opaque: ry_pi2 (1q), golden in registry/modules/ry_pi2.sealed.json

h q[0];
cx q[0], q[1];
// UNMAPPED ry_pi2 [2]  (QASM3 비표준 — opaque)
qpgf_ry_pi2 q[2];
cx q[2], q[1];
