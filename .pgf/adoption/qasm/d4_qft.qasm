OPENQASM 3.0;
include "stdgates.inc";
qubit[3] q;

gate qpgf_qft2 q0, q1 { }  // opaque: qft2 (2q), golden in registry/modules/qft2.sealed.json
gate qpgf_ry_negpi4 q0 { }  // opaque: ry_negpi4 (1q), golden in registry/modules/ry_negpi4.sealed.json
gate qpgf_ry_pi4 q0 { }  // opaque: ry_pi4 (1q), golden in registry/modules/ry_pi4.sealed.json

// UNMAPPED qft2 [0, 1]  (QASM3 비표준 — opaque)
qpgf_qft2 q[0], q[1];
// UNMAPPED ry_negpi4 [2]  (QASM3 비표준 — opaque)
qpgf_ry_negpi4 q[2];
x q[1];
cz q[1], q[2];
x q[1];
// UNMAPPED ry_pi4 [2]  (QASM3 비표준 — opaque)
qpgf_ry_pi4 q[2];
