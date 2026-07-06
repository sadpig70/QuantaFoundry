OPENQASM 3.0;
include "stdgates.inc";
qubit[2] q;

gate qpgf_ry_negpi2 q0 { }  // opaque: ry_negpi2 (1q), golden in registry/modules/ry_negpi2.sealed.json
gate qpgf_ry_pi2 q0 { }  // opaque: ry_pi2 (1q), golden in registry/modules/ry_pi2.sealed.json

cx q[0], q[1];
// UNMAPPED ry_negpi2 [1]  (QASM3 비표준 — opaque)
qpgf_ry_negpi2 q[1];
cx q[0], q[1];
// UNMAPPED ry_pi2 [1]  (QASM3 비표준 — opaque)
qpgf_ry_pi2 q[1];
