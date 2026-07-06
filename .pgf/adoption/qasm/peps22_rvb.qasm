OPENQASM 3.0;
include "stdgates.inc";
qubit[4] q;

gate qpgf_ry_negpi2 q0 { }  // opaque: ry_negpi2 (1q), golden in registry/modules/ry_negpi2.sealed.json
gate qpgf_ry_pi2 q0 { }  // opaque: ry_pi2 (1q), golden in registry/modules/ry_pi2.sealed.json

// UNMAPPED ry_pi2 [0]  (QASM3 비표준 — opaque)
qpgf_ry_pi2 q[0];
// UNMAPPED ry_pi2 [1]  (QASM3 비표준 — opaque)
qpgf_ry_pi2 q[1];
cx q[0], q[1];
ry(1.15026199151) q[1];
ry(1.15026199151) q[1];
// UNMAPPED ry_negpi2 [1]  (QASM3 비표준 — opaque)
qpgf_ry_negpi2 q[1];
cx q[0], q[1];
x q[0];
x q[1];
ccx q[0], q[1], q[2];
x q[0];
x q[1];
x q[0];
ry(1.10714871779) q[2];
ccx q[0], q[1], q[2];
ry(-1.10714871779) q[2];
ccx q[0], q[1], q[2];
x q[0];
x q[1];
// UNMAPPED ry_pi2 [2]  (QASM3 비표준 — opaque)
qpgf_ry_pi2 q[2];
ry(-1.10714871779) q[2];
ccx q[0], q[1], q[2];
ry(1.10714871779) q[2];
// UNMAPPED ry_negpi2 [2]  (QASM3 비표준 — opaque)
qpgf_ry_negpi2 q[2];
ccx q[0], q[1], q[2];
x q[1];
cx q[0], q[3];
cx q[1], q[3];
cx q[2], q[3];
z q[0];
cz q[0], q[1];
cz q[0], q[2];
cz q[1], q[2];
