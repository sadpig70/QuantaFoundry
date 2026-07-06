OPENQASM 3.0;
include "stdgates.inc";
qubit[2] q;

gate qpgf_ry_negpi6 q0 { }  // opaque: ry_negpi6 (1q), golden in registry/modules/ry_negpi6.sealed.json
gate qpgf_ry_pi6 q0 { }  // opaque: ry_pi6 (1q), golden in registry/modules/ry_pi6.sealed.json

cx q[0], q[1];
// UNMAPPED ry_negpi6 [1]  (QASM3 비표준 — opaque)
qpgf_ry_negpi6 q[1];
cx q[0], q[1];
// UNMAPPED ry_pi6 [1]  (QASM3 비표준 — opaque)
qpgf_ry_pi6 q[1];
