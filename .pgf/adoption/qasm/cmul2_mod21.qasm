OPENQASM 3.0;
include "stdgates.inc";
qubit[6] q;

gate qpgf_c3x q0, q1, q2, q3 { }  // opaque: c3x (4q), golden in registry/modules/c3x.sealed.json
gate qpgf_c4x q0, q1, q2, q3, q4 { }  // opaque: c4x (5q), golden in registry/modules/c4x.sealed.json
gate qpgf_c5x q0, q1, q2, q3, q4, q5 { }  // opaque: c5x (6q), golden in registry/modules/c5x.sealed.json

ccx q[5], q[0], q[4];
ccx q[5], q[0], q[2];
ccx q[4], q[0], q[5];
ccx q[4], q[0], q[2];
// UNMAPPED c3x [3, 2, 0, 5]  (QASM3 비표준 — opaque)
qpgf_c3x q[3], q[2], q[0], q[5];
// UNMAPPED c4x [5, 3, 2, 0, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[5], q[3], q[2], q[0], q[4];
// UNMAPPED c3x [5, 4, 0, 3]  (QASM3 비표준 — opaque)
qpgf_c3x q[5], q[4], q[0], q[3];
// UNMAPPED c3x [5, 4, 0, 2]  (QASM3 비표준 — opaque)
qpgf_c3x q[5], q[4], q[0], q[2];
ccx q[3], q[0], q[5];
ccx q[3], q[0], q[4];
// UNMAPPED c4x [4, 3, 2, 0, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[4], q[3], q[2], q[0], q[5];
// UNMAPPED c3x [5, 3, 0, 4]  (QASM3 비표준 — opaque)
qpgf_c3x q[5], q[3], q[0], q[4];
// UNMAPPED c3x [5, 3, 0, 2]  (QASM3 비표준 — opaque)
qpgf_c3x q[5], q[3], q[0], q[2];
// UNMAPPED c3x [5, 2, 0, 4]  (QASM3 비표준 — opaque)
qpgf_c3x q[5], q[2], q[0], q[4];
// UNMAPPED c4x [5, 4, 2, 0, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[5], q[4], q[2], q[0], q[3];
// UNMAPPED c3x [4, 3, 0, 5]  (QASM3 비표준 — opaque)
qpgf_c3x q[4], q[3], q[0], q[5];
// UNMAPPED c3x [4, 3, 0, 2]  (QASM3 비표준 — opaque)
qpgf_c3x q[4], q[3], q[0], q[2];
// UNMAPPED c3x [5, 2, 0, 4]  (QASM3 비표준 — opaque)
qpgf_c3x q[5], q[2], q[0], q[4];
// UNMAPPED c4x [5, 4, 2, 0, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[5], q[4], q[2], q[0], q[3];
// UNMAPPED c4x [5, 4, 3, 0, 2]  (QASM3 비표준 — opaque)
qpgf_c4x q[5], q[4], q[3], q[0], q[2];
ccx q[2], q[0], q[5];
// UNMAPPED c3x [3, 2, 0, 5]  (QASM3 비표준 — opaque)
qpgf_c3x q[3], q[2], q[0], q[5];
// UNMAPPED c3x [5, 2, 0, 3]  (QASM3 비표준 — opaque)
qpgf_c3x q[5], q[2], q[0], q[3];
ccx q[1], q[0], q[5];
// UNMAPPED c3x [5, 1, 0, 4]  (QASM3 비표준 — opaque)
qpgf_c3x q[5], q[1], q[0], q[4];
// UNMAPPED c4x [5, 4, 1, 0, 2]  (QASM3 비표준 — opaque)
qpgf_c4x q[5], q[4], q[1], q[0], q[2];
// UNMAPPED c4x [5, 4, 2, 0, 1]  (QASM3 비표준 — opaque)
qpgf_c4x q[5], q[4], q[2], q[0], q[1];
// UNMAPPED c3x [3, 2, 0, 4]  (QASM3 비표준 — opaque)
qpgf_c3x q[3], q[2], q[0], q[4];
// UNMAPPED c3x [5, 1, 0, 3]  (QASM3 비표준 — opaque)
qpgf_c3x q[5], q[1], q[0], q[3];
// UNMAPPED c4x [5, 3, 1, 0, 2]  (QASM3 비표준 — opaque)
qpgf_c4x q[5], q[3], q[1], q[0], q[2];
// UNMAPPED c4x [5, 3, 2, 0, 1]  (QASM3 비표준 — opaque)
qpgf_c4x q[5], q[3], q[2], q[0], q[1];
// UNMAPPED c5x [5, 4, 3, 1, 0, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[5], q[4], q[3], q[1], q[0], q[2];
// UNMAPPED c4x [4, 3, 2, 0, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[4], q[3], q[2], q[0], q[5];
// UNMAPPED c4x [4, 3, 2, 0, 1]  (QASM3 비표준 — opaque)
qpgf_c4x q[4], q[3], q[2], q[0], q[1];
// UNMAPPED c5x [5, 3, 2, 1, 0, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[5], q[3], q[2], q[1], q[0], q[4];
// UNMAPPED c5x [5, 4, 3, 2, 0, 1]  (QASM3 비표준 — opaque)
qpgf_c5x q[5], q[4], q[3], q[2], q[0], q[1];
ccx q[1], q[0], q[5];
ccx q[1], q[0], q[4];
ccx q[1], q[0], q[3];
// UNMAPPED c4x [4, 3, 1, 0, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[4], q[3], q[1], q[0], q[5];
// UNMAPPED c3x [5, 1, 0, 4]  (QASM3 비표준 — opaque)
qpgf_c3x q[5], q[1], q[0], q[4];
// UNMAPPED c3x [5, 1, 0, 3]  (QASM3 비표준 — opaque)
qpgf_c3x q[5], q[1], q[0], q[3];
// UNMAPPED c4x [5, 2, 1, 0, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[5], q[2], q[1], q[0], q[4];
// UNMAPPED c3x [4, 1, 0, 5]  (QASM3 비표준 — opaque)
qpgf_c3x q[4], q[1], q[0], q[5];
// UNMAPPED c3x [4, 1, 0, 2]  (QASM3 비표준 — opaque)
qpgf_c3x q[4], q[1], q[0], q[2];
// UNMAPPED c5x [5, 3, 2, 1, 0, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[5], q[3], q[2], q[1], q[0], q[4];
// UNMAPPED c4x [5, 4, 1, 0, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[5], q[4], q[1], q[0], q[3];
// UNMAPPED c4x [5, 4, 1, 0, 2]  (QASM3 비표준 — opaque)
qpgf_c4x q[5], q[4], q[1], q[0], q[2];
// UNMAPPED c3x [3, 1, 0, 5]  (QASM3 비표준 — opaque)
qpgf_c3x q[3], q[1], q[0], q[5];
// UNMAPPED c3x [3, 1, 0, 4]  (QASM3 비표준 — opaque)
qpgf_c3x q[3], q[1], q[0], q[4];
// UNMAPPED c3x [3, 1, 0, 2]  (QASM3 비표준 — opaque)
qpgf_c3x q[3], q[1], q[0], q[2];
// UNMAPPED c4x [3, 2, 1, 0, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[3], q[2], q[1], q[0], q[5];
// UNMAPPED c4x [5, 3, 1, 0, 2]  (QASM3 비표준 — opaque)
qpgf_c4x q[5], q[3], q[1], q[0], q[2];
// UNMAPPED c4x [4, 3, 1, 0, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[4], q[3], q[1], q[0], q[5];
// UNMAPPED c4x [4, 3, 1, 0, 2]  (QASM3 비표준 — opaque)
qpgf_c4x q[4], q[3], q[1], q[0], q[2];
// UNMAPPED c4x [5, 2, 1, 0, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[5], q[2], q[1], q[0], q[4];
// UNMAPPED c5x [5, 4, 2, 1, 0, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[5], q[4], q[2], q[1], q[0], q[3];
// UNMAPPED c5x [5, 4, 3, 1, 0, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[5], q[4], q[3], q[1], q[0], q[2];
// UNMAPPED c4x [3, 2, 1, 0, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[3], q[2], q[1], q[0], q[5];
// UNMAPPED c4x [5, 2, 1, 0, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[5], q[2], q[1], q[0], q[3];
// UNMAPPED c4x [4, 2, 1, 0, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[4], q[2], q[1], q[0], q[3];
// UNMAPPED c4x [3, 2, 1, 0, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[3], q[2], q[1], q[0], q[5];
// UNMAPPED c5x [5, 3, 2, 1, 0, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[5], q[3], q[2], q[1], q[0], q[4];
// UNMAPPED c5x [5, 4, 2, 1, 0, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[5], q[4], q[2], q[1], q[0], q[3];
// UNMAPPED c4x [3, 2, 1, 0, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[3], q[2], q[1], q[0], q[5];
// UNMAPPED c5x [5, 3, 2, 1, 0, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[5], q[3], q[2], q[1], q[0], q[4];
