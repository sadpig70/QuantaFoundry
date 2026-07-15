OPENQASM 3.0;
include "stdgates.inc";
qubit[3] q;

gate qpgf_ry_negpi4 q0 { }  // opaque: ry_negpi4 (1q), golden in registry/modules/ry_negpi4.sealed.json
gate qpgf_ry_pi4 q0 { }  // opaque: ry_pi4 (1q), golden in registry/modules/ry_pi4.sealed.json

h q[2];
swap q[0], q[2];
swap q[1], q[2];
x q[0];
// UNMAPPED ry_negpi4 [1]  (QASM3 비표준 — opaque)
qpgf_ry_negpi4 q[1];
cz q[0], q[1];
// UNMAPPED ry_pi4 [1]  (QASM3 비표준 — opaque)
qpgf_ry_pi4 q[1];
// UNMAPPED ry_negpi4 [2]  (QASM3 비표준 — opaque)
qpgf_ry_negpi4 q[2];
cz q[0], q[2];
// UNMAPPED ry_pi4 [2]  (QASM3 비표준 — opaque)
qpgf_ry_pi4 q[2];
cswap q[0], q[1], q[2];
x q[0];
cp(1.57079632679) q[0], q[1];
ccx q[0], q[1], q[2];
cp(1.57079632679) q[0], q[2];
// UNMAPPED ry_negpi4 [2]  (QASM3 비표준 — opaque)
qpgf_ry_negpi4 q[2];
cz q[0], q[2];
// UNMAPPED ry_pi4 [2]  (QASM3 비표준 — opaque)
qpgf_ry_pi4 q[2];
ccx q[0], q[2], q[1];
