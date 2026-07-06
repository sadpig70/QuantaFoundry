OPENQASM 3.0;
include "stdgates.inc";
qubit[2] q;

gate qpgf_sdg_gate q0 { }  // opaque: sdg_gate (1q), golden in registry/modules/sdg_gate.sealed.json

// UNMAPPED sdg_gate [0]  (QASM3 비표준 — opaque)
qpgf_sdg_gate q[0];
h q[0];
// UNMAPPED sdg_gate [1]  (QASM3 비표준 — opaque)
qpgf_sdg_gate q[1];
h q[1];
