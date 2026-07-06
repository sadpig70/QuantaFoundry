OPENQASM 3.0;
include "stdgates.inc";
qubit[2] q;

gate qpgf_rz_y4_q q0 { }  // opaque: rz_y4_q (1q), golden in registry/modules/rz_y4_q.sealed.json

cx q[0], q[1];
// UNMAPPED rz_y4_q [1]  (QASM3 비표준 — opaque)
qpgf_rz_y4_q q[1];
cx q[0], q[1];
