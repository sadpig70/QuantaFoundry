OPENQASM 3.0;
include "stdgates.inc";
qubit[4] q;

gate qpgf_c3x q0, q1, q2, q3 { }  // opaque: c3x (4q), golden in registry/modules/c3x.sealed.json
gate qpgf_ry_cg_half q0 { }  // opaque: ry_cg_half (1q), golden in registry/modules/ry_cg_half.sealed.json
gate qpgf_ry_cg_half_dag q0 { }  // opaque: ry_cg_half_dag (1q), golden in registry/modules/ry_cg_half_dag.sealed.json
gate qpgf_ry_negpi4 q0 { }  // opaque: ry_negpi4 (1q), golden in registry/modules/ry_negpi4.sealed.json
gate qpgf_ry_negpi6 q0 { }  // opaque: ry_negpi6 (1q), golden in registry/modules/ry_negpi6.sealed.json
gate qpgf_ry_pi4 q0 { }  // opaque: ry_pi4 (1q), golden in registry/modules/ry_pi4.sealed.json
gate qpgf_ry_pi6 q0 { }  // opaque: ry_pi6 (1q), golden in registry/modules/ry_pi6.sealed.json

cx q[3], q[2];
x q[0];
x q[1];
// UNMAPPED c3x [0, 1, 2, 3]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[2], q[3];
// UNMAPPED ry_negpi6 [3]  (QASM3 비표준 — opaque)
qpgf_ry_negpi6 q[3];
// UNMAPPED c3x [0, 1, 2, 3]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[2], q[3];
// UNMAPPED ry_pi6 [3]  (QASM3 비표준 — opaque)
qpgf_ry_pi6 q[3];
x q[0];
x q[1];
cx q[3], q[2];
cx q[3], q[0];
x q[1];
// UNMAPPED c3x [0, 1, 2, 3]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[2], q[3];
// UNMAPPED ry_negpi4 [3]  (QASM3 비표준 — opaque)
qpgf_ry_negpi4 q[3];
// UNMAPPED c3x [0, 1, 2, 3]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[2], q[3];
// UNMAPPED ry_pi4 [3]  (QASM3 비표준 — opaque)
qpgf_ry_pi4 q[3];
x q[1];
cx q[3], q[0];
cx q[3], q[1];
// UNMAPPED c3x [0, 1, 2, 3]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[2], q[3];
// UNMAPPED ry_negpi6 [3]  (QASM3 비표준 — opaque)
qpgf_ry_negpi6 q[3];
// UNMAPPED ry_negpi6 [3]  (QASM3 비표준 — opaque)
qpgf_ry_negpi6 q[3];
// UNMAPPED c3x [0, 1, 2, 3]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[2], q[3];
// UNMAPPED ry_pi6 [3]  (QASM3 비표준 — opaque)
qpgf_ry_pi6 q[3];
// UNMAPPED ry_pi6 [3]  (QASM3 비표준 — opaque)
qpgf_ry_pi6 q[3];
cx q[3], q[1];
cx q[3], q[0];
cx q[3], q[1];
cx q[3], q[2];
x q[0];
// UNMAPPED c3x [0, 1, 2, 3]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[2], q[3];
// UNMAPPED ry_negpi4 [3]  (QASM3 비표준 — opaque)
qpgf_ry_negpi4 q[3];
// UNMAPPED c3x [0, 1, 2, 3]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[2], q[3];
// UNMAPPED ry_pi4 [3]  (QASM3 비표준 — opaque)
qpgf_ry_pi4 q[3];
x q[0];
cx q[3], q[2];
cx q[3], q[1];
cx q[3], q[0];
cx q[3], q[0];
x q[2];
// UNMAPPED c3x [0, 1, 2, 3]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[2], q[3];
// UNMAPPED ry_negpi4 [3]  (QASM3 비표준 — opaque)
qpgf_ry_negpi4 q[3];
// UNMAPPED c3x [0, 1, 2, 3]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[2], q[3];
// UNMAPPED ry_pi4 [3]  (QASM3 비표준 — opaque)
qpgf_ry_pi4 q[3];
x q[2];
cx q[3], q[0];
cx q[0], q[2];
x q[1];
ccx q[1], q[2], q[0];
// UNMAPPED ry_cg_half_dag [0]  (QASM3 비표준 — opaque)
qpgf_ry_cg_half_dag q[0];
ccx q[1], q[2], q[0];
// UNMAPPED ry_cg_half [0]  (QASM3 비표준 — opaque)
qpgf_ry_cg_half q[0];
x q[1];
cx q[0], q[2];
cx q[0], q[1];
ccx q[1], q[2], q[0];
// UNMAPPED ry_cg_half [0]  (QASM3 비표준 — opaque)
qpgf_ry_cg_half q[0];
ccx q[1], q[2], q[0];
// UNMAPPED ry_cg_half_dag [0]  (QASM3 비표준 — opaque)
qpgf_ry_cg_half_dag q[0];
cx q[0], q[1];
cx q[2], q[1];
x q[2];
// UNMAPPED ry_negpi4 [2]  (QASM3 비표준 — opaque)
qpgf_ry_negpi4 q[2];
cz q[1], q[2];
// UNMAPPED ry_pi4 [2]  (QASM3 비표준 — opaque)
qpgf_ry_pi4 q[2];
x q[2];
cx q[2], q[1];
