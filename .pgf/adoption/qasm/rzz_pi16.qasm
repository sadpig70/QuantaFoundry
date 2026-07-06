OPENQASM 3.0;
include "stdgates.inc";
qubit[2] q;

gate qpgf_rz_negpi8 q0 { }  // opaque: rz_negpi8 (1q), golden in registry/modules/rz_negpi8.sealed.json

cx q[0], q[1];
// UNMAPPED rz_negpi8 [1]  (QASM3 비표준 — opaque)
qpgf_rz_negpi8 q[1];
cx q[0], q[1];
