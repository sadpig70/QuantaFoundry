OPENQASM 3.0;
include "stdgates.inc";
qubit[2] q;

gate qpgf_ry_pi2 q0 { }  // opaque: ry_pi2 (1q), golden in registry/modules/ry_pi2.sealed.json

// UNMAPPED ry_pi2 [1]  (QASM3 비표준 — opaque)
qpgf_ry_pi2 q[1];
cx q[1], q[0];
