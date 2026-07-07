OPENQASM 3.0;
include "stdgates.inc";
qubit[3] q;

gate qpgf_iswap q0, q1 { }  // opaque: iswap (2q), golden in registry/modules/iswap.sealed.json
gate qpgf_sdg_gate q0 { }  // opaque: sdg_gate (1q), golden in registry/modules/sdg_gate.sealed.json

s q[0];
// UNMAPPED iswap [0, 1]  (QASM3 비표준 — opaque)
qpgf_iswap q[0], q[1];
t q[2];
// UNMAPPED iswap [1, 2]  (QASM3 비표준 — opaque)
qpgf_iswap q[1], q[2];
// UNMAPPED sdg_gate [1]  (QASM3 비표준 — opaque)
qpgf_sdg_gate q[1];
swap q[1], q[2];
cz q[1], q[2];
