OPENQASM 3.0;
include "stdgates.inc";
qubit[2] q;

gate qpgf_rz_y4_p q0 { }  // opaque: rz_y4_p (1q), golden in registry/modules/rz_y4_p.sealed.json

cx q[0], q[1];
// UNMAPPED rz_y4_p [1]  (QASM3 비표준 — opaque)
qpgf_rz_y4_p q[1];
cx q[0], q[1];
