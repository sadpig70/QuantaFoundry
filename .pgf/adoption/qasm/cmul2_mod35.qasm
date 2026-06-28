OPENQASM 3.0;
include "stdgates.inc";
qubit[7] q;

gate qpgf_c3x q0, q1, q2, q3 { }  // opaque: c3x (4q), golden in registry/modules/c3x.sealed.json
gate qpgf_c4x q0, q1, q2, q3, q4 { }  // opaque: c4x (5q), golden in registry/modules/c4x.sealed.json
gate qpgf_c5x q0, q1, q2, q3, q4, q5 { }  // opaque: c5x (6q), golden in registry/modules/c5x.sealed.json
gate qpgf_c6x q0, q1, q2, q3, q4, q5, q6 { }  // opaque: c6x (7q), golden in registry/modules/c6x.sealed.json

// UNMAPPED c6x [0, 1, 2, 3, 4, 5, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[5], q[6];
// UNMAPPED c5x [0, 1, 2, 3, 4, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[4], q[6];
// UNMAPPED c6x [0, 1, 2, 3, 5, 6, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[6], q[4];
// UNMAPPED c6x [0, 1, 2, 3, 4, 5, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[5], q[6];
// UNMAPPED c5x [0, 1, 2, 3, 5, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[5], q[4];
// UNMAPPED c4x [0, 1, 2, 3, 6]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[3], q[6];
// UNMAPPED c6x [0, 1, 2, 4, 5, 6, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[5], q[6], q[3];
// UNMAPPED c6x [0, 1, 2, 3, 5, 6, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[6], q[4];
// UNMAPPED c5x [0, 1, 2, 4, 5, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[4], q[5], q[6];
// UNMAPPED c5x [0, 1, 2, 4, 6, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[4], q[6], q[5];
// UNMAPPED c5x [0, 1, 2, 4, 6, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[4], q[6], q[3];
// UNMAPPED c6x [0, 1, 2, 3, 5, 6, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[6], q[4];
// UNMAPPED c4x [0, 1, 2, 4, 6]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[4], q[6];
// UNMAPPED c5x [0, 1, 2, 5, 6, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[5], q[6], q[4];
// UNMAPPED c5x [0, 1, 2, 4, 6, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[4], q[6], q[5];
// UNMAPPED c4x [0, 1, 2, 5, 6]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[5], q[6];
// UNMAPPED c4x [0, 1, 2, 5, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[5], q[3];
// UNMAPPED c4x [0, 1, 2, 6, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[6], q[5];
// UNMAPPED c4x [0, 1, 2, 6, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[6], q[3];
// UNMAPPED c3x [0, 1, 2, 6]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[2], q[6];
// UNMAPPED c3x [0, 1, 2, 4]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[2], q[4];
// UNMAPPED c5x [0, 1, 3, 4, 5, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[4], q[5], q[6];
// UNMAPPED c5x [0, 1, 3, 4, 5, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[4], q[5], q[2];
// UNMAPPED c6x [0, 1, 2, 3, 4, 6, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[6], q[5];
// UNMAPPED c5x [0, 1, 3, 4, 6, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[4], q[6], q[2];
// UNMAPPED c5x [0, 1, 2, 3, 6, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[6], q[4];
// UNMAPPED c4x [0, 1, 3, 4, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[3], q[4], q[5];
// UNMAPPED c4x [0, 1, 3, 4, 2]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[3], q[4], q[2];
// UNMAPPED c5x [0, 1, 2, 3, 5, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[5], q[4];
// UNMAPPED c4x [0, 1, 2, 5, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[5], q[3];
// UNMAPPED c4x [0, 1, 3, 6, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[3], q[6], q[4];
// UNMAPPED c4x [0, 1, 3, 6, 2]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[3], q[6], q[2];
// UNMAPPED c5x [0, 1, 2, 3, 4, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[4], q[6];
// UNMAPPED c4x [0, 1, 2, 4, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[4], q[3];
// UNMAPPED c3x [0, 1, 3, 6]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[3], q[6];
// UNMAPPED c3x [0, 1, 3, 4]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[3], q[4];
// UNMAPPED c3x [0, 1, 3, 2]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[3], q[2];
// UNMAPPED c5x [0, 1, 2, 4, 6, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[4], q[6], q[3];
// UNMAPPED c4x [0, 1, 4, 5, 6]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[4], q[5], q[6];
// UNMAPPED c4x [0, 1, 4, 5, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[4], q[5], q[3];
// UNMAPPED c4x [0, 1, 4, 6, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[4], q[6], q[5];
// UNMAPPED c4x [0, 1, 4, 6, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[4], q[6], q[3];
// UNMAPPED c5x [0, 1, 3, 4, 5, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[4], q[5], q[6];
// UNMAPPED c3x [0, 1, 4, 5]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[4], q[5];
// UNMAPPED c3x [0, 1, 4, 2]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[4], q[2];
// UNMAPPED c4x [0, 1, 2, 5, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[5], q[4];
// UNMAPPED c3x [0, 1, 5, 4]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[5], q[4];
// UNMAPPED c3x [0, 1, 5, 3]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[5], q[3];
// UNMAPPED c3x [0, 1, 5, 2]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[5], q[2];
ccx q[0], q[1], q[6];
ccx q[0], q[1], q[2];
// UNMAPPED c5x [0, 2, 3, 4, 5, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[4], q[5], q[6];
// UNMAPPED c5x [0, 2, 3, 4, 5, 1]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[4], q[5], q[1];
// UNMAPPED c4x [0, 2, 3, 4, 6]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[3], q[4], q[6];
// UNMAPPED c4x [0, 2, 3, 4, 1]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[3], q[4], q[1];
// UNMAPPED c4x [0, 2, 3, 5, 6]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[3], q[5], q[6];
// UNMAPPED c4x [0, 2, 3, 5, 1]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[3], q[5], q[1];
// UNMAPPED c3x [0, 2, 3, 6]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[2], q[3], q[6];
// UNMAPPED c3x [0, 2, 3, 1]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[2], q[3], q[1];
// UNMAPPED c4x [0, 2, 4, 5, 6]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[4], q[5], q[6];
// UNMAPPED c4x [0, 2, 4, 5, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[4], q[5], q[3];
// UNMAPPED c4x [0, 2, 4, 5, 1]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[4], q[5], q[1];
// UNMAPPED c3x [0, 2, 4, 6]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[2], q[4], q[6];
// UNMAPPED c3x [0, 2, 4, 3]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[2], q[4], q[3];
// UNMAPPED c3x [0, 2, 4, 1]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[2], q[4], q[1];
// UNMAPPED c3x [0, 2, 5, 6]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[2], q[5], q[6];
// UNMAPPED c3x [0, 2, 5, 4]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[2], q[5], q[4];
// UNMAPPED c3x [0, 2, 5, 3]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[2], q[5], q[3];
// UNMAPPED c3x [0, 2, 5, 1]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[2], q[5], q[1];
ccx q[0], q[2], q[1];
ccx q[0], q[1], q[2];
ccx q[0], q[3], q[2];
ccx q[0], q[2], q[3];
ccx q[0], q[4], q[3];
ccx q[0], q[3], q[4];
ccx q[0], q[5], q[4];
ccx q[0], q[4], q[5];
ccx q[0], q[6], q[5];
ccx q[0], q[5], q[6];
