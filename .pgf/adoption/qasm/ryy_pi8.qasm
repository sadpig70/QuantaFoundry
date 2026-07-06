OPENQASM 3.0;
include "stdgates.inc";
qubit[2] q;

gate qpgf_rz_negpi4 q0 { }  // opaque: rz_negpi4 (1q), golden in registry/modules/rz_negpi4.sealed.json
gate qpgf_sdg_gate q0 { }  // opaque: sdg_gate (1q), golden in registry/modules/sdg_gate.sealed.json

// UNMAPPED sdg_gate [0]  (QASM3 비표준 — opaque)
qpgf_sdg_gate q[0];
// UNMAPPED sdg_gate [1]  (QASM3 비표준 — opaque)
qpgf_sdg_gate q[1];
h q[0];
h q[1];
cx q[0], q[1];
// UNMAPPED rz_negpi4 [1]  (QASM3 비표준 — opaque)
qpgf_rz_negpi4 q[1];
cx q[0], q[1];
h q[0];
h q[1];
s q[0];
s q[1];
