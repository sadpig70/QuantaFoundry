OPENQASM 3.0;
include "stdgates.inc";
qubit[2] q;

gate qpgf_ry_pi4 q0 { }  // opaque: ry_pi4 (1q), golden in registry/modules/ry_pi4.sealed.json

// UNMAPPED ry_pi4 [0]  (QASM3 비표준 — opaque)
qpgf_ry_pi4 q[0];
// UNMAPPED ry_pi4 [1]  (QASM3 비표준 — opaque)
qpgf_ry_pi4 q[1];
cx q[0], q[1];
