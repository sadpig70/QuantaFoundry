OPENQASM 3.0;
include "stdgates.inc";
qubit[8] q;

gate qpgf_sdg_gate q0 { }  // opaque: sdg_gate (1q), golden in registry/modules/sdg_gate.sealed.json

t q[0];
t q[3];
t q[5];
t q[6];
t q[1];
// UNMAPPED sdg_gate [1]  (QASM3 비표준 — opaque)
qpgf_sdg_gate q[1];
t q[2];
// UNMAPPED sdg_gate [2]  (QASM3 비표준 — opaque)
qpgf_sdg_gate q[2];
t q[4];
// UNMAPPED sdg_gate [4]  (QASM3 비표준 — opaque)
qpgf_sdg_gate q[4];
t q[7];
// UNMAPPED sdg_gate [7]  (QASM3 비표준 — opaque)
qpgf_sdg_gate q[7];
