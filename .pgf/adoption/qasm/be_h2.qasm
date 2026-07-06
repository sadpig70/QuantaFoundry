OPENQASM 3.0;
include "stdgates.inc";
qubit[4] q;

gate qpgf_ccz q0, q1, q2 { }  // opaque: ccz (3q), golden in registry/modules/ccz.sealed.json
gate qpgf_sdg_gate q0 { }  // opaque: sdg_gate (1q), golden in registry/modules/sdg_gate.sealed.json

h q[0];
h q[1];
x q[0];
x q[1];
cz q[0], q[1];
x q[0];
x q[1];
x q[0];
// UNMAPPED ccz [0, 1, 2]  (QASM3 비표준 — opaque)
qpgf_ccz q[0], q[1], q[2];
// UNMAPPED ccz [0, 1, 3]  (QASM3 비표준 — opaque)
qpgf_ccz q[0], q[1], q[3];
x q[0];
x q[1];
ccx q[0], q[1], q[2];
ccx q[0], q[1], q[3];
x q[1];
// UNMAPPED sdg_gate [2]  (QASM3 비표준 — opaque)
qpgf_sdg_gate q[2];
// UNMAPPED sdg_gate [3]  (QASM3 비표준 — opaque)
qpgf_sdg_gate q[3];
ccx q[0], q[1], q[2];
ccx q[0], q[1], q[3];
s q[2];
s q[3];
h q[0];
h q[1];
