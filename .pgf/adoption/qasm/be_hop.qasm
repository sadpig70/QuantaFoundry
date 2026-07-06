OPENQASM 3.0;
include "stdgates.inc";
qubit[3] q;

gate qpgf_sdg_gate q0 { }  // opaque: sdg_gate (1q), golden in registry/modules/sdg_gate.sealed.json

h q[0];
// UNMAPPED sdg_gate [2]  (QASM3 비표준 — opaque)
qpgf_sdg_gate q[2];
// UNMAPPED sdg_gate [1]  (QASM3 비표준 — opaque)
qpgf_sdg_gate q[1];
cx q[0], q[1];
cx q[0], q[2];
s q[2];
s q[1];
x q[0];
cx q[0], q[1];
cx q[0], q[2];
x q[0];
h q[0];
