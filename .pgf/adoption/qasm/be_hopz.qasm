OPENQASM 3.0;
include "stdgates.inc";
qubit[4] q;

gate qpgf_sdg_gate q0 { }  // opaque: sdg_gate (1q), golden in registry/modules/sdg_gate.sealed.json

h q[0];
// UNMAPPED sdg_gate [1]  (QASM3 비표준 — opaque)
qpgf_sdg_gate q[1];
// UNMAPPED sdg_gate [3]  (QASM3 비표준 — opaque)
qpgf_sdg_gate q[3];
cx q[0], q[1];
cz q[0], q[2];
cx q[0], q[3];
s q[1];
s q[3];
x q[0];
cx q[0], q[1];
cz q[0], q[2];
cx q[0], q[3];
x q[0];
h q[0];
