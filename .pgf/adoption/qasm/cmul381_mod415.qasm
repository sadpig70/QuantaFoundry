OPENQASM 3.0;
include "stdgates.inc";
qubit[10] q;

gate qpgf_c3x q0, q1, q2, q3 { }  // opaque: c3x (4q), golden in registry/modules/c3x.sealed.json
gate qpgf_c4x q0, q1, q2, q3, q4 { }  // opaque: c4x (5q), golden in registry/modules/c4x.sealed.json
gate qpgf_c5x q0, q1, q2, q3, q4, q5 { }  // opaque: c5x (6q), golden in registry/modules/c5x.sealed.json
gate qpgf_c6x q0, q1, q2, q3, q4, q5, q6 { }  // opaque: c6x (7q), golden in registry/modules/c6x.sealed.json
gate qpgf_c7x q0, q1, q2, q3, q4, q5, q6, q7 { }  // opaque: c7x (8q), golden in registry/modules/c7x.sealed.json
gate qpgf_c8x q0, q1, q2, q3, q4, q5, q6, q7, q8 { }  // opaque: c8x (9q), golden in registry/modules/c8x.sealed.json
gate qpgf_c9x q0, q1, q2, q3, q4, q5, q6, q7, q8, q9 { }  // opaque: c9x (10q), golden in registry/modules/c9x.sealed.json

// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[7];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[7];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[7];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 6, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[6];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 7, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[6];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[7];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[9], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 7, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[6];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[9], q[7];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[9], q[6];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[6];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[9], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[9], q[6];
// UNMAPPED c6x [0, 1, 2, 3, 4, 5, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[5], q[9];
// UNMAPPED c6x [0, 1, 2, 3, 4, 5, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[5], q[6];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 7, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[5];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 7, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[5];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 6, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[9], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 7, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[9], q[5];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[6];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 7, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[5];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[6];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[9], q[5];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8];
// UNMAPPED c6x [0, 1, 2, 3, 4, 5, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[5], q[6];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[7];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[9], q[7];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[9], q[5];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9];
// UNMAPPED c6x [0, 1, 2, 3, 4, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[6], q[8];
// UNMAPPED c6x [0, 1, 2, 3, 4, 6, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[6], q[5];
// UNMAPPED c8x [0, 1, 2, 3, 4, 7, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[9], q[6];
// UNMAPPED c8x [0, 1, 2, 3, 4, 7, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[9], q[5];
// UNMAPPED c7x [0, 1, 2, 3, 4, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 4, 7, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[6];
// UNMAPPED c7x [0, 1, 2, 3, 4, 7, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[5];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[7];
// UNMAPPED c7x [0, 1, 2, 3, 4, 7, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[7], q[9], q[6];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[9];
// UNMAPPED c6x [0, 1, 2, 3, 4, 6, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[6], q[7];
// UNMAPPED c6x [0, 1, 2, 3, 4, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[7], q[9];
// UNMAPPED c6x [0, 1, 2, 3, 4, 7, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[7], q[6];
// UNMAPPED c7x [0, 1, 2, 3, 4, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[8], q[9], q[7];
// UNMAPPED c7x [0, 1, 2, 3, 4, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[8], q[9], q[6];
// UNMAPPED c7x [0, 1, 2, 3, 4, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[8], q[9], q[5];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8];
// UNMAPPED c6x [0, 1, 2, 3, 4, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[8], q[7];
// UNMAPPED c6x [0, 1, 2, 3, 4, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[8], q[5];
// UNMAPPED c6x [0, 1, 2, 3, 4, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[9], q[7];
// UNMAPPED c5x [0, 1, 2, 3, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[4], q[9];
// UNMAPPED c5x [0, 1, 2, 3, 4, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[4], q[7];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 7, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[9], q[4];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[7];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[6];
// UNMAPPED c6x [0, 1, 2, 3, 4, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[8], q[5];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 7, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[4];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[7];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[6];
// UNMAPPED c6x [0, 1, 2, 3, 4, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[8], q[5];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[9], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 7, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[9], q[4];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[7];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[9], q[5];
// UNMAPPED c7x [0, 1, 2, 3, 5, 6, 7, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[4];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 7, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[5];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[9], q[7];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[9], q[4];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 7, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[9], q[5];
// UNMAPPED c7x [0, 1, 2, 3, 5, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[7];
// UNMAPPED c7x [0, 1, 2, 3, 5, 6, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[4];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 7, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[5];
// UNMAPPED c7x [0, 1, 2, 3, 5, 6, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[6], q[9], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 5, 6, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[6], q[9], q[7];
// UNMAPPED c7x [0, 1, 2, 3, 5, 6, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[6], q[9], q[4];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 7, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[5];
// UNMAPPED c8x [0, 1, 2, 3, 5, 7, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[9], q[4];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[9], q[7];
// UNMAPPED c7x [0, 1, 2, 3, 5, 7, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[6];
// UNMAPPED c7x [0, 1, 2, 3, 5, 7, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[4];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 7, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[5];
// UNMAPPED c7x [0, 1, 2, 3, 5, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[7], q[9], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 5, 7, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[7], q[9], q[6];
// UNMAPPED c7x [0, 1, 2, 3, 5, 7, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[7], q[9], q[4];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[7];
// UNMAPPED c6x [0, 1, 2, 3, 5, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[7], q[9];
// UNMAPPED c6x [0, 1, 2, 3, 5, 7, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[7], q[6];
// UNMAPPED c6x [0, 1, 2, 3, 5, 7, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[7], q[4];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 7, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[9], q[5];
// UNMAPPED c7x [0, 1, 2, 3, 5, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[8], q[9], q[7];
// UNMAPPED c7x [0, 1, 2, 3, 5, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[8], q[9], q[6];
// UNMAPPED c7x [0, 1, 2, 3, 5, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[8], q[9], q[4];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 7, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[5];
// UNMAPPED c6x [0, 1, 2, 3, 5, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[8], q[7];
// UNMAPPED c6x [0, 1, 2, 3, 5, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[8], q[4];
// UNMAPPED c6x [0, 1, 2, 3, 5, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[9], q[6];
// UNMAPPED c6x [0, 1, 2, 3, 5, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[9], q[4];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 6, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9];
// UNMAPPED c5x [0, 1, 2, 3, 5, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[5], q[6];
// UNMAPPED c5x [0, 1, 2, 3, 5, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[5], q[4];
// UNMAPPED c8x [0, 1, 2, 3, 6, 7, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[6], q[7], q[8], q[9], q[5];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 5, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 6, 7, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[6], q[7], q[9], q[4];
// UNMAPPED c7x [0, 1, 2, 3, 4, 7, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[7], q[9], q[6];
// UNMAPPED c6x [0, 1, 2, 3, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[6], q[7], q[8];
// UNMAPPED c6x [0, 1, 2, 3, 6, 7, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[6], q[7], q[5];
// UNMAPPED c7x [0, 1, 2, 3, 5, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[7];
// UNMAPPED c6x [0, 1, 2, 3, 5, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[8], q[6];
// UNMAPPED c7x [0, 1, 2, 3, 6, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[6], q[8], q[9], q[7];
// UNMAPPED c7x [0, 1, 2, 3, 6, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[6], q[8], q[9], q[5];
// UNMAPPED c7x [0, 1, 2, 3, 6, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[6], q[8], q[9], q[4];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8];
// UNMAPPED c6x [0, 1, 2, 3, 6, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[6], q[8], q[9];
// UNMAPPED c6x [0, 1, 2, 3, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[6], q[8], q[7];
// UNMAPPED c6x [0, 1, 2, 3, 6, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[6], q[8], q[4];
// UNMAPPED c6x [0, 1, 2, 3, 6, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[6], q[9], q[5];
// UNMAPPED c6x [0, 1, 2, 3, 5, 6, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[6], q[9];
// UNMAPPED c5x [0, 1, 2, 3, 6, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[6], q[9];
// UNMAPPED c5x [0, 1, 2, 3, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[6], q[8];
// UNMAPPED c5x [0, 1, 2, 3, 6, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[6], q[7];
// UNMAPPED c7x [0, 1, 2, 3, 7, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[7], q[8], q[9], q[5];
// UNMAPPED c7x [0, 1, 2, 3, 7, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[7], q[8], q[9], q[4];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8];
// UNMAPPED c6x [0, 1, 2, 3, 7, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[7], q[8], q[4];
// UNMAPPED c6x [0, 1, 2, 3, 4, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[7], q[8];
// UNMAPPED c6x [0, 1, 2, 3, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[7], q[9], q[8];
// UNMAPPED c6x [0, 1, 2, 3, 7, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[7], q[9], q[6];
// UNMAPPED c6x [0, 1, 2, 3, 7, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[7], q[9], q[5];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 5, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[7];
// UNMAPPED c5x [0, 1, 2, 3, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[7], q[9];
// UNMAPPED c5x [0, 1, 2, 3, 7, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[7], q[6];
// UNMAPPED c5x [0, 1, 2, 3, 7, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[7], q[5];
// UNMAPPED c6x [0, 1, 2, 3, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[8], q[9], q[4];
// UNMAPPED c6x [0, 1, 2, 3, 4, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[8], q[9];
// UNMAPPED c5x [0, 1, 2, 3, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[4], q[8];
// UNMAPPED c5x [0, 1, 2, 3, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[8], q[6];
// UNMAPPED c5x [0, 1, 2, 3, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[6], q[8];
// UNMAPPED c5x [0, 1, 2, 3, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[9], q[8];
// UNMAPPED c5x [0, 1, 2, 3, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[9], q[7];
// UNMAPPED c5x [0, 1, 2, 3, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[9], q[6];
// UNMAPPED c7x [0, 1, 2, 3, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[6], q[7], q[8], q[9];
// UNMAPPED c4x [0, 1, 2, 3, 6]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[3], q[6];
// UNMAPPED c9x [0, 1, 2, 4, 5, 6, 7, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[4], q[5], q[6], q[7], q[8], q[9], q[3];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8];
// UNMAPPED c8x [0, 1, 2, 4, 5, 6, 7, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[4], q[5], q[6], q[7], q[8], q[3];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 7, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[4];
// UNMAPPED c8x [0, 1, 2, 4, 5, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[4], q[5], q[6], q[7], q[9], q[8];
// UNMAPPED c8x [0, 1, 2, 4, 5, 6, 7, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[4], q[5], q[6], q[7], q[9], q[3];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 7, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[9], q[4];
// UNMAPPED c7x [0, 1, 2, 4, 5, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[4], q[5], q[6], q[7], q[8];
// UNMAPPED c7x [0, 1, 2, 4, 5, 6, 7, 3]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[4], q[5], q[6], q[7], q[3];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[7];
// UNMAPPED c7x [0, 1, 2, 3, 5, 6, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[4];
// UNMAPPED c8x [0, 1, 2, 4, 5, 6, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[4], q[5], q[6], q[8], q[9], q[7];
// UNMAPPED c8x [0, 1, 2, 4, 5, 6, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[4], q[5], q[6], q[8], q[9], q[3];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 7, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[6];
// UNMAPPED c6x [0, 1, 2, 3, 4, 7, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[7], q[5];
// UNMAPPED c7x [0, 1, 2, 4, 5, 6, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[4], q[5], q[6], q[8], q[3];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8];
// UNMAPPED c6x [0, 1, 2, 3, 4, 6, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[6], q[5];
// UNMAPPED c7x [0, 1, 2, 4, 5, 6, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[4], q[5], q[6], q[9], q[8];
// UNMAPPED c7x [0, 1, 2, 4, 5, 6, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[4], q[5], q[6], q[9], q[3];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[6];
// UNMAPPED c6x [0, 1, 2, 3, 5, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[8], q[4];
// UNMAPPED c6x [0, 1, 2, 4, 5, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[5], q[6], q[8];
// UNMAPPED c6x [0, 1, 2, 4, 5, 6, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[5], q[6], q[3];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[6];
// UNMAPPED c6x [0, 1, 2, 3, 5, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[8], q[4];
// UNMAPPED c8x [0, 1, 2, 4, 5, 7, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[4], q[5], q[7], q[8], q[9], q[6];
// UNMAPPED c8x [0, 1, 2, 4, 5, 7, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[4], q[5], q[7], q[8], q[9], q[3];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[7];
// UNMAPPED c7x [0, 1, 2, 3, 5, 6, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[4];
// UNMAPPED c7x [0, 1, 2, 4, 5, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[4], q[5], q[7], q[8], q[9];
// UNMAPPED c7x [0, 1, 2, 4, 5, 7, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[4], q[5], q[7], q[8], q[6];
// UNMAPPED c7x [0, 1, 2, 4, 5, 7, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[4], q[5], q[7], q[8], q[3];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[7];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[9], q[5];
// UNMAPPED c6x [0, 1, 2, 3, 6, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[6], q[9], q[4];
// UNMAPPED c7x [0, 1, 2, 4, 5, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[4], q[5], q[7], q[9], q[8];
// UNMAPPED c7x [0, 1, 2, 4, 5, 7, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[4], q[5], q[7], q[9], q[6];
// UNMAPPED c7x [0, 1, 2, 4, 5, 7, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[4], q[5], q[7], q[9], q[3];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[7];
// UNMAPPED c7x [0, 1, 2, 3, 5, 6, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[4];
// UNMAPPED c6x [0, 1, 2, 4, 5, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[5], q[7], q[9];
// UNMAPPED c6x [0, 1, 2, 4, 5, 7, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[5], q[7], q[3];
// UNMAPPED c7x [0, 1, 2, 4, 5, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[4], q[5], q[8], q[9], q[7];
// UNMAPPED c7x [0, 1, 2, 4, 5, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[4], q[5], q[8], q[9], q[6];
// UNMAPPED c8x [0, 1, 2, 4, 5, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[4], q[5], q[6], q[7], q[9], q[8];
// UNMAPPED c6x [0, 1, 2, 4, 5, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[5], q[8], q[7];
// UNMAPPED c6x [0, 1, 2, 4, 5, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[5], q[8], q[6];
// UNMAPPED c6x [0, 1, 2, 4, 5, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[5], q[8], q[3];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 7, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[4];
// UNMAPPED c6x [0, 1, 2, 4, 5, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[5], q[9], q[8];
// UNMAPPED c6x [0, 1, 2, 4, 5, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[5], q[9], q[7];
// UNMAPPED c6x [0, 1, 2, 4, 5, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[5], q[9], q[6];
// UNMAPPED c6x [0, 1, 2, 4, 5, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[5], q[9], q[3];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c5x [0, 1, 2, 4, 5, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[4], q[5], q[9];
// UNMAPPED c5x [0, 1, 2, 4, 5, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[4], q[5], q[3];
// UNMAPPED c6x [0, 1, 2, 3, 4, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[9], q[5];
// UNMAPPED c5x [0, 1, 2, 3, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[9], q[4];
// UNMAPPED c8x [0, 1, 2, 4, 6, 7, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[4], q[6], q[7], q[8], q[9], q[5];
// UNMAPPED c8x [0, 1, 2, 4, 6, 7, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[4], q[6], q[7], q[8], q[9], q[3];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 6, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7];
// UNMAPPED c6x [0, 1, 2, 3, 4, 5, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[5], q[6];
// UNMAPPED c5x [0, 1, 2, 3, 5, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[5], q[4];
// UNMAPPED c7x [0, 1, 2, 4, 6, 7, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[4], q[6], q[7], q[8], q[5];
// UNMAPPED c7x [0, 1, 2, 4, 5, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[4], q[5], q[6], q[8], q[7];
// UNMAPPED c6x [0, 1, 2, 4, 5, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[5], q[8], q[6];
// UNMAPPED c7x [0, 1, 2, 4, 6, 7, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[4], q[6], q[7], q[9], q[3];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[9];
// UNMAPPED c6x [0, 1, 2, 3, 4, 6, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[6], q[7];
// UNMAPPED c6x [0, 1, 2, 4, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[6], q[7], q[8];
// UNMAPPED c6x [0, 1, 2, 4, 6, 7, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[6], q[7], q[5];
// UNMAPPED c6x [0, 1, 2, 4, 6, 7, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[6], q[7], q[3];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[7];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[6];
// UNMAPPED c7x [0, 1, 2, 4, 6, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[4], q[6], q[8], q[9], q[5];
// UNMAPPED c7x [0, 1, 2, 4, 5, 6, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[4], q[5], q[6], q[8], q[9];
// UNMAPPED c6x [0, 1, 2, 4, 5, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[5], q[6], q[8];
// UNMAPPED c6x [0, 1, 2, 4, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[6], q[8], q[7];
// UNMAPPED c6x [0, 1, 2, 4, 6, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[6], q[8], q[5];
// UNMAPPED c6x [0, 1, 2, 4, 6, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[6], q[8], q[3];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8];
// UNMAPPED c6x [0, 1, 2, 4, 6, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[6], q[9], q[8];
// UNMAPPED c6x [0, 1, 2, 4, 6, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[6], q[9], q[3];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[9];
// UNMAPPED c5x [0, 1, 2, 4, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[4], q[6], q[8];
// UNMAPPED c5x [0, 1, 2, 4, 6, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[4], q[6], q[3];
// UNMAPPED c7x [0, 1, 2, 4, 7, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[4], q[7], q[8], q[9], q[3];
// UNMAPPED c7x [0, 1, 2, 3, 4, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[7], q[9], q[8];
// UNMAPPED c6x [0, 1, 2, 3, 7, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[7], q[9], q[4];
// UNMAPPED c6x [0, 1, 2, 4, 7, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[7], q[8], q[5];
// UNMAPPED c6x [0, 1, 2, 4, 5, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[5], q[7], q[8];
// UNMAPPED c6x [0, 1, 2, 4, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[7], q[9], q[8];
// UNMAPPED c6x [0, 1, 2, 4, 7, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[7], q[9], q[6];
// UNMAPPED c7x [0, 1, 2, 4, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[4], q[6], q[7], q[8], q[9];
// UNMAPPED c5x [0, 1, 2, 4, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[4], q[7], q[9];
// UNMAPPED c5x [0, 1, 2, 4, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[4], q[7], q[8];
// UNMAPPED c5x [0, 1, 2, 4, 7, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[4], q[7], q[3];
// UNMAPPED c7x [0, 1, 2, 3, 4, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[8], q[9], q[7];
// UNMAPPED c6x [0, 1, 2, 3, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[8], q[9], q[4];
// UNMAPPED c6x [0, 1, 2, 4, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[8], q[9], q[6];
// UNMAPPED c6x [0, 1, 2, 4, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[8], q[9], q[5];
// UNMAPPED c7x [0, 1, 2, 4, 5, 6, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[4], q[5], q[6], q[9], q[8];
// UNMAPPED c5x [0, 1, 2, 4, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[4], q[8], q[5];
// UNMAPPED c5x [0, 1, 2, 4, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[4], q[8], q[3];
// UNMAPPED c5x [0, 1, 2, 4, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[4], q[9], q[7];
// UNMAPPED c5x [0, 1, 2, 4, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[4], q[9], q[6];
// UNMAPPED c5x [0, 1, 2, 4, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[4], q[9], q[3];
// UNMAPPED c7x [0, 1, 2, 3, 6, 7, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[6], q[7], q[9], q[4];
// UNMAPPED c4x [0, 1, 2, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[4], q[9];
// UNMAPPED c4x [0, 1, 2, 4, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[4], q[7];
// UNMAPPED c4x [0, 1, 2, 4, 6]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[4], q[6];
// UNMAPPED c8x [0, 1, 2, 5, 6, 7, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[5], q[6], q[7], q[8], q[9], q[4];
// UNMAPPED c8x [0, 1, 2, 5, 6, 7, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[5], q[6], q[7], q[8], q[9], q[3];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 7, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[6];
// UNMAPPED c7x [0, 1, 2, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c7x [0, 1, 2, 5, 6, 7, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[5], q[6], q[7], q[8], q[3];
// UNMAPPED c7x [0, 1, 2, 5, 6, 7, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[5], q[6], q[7], q[9], q[4];
// UNMAPPED c7x [0, 1, 2, 5, 6, 7, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[5], q[6], q[7], q[9], q[3];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[7];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[9], q[6];
// UNMAPPED c6x [0, 1, 2, 5, 6, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[5], q[6], q[7], q[9];
// UNMAPPED c6x [0, 1, 2, 5, 6, 7, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[5], q[6], q[7], q[3];
// UNMAPPED c7x [0, 1, 2, 3, 5, 6, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[6], q[9], q[7];
// UNMAPPED c7x [0, 1, 2, 5, 6, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[5], q[6], q[8], q[9], q[4];
// UNMAPPED c7x [0, 1, 2, 5, 6, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[5], q[6], q[8], q[9], q[3];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[9], q[6];
// UNMAPPED c6x [0, 1, 2, 5, 6, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[5], q[6], q[8], q[9];
// UNMAPPED c6x [0, 1, 2, 5, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[5], q[6], q[8], q[7];
// UNMAPPED c6x [0, 1, 2, 5, 6, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[5], q[6], q[8], q[3];
// UNMAPPED c6x [0, 1, 2, 5, 6, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[5], q[6], q[9], q[8];
// UNMAPPED c6x [0, 1, 2, 5, 6, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[5], q[6], q[9], q[4];
// UNMAPPED c6x [0, 1, 2, 5, 6, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[5], q[6], q[9], q[3];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[9], q[6];
// UNMAPPED c7x [0, 1, 2, 3, 4, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[8], q[9], q[5];
// UNMAPPED c5x [0, 1, 2, 5, 6, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[5], q[6], q[9];
// UNMAPPED c5x [0, 1, 2, 5, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[5], q[6], q[8];
// UNMAPPED c5x [0, 1, 2, 5, 6, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[5], q[6], q[7];
// UNMAPPED c5x [0, 1, 2, 5, 6, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[5], q[6], q[3];
// UNMAPPED c7x [0, 1, 2, 5, 7, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[5], q[7], q[8], q[9], q[6];
// UNMAPPED c7x [0, 1, 2, 5, 7, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[5], q[7], q[8], q[9], q[4];
// UNMAPPED c8x [0, 1, 2, 4, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[4], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c7x [0, 1, 2, 4, 5, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[4], q[5], q[6], q[7], q[8];
// UNMAPPED c6x [0, 1, 2, 4, 5, 6, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[5], q[6], q[7];
// UNMAPPED c5x [0, 1, 2, 4, 6, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[4], q[6], q[5];
// UNMAPPED c6x [0, 1, 2, 5, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[5], q[7], q[8], q[9];
// UNMAPPED c6x [0, 1, 2, 5, 7, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[5], q[7], q[8], q[6];
// UNMAPPED c6x [0, 1, 2, 5, 7, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[5], q[7], q[8], q[4];
// UNMAPPED c6x [0, 1, 2, 5, 7, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[5], q[7], q[8], q[3];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 7, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[5];
// UNMAPPED c6x [0, 1, 2, 5, 7, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[5], q[7], q[9], q[4];
// UNMAPPED c6x [0, 1, 2, 5, 7, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[5], q[7], q[9], q[3];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[9], q[7];
// UNMAPPED c6x [0, 1, 2, 3, 4, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[9], q[5];
// UNMAPPED c5x [0, 1, 2, 5, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[5], q[7], q[9];
// UNMAPPED c5x [0, 1, 2, 5, 7, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[5], q[7], q[4];
// UNMAPPED c6x [0, 1, 2, 4, 7, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[7], q[9], q[5];
// UNMAPPED c6x [0, 1, 2, 5, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[5], q[8], q[9], q[7];
// UNMAPPED c6x [0, 1, 2, 5, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[5], q[8], q[9], q[6];
// UNMAPPED c6x [0, 1, 2, 5, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[5], q[8], q[9], q[3];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[9], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 6, 7, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[6], q[7], q[9], q[5];
// UNMAPPED c5x [0, 1, 2, 5, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[5], q[8], q[7];
// UNMAPPED c5x [0, 1, 2, 5, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[5], q[8], q[3];
// UNMAPPED c6x [0, 1, 2, 3, 7, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[7], q[8], q[5];
// UNMAPPED c5x [0, 1, 2, 5, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[5], q[9], q[8];
// UNMAPPED c5x [0, 1, 2, 5, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[5], q[9], q[4];
// UNMAPPED c4x [0, 1, 2, 5, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[5], q[7];
// UNMAPPED c4x [0, 1, 2, 5, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[5], q[4];
// UNMAPPED c4x [0, 1, 2, 5, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[5], q[3];
// UNMAPPED c6x [0, 1, 2, 3, 4, 7, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[7], q[5];
// UNMAPPED c7x [0, 1, 2, 6, 7, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[6], q[7], q[8], q[9], q[4];
// UNMAPPED c7x [0, 1, 2, 6, 7, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[6], q[7], q[8], q[9], q[3];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 4, 7, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[6];
// UNMAPPED c6x [0, 1, 2, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[6], q[7], q[8], q[9];
// UNMAPPED c6x [0, 1, 2, 6, 7, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[6], q[7], q[8], q[4];
// UNMAPPED c7x [0, 1, 2, 4, 7, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[4], q[7], q[8], q[9], q[6];
// UNMAPPED c6x [0, 1, 2, 6, 7, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[6], q[7], q[9], q[3];
// UNMAPPED c6x [0, 1, 2, 3, 6, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[6], q[9], q[7];
// UNMAPPED c5x [0, 1, 2, 3, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[9], q[6];
// UNMAPPED c5x [0, 1, 2, 6, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[6], q[7], q[9];
// UNMAPPED c5x [0, 1, 2, 6, 7, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[6], q[7], q[5];
// UNMAPPED c5x [0, 1, 2, 6, 7, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[6], q[7], q[3];
// UNMAPPED c6x [0, 1, 2, 6, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[6], q[8], q[9], q[3];
// UNMAPPED c6x [0, 1, 2, 3, 6, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[6], q[9], q[8];
// UNMAPPED c5x [0, 1, 2, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[6], q[8], q[7];
// UNMAPPED c5x [0, 1, 2, 6, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[6], q[8], q[5];
// UNMAPPED c6x [0, 1, 2, 5, 7, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[5], q[7], q[8], q[6];
// UNMAPPED c5x [0, 1, 2, 6, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[6], q[9], q[8];
// UNMAPPED c4x [0, 1, 2, 6, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[6], q[9];
// UNMAPPED c4x [0, 1, 2, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[6], q[8];
// UNMAPPED c4x [0, 1, 2, 6, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[6], q[5];
// UNMAPPED c4x [0, 1, 2, 6, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[6], q[4];
// UNMAPPED c6x [0, 1, 2, 7, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[7], q[8], q[9], q[4];
// UNMAPPED c6x [0, 1, 2, 4, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[7], q[8], q[9];
// UNMAPPED c5x [0, 1, 2, 4, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[4], q[7], q[8];
// UNMAPPED c5x [0, 1, 2, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[7], q[8], q[9];
// UNMAPPED c5x [0, 1, 2, 7, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[7], q[8], q[6];
// UNMAPPED c5x [0, 1, 2, 7, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[7], q[8], q[5];
// UNMAPPED c5x [0, 1, 2, 7, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[7], q[8], q[4];
// UNMAPPED c5x [0, 1, 2, 7, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[7], q[8], q[3];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[8];
// UNMAPPED c5x [0, 1, 2, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[7], q[9], q[8];
// UNMAPPED c5x [0, 1, 2, 7, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[7], q[9], q[6];
// UNMAPPED c5x [0, 1, 2, 7, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[7], q[9], q[5];
// UNMAPPED c7x [0, 1, 2, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c6x [0, 1, 2, 5, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[5], q[6], q[8], q[7];
// UNMAPPED c4x [0, 1, 2, 7, 6]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[7], q[6];
// UNMAPPED c4x [0, 1, 2, 7, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[7], q[4];
// UNMAPPED c4x [0, 1, 2, 7, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[7], q[3];
// UNMAPPED c6x [0, 1, 2, 3, 4, 6, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[6], q[7];
// UNMAPPED c5x [0, 1, 2, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[8], q[9], q[7];
// UNMAPPED c5x [0, 1, 2, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[8], q[9], q[4];
// UNMAPPED c6x [0, 1, 2, 4, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[7], q[8], q[9];
// UNMAPPED c4x [0, 1, 2, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[8], q[6];
// UNMAPPED c4x [0, 1, 2, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[9], q[8];
// UNMAPPED c4x [0, 1, 2, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[9], q[6];
// UNMAPPED c4x [0, 1, 2, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[9], q[3];
// UNMAPPED c3x [0, 1, 2, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[2], q[9];
// UNMAPPED c3x [0, 1, 2, 6]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[2], q[6];
// UNMAPPED c3x [0, 1, 2, 5]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[2], q[5];
// UNMAPPED c3x [0, 1, 2, 3]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[2], q[3];
// UNMAPPED c9x [0, 1, 3, 4, 5, 6, 7, 8, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[2];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 5, 6, 7, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[4];
// UNMAPPED c8x [0, 1, 3, 4, 5, 6, 7, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[3], q[4], q[5], q[6], q[7], q[8], q[2];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 6, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7];
// UNMAPPED c6x [0, 1, 2, 3, 4, 5, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[5], q[6];
// UNMAPPED c5x [0, 1, 2, 3, 4, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[4], q[5];
// UNMAPPED c4x [0, 1, 2, 3, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[3], q[4];
// UNMAPPED c8x [0, 1, 3, 4, 5, 6, 7, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[3], q[4], q[5], q[6], q[7], q[9], q[2];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 5, 6, 7, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[4];
// UNMAPPED c7x [0, 1, 3, 4, 5, 6, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[4], q[5], q[6], q[7], q[9];
// UNMAPPED c7x [0, 1, 3, 4, 5, 6, 7, 2]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[4], q[5], q[6], q[7], q[2];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[7];
// UNMAPPED c7x [0, 1, 2, 3, 5, 6, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[6], q[9], q[4];
// UNMAPPED c6x [0, 1, 2, 5, 6, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[5], q[6], q[9], q[3];
// UNMAPPED c8x [0, 1, 3, 4, 5, 6, 8, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[3], q[4], q[5], q[6], q[8], q[9], q[2];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[9], q[4];
// UNMAPPED c7x [0, 1, 3, 4, 5, 6, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[4], q[5], q[6], q[8], q[2];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8];
// UNMAPPED c6x [0, 1, 2, 3, 4, 5, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[5], q[6];
// UNMAPPED c5x [0, 1, 2, 3, 5, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[5], q[4];
// UNMAPPED c4x [0, 1, 2, 5, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[5], q[3];
// UNMAPPED c7x [0, 1, 3, 4, 5, 6, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[4], q[5], q[6], q[9], q[2];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[9], q[5];
// UNMAPPED c6x [0, 1, 2, 3, 6, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[6], q[9], q[4];
// UNMAPPED c6x [0, 1, 3, 4, 5, 6, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[4], q[5], q[6], q[9];
// UNMAPPED c6x [0, 1, 3, 4, 5, 6, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[4], q[5], q[6], q[2];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[9], q[6];
// UNMAPPED c6x [0, 1, 2, 3, 4, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[9], q[5];
// UNMAPPED c5x [0, 1, 2, 3, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[9], q[4];
// UNMAPPED c8x [0, 1, 3, 4, 5, 7, 8, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[3], q[4], q[5], q[7], q[8], q[9], q[2];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[9], q[8];
// UNMAPPED c7x [0, 1, 3, 4, 5, 7, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[4], q[5], q[7], q[8], q[6];
// UNMAPPED c7x [0, 1, 3, 4, 5, 7, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[4], q[5], q[7], q[8], q[2];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 6, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7];
// UNMAPPED c6x [0, 1, 2, 3, 5, 6, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[6], q[4];
// UNMAPPED c5x [0, 1, 2, 5, 6, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[5], q[6], q[3];
// UNMAPPED c7x [0, 1, 3, 4, 5, 7, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[4], q[5], q[7], q[9], q[2];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[9], q[7];
// UNMAPPED c6x [0, 1, 2, 4, 5, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[5], q[9], q[3];
// UNMAPPED c6x [0, 1, 3, 4, 5, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[4], q[5], q[7], q[8];
// UNMAPPED c6x [0, 1, 3, 4, 5, 7, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[4], q[5], q[7], q[6];
// UNMAPPED c6x [0, 1, 3, 4, 5, 7, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[4], q[5], q[7], q[2];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[7];
// UNMAPPED c7x [0, 1, 3, 4, 5, 8, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[4], q[5], q[8], q[9], q[2];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[9];
// UNMAPPED c6x [0, 1, 2, 3, 4, 5, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[5], q[8];
// UNMAPPED c5x [0, 1, 2, 3, 4, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[4], q[5];
// UNMAPPED c4x [0, 1, 2, 3, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[3], q[4];
// UNMAPPED c3x [0, 1, 2, 3]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[2], q[3];
// UNMAPPED c6x [0, 1, 3, 4, 5, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[4], q[5], q[8], q[7];
// UNMAPPED c6x [0, 1, 3, 4, 5, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[4], q[5], q[8], q[6];
// UNMAPPED c6x [0, 1, 3, 4, 5, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[4], q[5], q[8], q[2];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 7, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[5];
// UNMAPPED c6x [0, 1, 3, 4, 5, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[4], q[5], q[9], q[8];
// UNMAPPED c6x [0, 1, 3, 4, 5, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[4], q[5], q[9], q[2];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[9];
// UNMAPPED c6x [0, 1, 2, 3, 4, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[8], q[5];
// UNMAPPED c5x [0, 1, 3, 4, 5, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[4], q[5], q[9];
// UNMAPPED c5x [0, 1, 3, 4, 5, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[4], q[5], q[2];
// UNMAPPED c8x [0, 1, 3, 4, 6, 7, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[3], q[4], q[6], q[7], q[8], q[9], q[5];
// UNMAPPED c8x [0, 1, 3, 4, 6, 7, 8, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[3], q[4], q[6], q[7], q[8], q[9], q[2];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 6, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7];
// UNMAPPED c6x [0, 1, 2, 3, 4, 5, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[5], q[6];
// UNMAPPED c5x [0, 1, 2, 3, 5, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[5], q[4];
// UNMAPPED c4x [0, 1, 2, 5, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[5], q[3];
// UNMAPPED c7x [0, 1, 3, 4, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[4], q[6], q[7], q[8], q[9];
// UNMAPPED c7x [0, 1, 3, 4, 6, 7, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[4], q[6], q[7], q[8], q[2];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[9], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[9], q[7];
// UNMAPPED c6x [0, 1, 2, 3, 4, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[9], q[6];
// UNMAPPED c5x [0, 1, 2, 4, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[4], q[9], q[3];
// UNMAPPED c7x [0, 1, 3, 4, 6, 7, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[4], q[6], q[7], q[9], q[5];
// UNMAPPED c7x [0, 1, 3, 4, 5, 7, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[4], q[5], q[7], q[9], q[6];
// UNMAPPED c6x [0, 1, 3, 4, 6, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[4], q[6], q[7], q[9];
// UNMAPPED c6x [0, 1, 3, 4, 6, 7, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[4], q[6], q[7], q[2];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[9], q[7];
// UNMAPPED c6x [0, 1, 2, 3, 4, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[9], q[6];
// UNMAPPED c5x [0, 1, 2, 4, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[4], q[9], q[3];
// UNMAPPED c7x [0, 1, 3, 4, 6, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[4], q[6], q[8], q[9], q[7];
// UNMAPPED c7x [0, 1, 3, 4, 6, 8, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[4], q[6], q[8], q[9], q[2];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 6, 7, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[6], q[7], q[8], q[4];
// UNMAPPED c6x [0, 1, 2, 6, 7, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[6], q[7], q[8], q[3];
// UNMAPPED c6x [0, 1, 3, 4, 6, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[4], q[6], q[8], q[9];
// UNMAPPED c6x [0, 1, 3, 4, 6, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[4], q[6], q[8], q[5];
// UNMAPPED c6x [0, 1, 3, 4, 6, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[4], q[6], q[8], q[2];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[9], q[6];
// UNMAPPED c6x [0, 1, 2, 3, 5, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[9], q[4];
// UNMAPPED c5x [0, 1, 2, 5, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[5], q[9], q[3];
// UNMAPPED c6x [0, 1, 3, 4, 6, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[4], q[6], q[9], q[8];
// UNMAPPED c6x [0, 1, 3, 4, 6, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[4], q[6], q[9], q[5];
// UNMAPPED c7x [0, 1, 3, 4, 5, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[4], q[5], q[8], q[9], q[6];
// UNMAPPED c5x [0, 1, 3, 4, 6, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[4], q[6], q[9];
// UNMAPPED c5x [0, 1, 3, 4, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[4], q[6], q[8];
// UNMAPPED c5x [0, 1, 3, 4, 6, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[4], q[6], q[2];
// UNMAPPED c7x [0, 1, 2, 4, 6, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[4], q[6], q[8], q[9], q[3];
// UNMAPPED c7x [0, 1, 3, 4, 7, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[4], q[7], q[8], q[9], q[6];
// UNMAPPED c7x [0, 1, 3, 4, 7, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[4], q[7], q[8], q[9], q[5];
// UNMAPPED c8x [0, 1, 3, 4, 5, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[3], q[4], q[5], q[6], q[7], q[9], q[8];
// UNMAPPED c7x [0, 1, 3, 4, 5, 6, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[4], q[5], q[6], q[9], q[7];
// UNMAPPED c6x [0, 1, 3, 4, 7, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[4], q[7], q[8], q[6];
// UNMAPPED c6x [0, 1, 3, 4, 7, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[4], q[7], q[8], q[2];
// UNMAPPED c7x [0, 1, 2, 3, 6, 7, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[6], q[7], q[8], q[4];
// UNMAPPED c6x [0, 1, 2, 6, 7, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[6], q[7], q[8], q[3];
// UNMAPPED c6x [0, 1, 3, 4, 7, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[4], q[7], q[9], q[6];
// UNMAPPED c6x [0, 1, 3, 4, 7, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[4], q[7], q[9], q[5];
// UNMAPPED c7x [0, 1, 3, 4, 5, 6, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[4], q[5], q[6], q[7], q[9];
// UNMAPPED c5x [0, 1, 3, 4, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[4], q[7], q[9];
// UNMAPPED c5x [0, 1, 3, 4, 7, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[4], q[7], q[6];
// UNMAPPED c5x [0, 1, 3, 4, 7, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[4], q[7], q[5];
// UNMAPPED c5x [0, 1, 3, 4, 7, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[4], q[7], q[2];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 7, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[9], q[4];
// UNMAPPED c7x [0, 1, 2, 5, 6, 7, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[5], q[6], q[7], q[9], q[3];
// UNMAPPED c6x [0, 1, 3, 4, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[4], q[8], q[9], q[7];
// UNMAPPED c6x [0, 1, 3, 4, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[4], q[8], q[9], q[6];
// UNMAPPED c6x [0, 1, 3, 4, 8, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[4], q[8], q[9], q[2];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[9], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 6, 7, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[6], q[7], q[9], q[4];
// UNMAPPED c5x [0, 1, 3, 4, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[4], q[8], q[9];
// UNMAPPED c5x [0, 1, 3, 4, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[4], q[8], q[6];
// UNMAPPED c5x [0, 1, 3, 4, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[4], q[8], q[5];
// UNMAPPED c5x [0, 1, 3, 4, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[4], q[9], q[5];
// UNMAPPED c4x [0, 1, 3, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[3], q[4], q[8];
// UNMAPPED c4x [0, 1, 3, 4, 6]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[3], q[4], q[6];
// UNMAPPED c4x [0, 1, 3, 4, 2]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[3], q[4], q[2];
// UNMAPPED c6x [0, 1, 2, 3, 6, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[6], q[8], q[4];
// UNMAPPED c5x [0, 1, 2, 6, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[6], q[8], q[3];
// UNMAPPED c8x [0, 1, 3, 5, 6, 7, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[3], q[5], q[6], q[7], q[8], q[9], q[4];
// UNMAPPED c8x [0, 1, 3, 4, 5, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[3], q[4], q[5], q[6], q[7], q[9], q[8];
// UNMAPPED c7x [0, 1, 3, 4, 5, 6, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[4], q[5], q[6], q[9], q[7];
// UNMAPPED c6x [0, 1, 3, 4, 5, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[4], q[5], q[9], q[6];
// UNMAPPED c5x [0, 1, 3, 4, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[4], q[9], q[5];
// UNMAPPED c7x [0, 1, 3, 5, 6, 7, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[5], q[6], q[7], q[8], q[2];
// UNMAPPED c7x [0, 1, 2, 3, 6, 7, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[6], q[7], q[8], q[5];
// UNMAPPED c7x [0, 1, 3, 5, 6, 7, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[5], q[6], q[7], q[9], q[4];
// UNMAPPED c6x [0, 1, 3, 5, 6, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[5], q[6], q[7], q[9];
// UNMAPPED c6x [0, 1, 3, 5, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[5], q[6], q[7], q[8];
// UNMAPPED c6x [0, 1, 3, 5, 6, 7, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[5], q[6], q[7], q[4];
// UNMAPPED c8x [0, 1, 3, 4, 5, 7, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[3], q[4], q[5], q[7], q[8], q[9], q[6];
// UNMAPPED c7x [0, 1, 3, 4, 7, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[4], q[7], q[8], q[9], q[5];
// UNMAPPED c7x [0, 1, 3, 5, 6, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[5], q[6], q[8], q[9], q[7];
// UNMAPPED c7x [0, 1, 3, 5, 6, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[5], q[6], q[8], q[9], q[4];
// UNMAPPED c7x [0, 1, 3, 5, 6, 8, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[5], q[6], q[8], q[9], q[2];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 7, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[9], q[6];
// UNMAPPED c7x [0, 1, 2, 3, 4, 7, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[7], q[9], q[5];
// UNMAPPED c6x [0, 1, 3, 5, 6, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[5], q[6], q[8], q[9];
// UNMAPPED c6x [0, 1, 3, 5, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[5], q[6], q[8], q[7];
// UNMAPPED c6x [0, 1, 3, 5, 6, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[5], q[6], q[8], q[2];
// UNMAPPED c6x [0, 1, 3, 5, 6, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[5], q[6], q[9], q[8];
// UNMAPPED c6x [0, 1, 3, 5, 6, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[5], q[6], q[9], q[2];
// UNMAPPED c7x [0, 1, 2, 5, 6, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[5], q[6], q[8], q[9], q[3];
// UNMAPPED c5x [0, 1, 3, 5, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[5], q[6], q[8];
// UNMAPPED c5x [0, 1, 3, 5, 6, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[5], q[6], q[7];
// UNMAPPED c5x [0, 1, 3, 5, 6, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[5], q[6], q[2];
// UNMAPPED c7x [0, 1, 2, 3, 6, 7, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[6], q[7], q[8], q[5];
// UNMAPPED c7x [0, 1, 3, 5, 7, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[5], q[7], q[8], q[9], q[6];
// UNMAPPED c7x [0, 1, 3, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c6x [0, 1, 3, 5, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[5], q[6], q[8], q[7];
// UNMAPPED c6x [0, 1, 3, 5, 7, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[5], q[7], q[8], q[6];
// UNMAPPED c6x [0, 1, 3, 5, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[5], q[6], q[7], q[8];
// UNMAPPED c5x [0, 1, 3, 5, 6, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[5], q[6], q[7];
// UNMAPPED c6x [0, 1, 3, 5, 7, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[5], q[7], q[9], q[6];
// UNMAPPED c6x [0, 1, 3, 5, 7, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[5], q[7], q[9], q[4];
// UNMAPPED c6x [0, 1, 3, 5, 7, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[5], q[7], q[9], q[2];
// UNMAPPED c5x [0, 1, 3, 5, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[5], q[7], q[9];
// UNMAPPED c5x [0, 1, 3, 5, 7, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[5], q[7], q[6];
// UNMAPPED c5x [0, 1, 3, 5, 7, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[5], q[7], q[2];
// UNMAPPED c7x [0, 1, 2, 3, 6, 7, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[6], q[7], q[9], q[5];
// UNMAPPED c6x [0, 1, 3, 5, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[5], q[8], q[9], q[7];
// UNMAPPED c6x [0, 1, 3, 5, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[5], q[8], q[9], q[6];
// UNMAPPED c6x [0, 1, 3, 5, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[5], q[8], q[9], q[4];
// UNMAPPED c6x [0, 1, 3, 5, 8, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[5], q[8], q[9], q[2];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[8];
// UNMAPPED c8x [0, 1, 2, 4, 5, 6, 7, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[4], q[5], q[6], q[7], q[9], q[3];
// UNMAPPED c5x [0, 1, 3, 5, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[5], q[8], q[9];
// UNMAPPED c5x [0, 1, 3, 5, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[5], q[8], q[4];
// UNMAPPED c6x [0, 1, 3, 4, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[4], q[8], q[9], q[5];
// UNMAPPED c5x [0, 1, 3, 5, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[5], q[9], q[7];
// UNMAPPED c5x [0, 1, 3, 5, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[5], q[9], q[6];
// UNMAPPED c4x [0, 1, 3, 5, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[3], q[5], q[9];
// UNMAPPED c4x [0, 1, 3, 5, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[3], q[5], q[7];
// UNMAPPED c4x [0, 1, 3, 5, 6]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[3], q[5], q[6];
// UNMAPPED c4x [0, 1, 3, 5, 2]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[3], q[5], q[2];
// UNMAPPED c7x [0, 1, 2, 3, 6, 7, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[6], q[7], q[9], q[5];
// UNMAPPED c7x [0, 1, 3, 6, 7, 8, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[6], q[7], q[8], q[9], q[2];
// UNMAPPED c7x [0, 1, 2, 3, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[6], q[7], q[8], q[9];
// UNMAPPED c6x [0, 1, 3, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[6], q[7], q[8], q[9];
// UNMAPPED c6x [0, 1, 3, 6, 7, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[6], q[7], q[8], q[5];
// UNMAPPED c6x [0, 1, 3, 6, 7, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[6], q[7], q[8], q[4];
// UNMAPPED c6x [0, 1, 3, 6, 7, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[6], q[7], q[8], q[2];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 7, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[9], q[6];
// UNMAPPED c6x [0, 1, 3, 6, 7, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[6], q[7], q[9], q[5];
// UNMAPPED c6x [0, 1, 3, 6, 7, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[6], q[7], q[9], q[4];
// UNMAPPED c6x [0, 1, 3, 6, 7, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[6], q[7], q[9], q[2];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[7];
// UNMAPPED c5x [0, 1, 3, 6, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[6], q[7], q[9];
// UNMAPPED c5x [0, 1, 3, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[6], q[7], q[8];
// UNMAPPED c5x [0, 1, 3, 6, 7, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[6], q[7], q[4];
// UNMAPPED c5x [0, 1, 3, 6, 7, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[6], q[7], q[2];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[9], q[7];
// UNMAPPED c7x [0, 1, 2, 3, 4, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[8], q[9], q[6];
// UNMAPPED c6x [0, 1, 2, 4, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[8], q[9], q[3];
// UNMAPPED c6x [0, 1, 3, 6, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[6], q[8], q[9], q[7];
// UNMAPPED c6x [0, 1, 3, 6, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[6], q[8], q[9], q[5];
// UNMAPPED c6x [0, 1, 3, 6, 8, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[6], q[8], q[9], q[2];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[9], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 5, 7, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[7], q[9], q[6];
// UNMAPPED c5x [0, 1, 3, 6, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[6], q[8], q[4];
// UNMAPPED c5x [0, 1, 3, 4, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[4], q[6], q[8];
// UNMAPPED c4x [0, 1, 3, 4, 6]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[3], q[4], q[6];
// UNMAPPED c5x [0, 1, 3, 6, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[6], q[9], q[8];
// UNMAPPED c5x [0, 1, 3, 6, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[6], q[9], q[5];
// UNMAPPED c5x [0, 1, 3, 6, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[6], q[9], q[2];
// UNMAPPED c7x [0, 1, 2, 3, 5, 6, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[9];
// UNMAPPED c6x [0, 1, 2, 5, 6, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[5], q[6], q[8], q[3];
// UNMAPPED c4x [0, 1, 3, 6, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[3], q[6], q[9];
// UNMAPPED c4x [0, 1, 3, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[3], q[6], q[8];
// UNMAPPED c4x [0, 1, 3, 6, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[3], q[6], q[4];
// UNMAPPED c4x [0, 1, 3, 6, 2]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[3], q[6], q[2];
// UNMAPPED c7x [0, 1, 2, 3, 4, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[8], q[9], q[6];
// UNMAPPED c6x [0, 1, 2, 4, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[8], q[9], q[3];
// UNMAPPED c6x [0, 1, 3, 7, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[7], q[8], q[9], q[5];
// UNMAPPED c6x [0, 1, 3, 7, 8, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[7], q[8], q[9], q[2];
// UNMAPPED c7x [0, 1, 2, 3, 5, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[8], q[9], q[7];
// UNMAPPED c5x [0, 1, 3, 7, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[7], q[8], q[5];
// UNMAPPED c5x [0, 1, 3, 7, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[7], q[8], q[4];
// UNMAPPED c5x [0, 1, 3, 7, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[7], q[8], q[2];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[7];
// UNMAPPED c5x [0, 1, 3, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[7], q[9], q[8];
// UNMAPPED c5x [0, 1, 3, 7, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[7], q[9], q[5];
// UNMAPPED c6x [0, 1, 3, 5, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[5], q[8], q[9], q[7];
// UNMAPPED c4x [0, 1, 3, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[3], q[7], q[8];
// UNMAPPED c4x [0, 1, 3, 7, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[3], q[7], q[4];
// UNMAPPED c4x [0, 1, 3, 7, 2]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[3], q[7], q[2];
// UNMAPPED c6x [0, 1, 2, 4, 7, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[7], q[8], q[3];
// UNMAPPED c5x [0, 1, 3, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[8], q[9], q[5];
// UNMAPPED c5x [0, 1, 3, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[8], q[9], q[4];
// UNMAPPED c5x [0, 1, 3, 8, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[8], q[9], q[2];
// UNMAPPED c7x [0, 1, 2, 4, 5, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[4], q[5], q[8], q[9], q[3];
// UNMAPPED c4x [0, 1, 3, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[3], q[8], q[4];
// UNMAPPED c4x [0, 1, 3, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[3], q[9], q[8];
// UNMAPPED c4x [0, 1, 3, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[3], q[9], q[6];
// UNMAPPED c4x [0, 1, 3, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[3], q[9], q[2];
// UNMAPPED c6x [0, 1, 2, 6, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[6], q[8], q[9], q[3];
// UNMAPPED c3x [0, 1, 3, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[3], q[8];
// UNMAPPED c3x [0, 1, 3, 6]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[3], q[6];
// UNMAPPED c3x [0, 1, 3, 2]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[3], q[2];
// UNMAPPED c5x [0, 1, 2, 6, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[6], q[8], q[3];
// UNMAPPED c8x [0, 1, 4, 5, 6, 7, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[4], q[5], q[6], q[7], q[8], q[9], q[3];
// UNMAPPED c8x [0, 1, 4, 5, 6, 7, 8, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[4], q[5], q[6], q[7], q[8], q[9], q[2];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 7, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[9], q[4];
// UNMAPPED c7x [0, 1, 4, 5, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[4], q[5], q[6], q[7], q[9], q[8];
// UNMAPPED c7x [0, 1, 4, 5, 6, 7, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[4], q[5], q[6], q[7], q[9], q[3];
// UNMAPPED c8x [0, 1, 3, 4, 5, 6, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[3], q[4], q[5], q[6], q[8], q[9], q[7];
// UNMAPPED c7x [0, 1, 3, 5, 6, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[5], q[6], q[8], q[9], q[4];
// UNMAPPED c6x [0, 1, 4, 5, 6, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[4], q[5], q[6], q[7], q[9];
// UNMAPPED c6x [0, 1, 4, 5, 6, 7, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[4], q[5], q[6], q[7], q[2];
// UNMAPPED c7x [0, 1, 2, 4, 5, 7, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[4], q[5], q[7], q[9], q[6];
// UNMAPPED c7x [0, 1, 4, 5, 6, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[4], q[5], q[6], q[8], q[9], q[3];
// UNMAPPED c7x [0, 1, 4, 5, 6, 8, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[4], q[5], q[6], q[8], q[9], q[2];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[9], q[6];
// UNMAPPED c6x [0, 1, 2, 3, 5, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[9], q[4];
// UNMAPPED c6x [0, 1, 4, 5, 6, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[4], q[5], q[6], q[8], q[9];
// UNMAPPED c6x [0, 1, 4, 5, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[4], q[5], q[6], q[8], q[7];
// UNMAPPED c6x [0, 1, 4, 5, 6, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[4], q[5], q[6], q[8], q[3];
// UNMAPPED c6x [0, 1, 4, 5, 6, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[4], q[5], q[6], q[8], q[2];
// UNMAPPED c6x [0, 1, 4, 5, 6, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[4], q[5], q[6], q[9], q[8];
// UNMAPPED c6x [0, 1, 4, 5, 6, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[4], q[5], q[6], q[9], q[2];
// UNMAPPED c7x [0, 1, 2, 4, 5, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[4], q[5], q[8], q[9], q[6];
// UNMAPPED c5x [0, 1, 4, 5, 6, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[4], q[5], q[6], q[9];
// UNMAPPED c5x [0, 1, 4, 5, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[4], q[5], q[6], q[8];
// UNMAPPED c5x [0, 1, 4, 5, 6, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[4], q[5], q[6], q[7];
// UNMAPPED c5x [0, 1, 4, 5, 6, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[4], q[5], q[6], q[2];
// UNMAPPED c8x [0, 1, 2, 4, 5, 7, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[4], q[5], q[7], q[8], q[9], q[6];
// UNMAPPED c7x [0, 1, 2, 5, 7, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[5], q[7], q[8], q[9], q[4];
// UNMAPPED c7x [0, 1, 4, 5, 7, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[4], q[5], q[7], q[8], q[9], q[6];
// UNMAPPED c7x [0, 1, 4, 5, 7, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[4], q[5], q[7], q[8], q[9], q[3];
// UNMAPPED c7x [0, 1, 4, 5, 7, 8, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[4], q[5], q[7], q[8], q[9], q[2];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 7, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[9], q[4];
// UNMAPPED c6x [0, 1, 4, 5, 7, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[4], q[5], q[7], q[8], q[2];
// UNMAPPED c6x [0, 1, 2, 4, 5, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[5], q[7], q[8];
// UNMAPPED c5x [0, 1, 2, 4, 7, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[4], q[7], q[5];
// UNMAPPED c4x [0, 1, 2, 7, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[7], q[4];
// UNMAPPED c6x [0, 1, 4, 5, 7, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[4], q[5], q[7], q[9], q[2];
// UNMAPPED c6x [0, 1, 2, 4, 5, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[5], q[7], q[9];
// UNMAPPED c5x [0, 1, 2, 4, 5, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[4], q[5], q[7];
// UNMAPPED c4x [0, 1, 2, 4, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[4], q[5];
// UNMAPPED c5x [0, 1, 4, 5, 7, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[4], q[5], q[7], q[6];
// UNMAPPED c5x [0, 1, 4, 5, 7, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[4], q[5], q[7], q[3];
// UNMAPPED c5x [0, 1, 4, 5, 7, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[4], q[5], q[7], q[2];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 6, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7];
// UNMAPPED c6x [0, 1, 4, 5, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[4], q[5], q[8], q[9], q[7];
// UNMAPPED c6x [0, 1, 4, 5, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[4], q[5], q[8], q[9], q[6];
// UNMAPPED c6x [0, 1, 4, 5, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[4], q[5], q[8], q[9], q[3];
// UNMAPPED c8x [0, 1, 3, 4, 5, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[3], q[4], q[5], q[6], q[7], q[9], q[8];
// UNMAPPED c5x [0, 1, 4, 5, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[4], q[5], q[8], q[2];
// UNMAPPED c5x [0, 1, 2, 4, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[4], q[8], q[5];
// UNMAPPED c4x [0, 1, 2, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[8], q[4];
// UNMAPPED c5x [0, 1, 4, 5, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[4], q[5], q[9], q[6];
// UNMAPPED c5x [0, 1, 4, 5, 6, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[4], q[5], q[6], q[9];
// UNMAPPED c4x [0, 1, 4, 5, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[4], q[5], q[3];
// UNMAPPED c4x [0, 1, 4, 5, 2]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[4], q[5], q[2];
// UNMAPPED c5x [0, 1, 2, 3, 5, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[5], q[4];
// UNMAPPED c7x [0, 1, 4, 6, 7, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[4], q[6], q[7], q[8], q[9], q[5];
// UNMAPPED c7x [0, 1, 4, 6, 7, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[4], q[6], q[7], q[8], q[9], q[3];
// UNMAPPED c8x [0, 1, 3, 4, 5, 6, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[3], q[4], q[5], q[6], q[8], q[9], q[7];
// UNMAPPED c7x [0, 1, 3, 4, 5, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[4], q[5], q[8], q[9], q[6];
// UNMAPPED c6x [0, 1, 3, 5, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[5], q[8], q[9], q[4];
// UNMAPPED c6x [0, 1, 4, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[4], q[6], q[7], q[8], q[9];
// UNMAPPED c6x [0, 1, 4, 6, 7, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[4], q[6], q[7], q[8], q[5];
// UNMAPPED c7x [0, 1, 4, 5, 7, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[4], q[5], q[7], q[8], q[9], q[6];
// UNMAPPED c6x [0, 1, 4, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[4], q[6], q[7], q[9], q[8];
// UNMAPPED c6x [0, 1, 4, 6, 7, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[4], q[6], q[7], q[9], q[5];
// UNMAPPED c6x [0, 1, 4, 6, 7, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[4], q[6], q[7], q[9], q[3];
// UNMAPPED c6x [0, 1, 4, 6, 7, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[4], q[6], q[7], q[9], q[2];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 7, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[6];
// UNMAPPED c5x [0, 1, 4, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[4], q[6], q[7], q[8];
// UNMAPPED c5x [0, 1, 4, 6, 7, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[4], q[6], q[7], q[3];
// UNMAPPED c6x [0, 1, 3, 4, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[4], q[6], q[8], q[7];
// UNMAPPED c5x [0, 1, 3, 6, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[6], q[8], q[4];
// UNMAPPED c6x [0, 1, 4, 6, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[4], q[6], q[8], q[9], q[3];
// UNMAPPED c6x [0, 1, 3, 4, 6, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[4], q[6], q[9], q[8];
// UNMAPPED c5x [0, 1, 3, 6, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[6], q[9], q[4];
// UNMAPPED c5x [0, 1, 4, 6, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[4], q[6], q[8], q[9];
// UNMAPPED c5x [0, 1, 4, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[4], q[6], q[8], q[7];
// UNMAPPED c5x [0, 1, 4, 6, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[4], q[6], q[8], q[2];
// UNMAPPED c7x [0, 1, 2, 4, 7, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[4], q[7], q[8], q[9], q[6];
// UNMAPPED c5x [0, 1, 4, 6, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[4], q[6], q[9], q[8];
// UNMAPPED c5x [0, 1, 4, 6, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[4], q[6], q[9], q[7];
// UNMAPPED c5x [0, 1, 4, 6, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[4], q[6], q[9], q[5];
// UNMAPPED c5x [0, 1, 4, 6, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[4], q[6], q[9], q[3];
// UNMAPPED c5x [0, 1, 4, 6, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[4], q[6], q[9], q[2];
// UNMAPPED c4x [0, 1, 4, 6, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[4], q[6], q[9];
// UNMAPPED c4x [0, 1, 4, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[4], q[6], q[8];
// UNMAPPED c4x [0, 1, 4, 6, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[4], q[6], q[7];
// UNMAPPED c4x [0, 1, 4, 6, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[4], q[6], q[5];
// UNMAPPED c4x [0, 1, 4, 6, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[4], q[6], q[3];
// UNMAPPED c8x [0, 1, 3, 5, 6, 7, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[3], q[5], q[6], q[7], q[8], q[9], q[4];
// UNMAPPED c6x [0, 1, 4, 7, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[4], q[7], q[8], q[9], q[6];
// UNMAPPED c6x [0, 1, 4, 7, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[4], q[7], q[8], q[9], q[3];
// UNMAPPED c6x [0, 1, 4, 7, 8, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[4], q[7], q[8], q[9], q[2];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[9], q[8];
// UNMAPPED c5x [0, 1, 4, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[4], q[7], q[8], q[9];
// UNMAPPED c5x [0, 1, 4, 7, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[4], q[7], q[8], q[3];
// UNMAPPED c6x [0, 1, 3, 7, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[7], q[8], q[9], q[4];
// UNMAPPED c5x [0, 1, 4, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[4], q[7], q[9], q[8];
// UNMAPPED c5x [0, 1, 4, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[4], q[7], q[8], q[9];
// UNMAPPED c4x [0, 1, 4, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[4], q[7], q[9];
// UNMAPPED c4x [0, 1, 4, 7, 6]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[4], q[7], q[6];
// UNMAPPED c4x [0, 1, 4, 7, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[4], q[7], q[5];
// UNMAPPED c4x [0, 1, 4, 7, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[4], q[7], q[3];
// UNMAPPED c7x [0, 1, 3, 5, 6, 7, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[5], q[6], q[7], q[9], q[4];
// UNMAPPED c5x [0, 1, 4, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[4], q[8], q[9], q[7];
// UNMAPPED c5x [0, 1, 4, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[4], q[8], q[9], q[6];
// UNMAPPED c5x [0, 1, 4, 8, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[4], q[8], q[9], q[2];
// UNMAPPED c7x [0, 1, 2, 4, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[4], q[6], q[7], q[9], q[8];
// UNMAPPED c4x [0, 1, 4, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[4], q[8], q[9];
// UNMAPPED c4x [0, 1, 4, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[4], q[8], q[7];
// UNMAPPED c4x [0, 1, 4, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[4], q[8], q[2];
// UNMAPPED c6x [0, 1, 2, 4, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[7], q[9], q[8];
// UNMAPPED c5x [0, 1, 2, 7, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[7], q[9], q[4];
// UNMAPPED c4x [0, 1, 4, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[4], q[9], q[8];
// UNMAPPED c4x [0, 1, 4, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[4], q[9], q[6];
// UNMAPPED c4x [0, 1, 4, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[4], q[9], q[5];
// UNMAPPED c4x [0, 1, 4, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[4], q[9], q[3];
// UNMAPPED c7x [0, 1, 3, 4, 5, 6, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[4], q[5], q[6], q[8], q[9];
// UNMAPPED c6x [0, 1, 3, 5, 6, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[5], q[6], q[8], q[4];
// UNMAPPED c3x [0, 1, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[4], q[8];
// UNMAPPED c3x [0, 1, 4, 3]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[4], q[3];
// UNMAPPED c3x [0, 1, 4, 2]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[4], q[2];
// UNMAPPED c7x [0, 1, 5, 6, 7, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[5], q[6], q[7], q[8], q[9], q[4];
// UNMAPPED c7x [0, 1, 5, 6, 7, 8, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[5], q[6], q[7], q[8], q[9], q[2];
// UNMAPPED c6x [0, 1, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c6x [0, 1, 5, 6, 7, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[5], q[6], q[7], q[8], q[4];
// UNMAPPED c6x [0, 1, 5, 6, 7, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[5], q[6], q[7], q[8], q[2];
// UNMAPPED c8x [0, 1, 2, 4, 5, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[4], q[5], q[6], q[7], q[9], q[8];
// UNMAPPED c6x [0, 1, 5, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[5], q[6], q[7], q[9], q[8];
// UNMAPPED c6x [0, 1, 5, 6, 7, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[5], q[6], q[7], q[9], q[4];
// UNMAPPED c7x [0, 1, 4, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[4], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c6x [0, 1, 4, 5, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[4], q[5], q[6], q[8], q[7];
// UNMAPPED c5x [0, 1, 5, 6, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[5], q[6], q[7], q[9];
// UNMAPPED c5x [0, 1, 5, 6, 7, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[5], q[6], q[7], q[4];
// UNMAPPED c5x [0, 1, 5, 6, 7, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[5], q[6], q[7], q[3];
// UNMAPPED c7x [0, 1, 3, 4, 6, 7, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[4], q[6], q[7], q[9], q[5];
// UNMAPPED c6x [0, 1, 5, 6, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[5], q[6], q[8], q[9], q[7];
// UNMAPPED c6x [0, 1, 5, 6, 8, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[5], q[6], q[8], q[9], q[2];
// UNMAPPED c7x [0, 1, 2, 5, 7, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[5], q[7], q[8], q[9], q[6];
// UNMAPPED c5x [0, 1, 5, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[5], q[6], q[8], q[7];
// UNMAPPED c5x [0, 1, 5, 6, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[5], q[6], q[8], q[2];
// UNMAPPED c6x [0, 1, 2, 5, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[5], q[6], q[7], q[8];
// UNMAPPED c5x [0, 1, 5, 6, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[5], q[6], q[9], q[7];
// UNMAPPED c5x [0, 1, 5, 6, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[5], q[6], q[9], q[4];
// UNMAPPED c5x [0, 1, 5, 6, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[5], q[6], q[9], q[2];
// UNMAPPED c7x [0, 1, 2, 4, 5, 6, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[4], q[5], q[6], q[7], q[9];
// UNMAPPED c6x [0, 1, 2, 4, 6, 7, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[6], q[7], q[5];
// UNMAPPED c4x [0, 1, 5, 6, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[5], q[6], q[7];
// UNMAPPED c4x [0, 1, 5, 6, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[5], q[6], q[4];
// UNMAPPED c4x [0, 1, 5, 6, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[5], q[6], q[3];
// UNMAPPED c6x [0, 1, 3, 4, 6, 7, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[4], q[6], q[7], q[5];
// UNMAPPED c6x [0, 1, 5, 7, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[5], q[7], q[8], q[9], q[4];
// UNMAPPED c6x [0, 1, 5, 7, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[5], q[7], q[8], q[9], q[3];
// UNMAPPED c7x [0, 1, 3, 4, 5, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[4], q[5], q[7], q[9], q[8];
// UNMAPPED c6x [0, 1, 3, 4, 5, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[4], q[5], q[9], q[7];
// UNMAPPED c5x [0, 1, 5, 7, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[5], q[7], q[8], q[2];
// UNMAPPED c5x [0, 1, 2, 5, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[5], q[7], q[8];
// UNMAPPED c5x [0, 1, 5, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[5], q[7], q[9], q[8];
// UNMAPPED c5x [0, 1, 5, 7, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[5], q[7], q[9], q[4];
// UNMAPPED c5x [0, 1, 5, 7, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[5], q[7], q[9], q[3];
// UNMAPPED c7x [0, 1, 3, 4, 5, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[4], q[5], q[7], q[8], q[9];
// UNMAPPED c6x [0, 1, 3, 4, 5, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[4], q[5], q[8], q[7];
// UNMAPPED c5x [0, 1, 3, 4, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[4], q[8], q[5];
// UNMAPPED c4x [0, 1, 5, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[5], q[7], q[9];
// UNMAPPED c4x [0, 1, 5, 7, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[5], q[7], q[4];
// UNMAPPED c4x [0, 1, 5, 7, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[5], q[7], q[3];
// UNMAPPED c5x [0, 1, 5, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[5], q[8], q[9], q[6];
// UNMAPPED c5x [0, 1, 5, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[5], q[8], q[9], q[4];
// UNMAPPED c5x [0, 1, 5, 8, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[5], q[8], q[9], q[2];
// UNMAPPED c7x [0, 1, 2, 4, 5, 6, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[4], q[5], q[6], q[8], q[9];
// UNMAPPED c6x [0, 1, 2, 4, 6, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[6], q[8], q[5];
// UNMAPPED c4x [0, 1, 5, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[5], q[8], q[9];
// UNMAPPED c4x [0, 1, 5, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[5], q[8], q[6];
// UNMAPPED c4x [0, 1, 5, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[5], q[8], q[4];
// UNMAPPED c4x [0, 1, 5, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[5], q[9], q[7];
// UNMAPPED c4x [0, 1, 5, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[5], q[9], q[6];
// UNMAPPED c4x [0, 1, 5, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[5], q[9], q[4];
// UNMAPPED c4x [0, 1, 5, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[5], q[9], q[3];
// UNMAPPED c4x [0, 1, 5, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[5], q[9], q[2];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 7, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[9], q[5];
// UNMAPPED c3x [0, 1, 5, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[5], q[8];
// UNMAPPED c3x [0, 1, 5, 4]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[5], q[4];
// UNMAPPED c3x [0, 1, 5, 2]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[5], q[2];
// UNMAPPED c5x [0, 1, 2, 4, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[4], q[8], q[5];
// UNMAPPED c6x [0, 1, 6, 7, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[6], q[7], q[8], q[9], q[5];
// UNMAPPED c6x [0, 1, 6, 7, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[6], q[7], q[8], q[9], q[4];
// UNMAPPED c6x [0, 1, 6, 7, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[6], q[7], q[8], q[9], q[3];
// UNMAPPED c8x [0, 1, 3, 4, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[3], q[4], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c7x [0, 1, 3, 4, 5, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[4], q[5], q[6], q[7], q[8];
// UNMAPPED c6x [0, 1, 3, 4, 5, 6, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[4], q[5], q[6], q[7];
// UNMAPPED c5x [0, 1, 3, 4, 5, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[4], q[5], q[6];
// UNMAPPED c5x [0, 1, 6, 7, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[6], q[7], q[8], q[5];
// UNMAPPED c5x [0, 1, 6, 7, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[6], q[7], q[8], q[2];
// UNMAPPED c6x [0, 1, 2, 5, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[5], q[6], q[8], q[7];
// UNMAPPED c5x [0, 1, 2, 5, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[5], q[8], q[6];
// UNMAPPED c5x [0, 1, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[6], q[7], q[9], q[8];
// UNMAPPED c5x [0, 1, 6, 7, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[6], q[7], q[9], q[5];
// UNMAPPED c5x [0, 1, 6, 7, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[6], q[7], q[9], q[4];
// UNMAPPED c4x [0, 1, 6, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[6], q[7], q[9];
// UNMAPPED c4x [0, 1, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[6], q[7], q[8];
// UNMAPPED c4x [0, 1, 6, 7, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[6], q[7], q[4];
// UNMAPPED c4x [0, 1, 6, 7, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[6], q[7], q[3];
// UNMAPPED c7x [0, 1, 3, 4, 6, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[4], q[6], q[8], q[9], q[7];
// UNMAPPED c5x [0, 1, 6, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[6], q[8], q[9], q[7];
// UNMAPPED c5x [0, 1, 6, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[6], q[8], q[9], q[4];
// UNMAPPED c5x [0, 1, 6, 8, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[6], q[8], q[9], q[2];
// UNMAPPED c7x [0, 1, 2, 4, 7, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[4], q[7], q[8], q[9], q[6];
// UNMAPPED c4x [0, 1, 6, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[6], q[8], q[9];
// UNMAPPED c4x [0, 1, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[6], q[8], q[7];
// UNMAPPED c4x [0, 1, 6, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[6], q[8], q[3];
// UNMAPPED c4x [0, 1, 6, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[6], q[8], q[2];
// UNMAPPED c7x [0, 1, 2, 3, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[6], q[7], q[9], q[8];
// UNMAPPED c4x [0, 1, 6, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[6], q[9], q[8];
// UNMAPPED c4x [0, 1, 6, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[6], q[9], q[7];
// UNMAPPED c4x [0, 1, 6, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[6], q[9], q[5];
// UNMAPPED c4x [0, 1, 6, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[6], q[9], q[3];
// UNMAPPED c7x [0, 1, 3, 5, 7, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[5], q[7], q[8], q[9], q[6];
// UNMAPPED c3x [0, 1, 6, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[6], q[9];
// UNMAPPED c3x [0, 1, 6, 5]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[6], q[5];
// UNMAPPED c3x [0, 1, 6, 3]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[6], q[3];
// UNMAPPED c5x [0, 1, 7, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[7], q[8], q[9], q[6];
// UNMAPPED c5x [0, 1, 7, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[7], q[8], q[9], q[5];
// UNMAPPED c4x [0, 1, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[7], q[8], q[9];
// UNMAPPED c4x [0, 1, 7, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[7], q[8], q[5];
// UNMAPPED c4x [0, 1, 7, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[7], q[8], q[2];
// UNMAPPED c6x [0, 1, 2, 5, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[5], q[7], q[9], q[8];
// UNMAPPED c4x [0, 1, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[7], q[9], q[8];
// UNMAPPED c4x [0, 1, 7, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[7], q[9], q[3];
// UNMAPPED c3x [0, 1, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[7], q[9];
// UNMAPPED c3x [0, 1, 7, 6]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[7], q[6];
// UNMAPPED c3x [0, 1, 7, 5]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[7], q[5];
// UNMAPPED c3x [0, 1, 7, 4]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[7], q[4];
// UNMAPPED c4x [0, 1, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[8], q[9], q[7];
// UNMAPPED c4x [0, 1, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[8], q[9], q[6];
// UNMAPPED c4x [0, 1, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[8], q[9], q[5];
// UNMAPPED c4x [0, 1, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[8], q[9], q[4];
// UNMAPPED c7x [0, 1, 4, 5, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[4], q[5], q[6], q[7], q[9], q[8];
// UNMAPPED c3x [0, 1, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[8], q[7];
// UNMAPPED c3x [0, 1, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[8], q[5];
// UNMAPPED c3x [0, 1, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[8], q[3];
// UNMAPPED c3x [0, 1, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[8], q[2];
// UNMAPPED c3x [0, 1, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[9], q[8];
// UNMAPPED c3x [0, 1, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[9], q[7];
// UNMAPPED c3x [0, 1, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[9], q[6];
// UNMAPPED c3x [0, 1, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[9], q[5];
// UNMAPPED c3x [0, 1, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[9], q[4];
// UNMAPPED c3x [0, 1, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[9], q[2];
// UNMAPPED c8x [0, 1, 2, 4, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[4], q[5], q[6], q[7], q[8], q[9];
ccx q[0], q[1], q[8];
ccx q[0], q[1], q[6];
ccx q[0], q[1], q[4];
ccx q[0], q[1], q[2];
// UNMAPPED c9x [0, 2, 3, 4, 5, 6, 7, 8, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[1];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 7, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[9], q[6];
// UNMAPPED c7x [0, 1, 2, 4, 5, 7, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[4], q[5], q[7], q[9], q[3];
// UNMAPPED c6x [0, 1, 4, 5, 7, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[4], q[5], q[7], q[9], q[2];
// UNMAPPED c8x [0, 2, 3, 4, 5, 6, 7, 8, 1]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[1];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[7];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[5];
// UNMAPPED c6x [0, 1, 2, 3, 6, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[6], q[8], q[4];
// UNMAPPED c5x [0, 1, 2, 6, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[6], q[8], q[3];
// UNMAPPED c4x [0, 1, 6, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[6], q[8], q[2];
// UNMAPPED c8x [0, 2, 3, 4, 5, 6, 7, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[1];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[7];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[9], q[6];
// UNMAPPED c6x [0, 1, 2, 3, 5, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[9], q[4];
// UNMAPPED c5x [0, 1, 2, 5, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[5], q[9], q[3];
// UNMAPPED c7x [0, 2, 3, 4, 5, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[5], q[6], q[7], q[8];
// UNMAPPED c7x [0, 2, 3, 4, 5, 6, 7, 1]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[5], q[6], q[7], q[1];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[7];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[5];
// UNMAPPED c6x [0, 1, 2, 4, 6, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[6], q[8], q[3];
// UNMAPPED c8x [0, 2, 3, 4, 5, 6, 8, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[1];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[6];
// UNMAPPED c6x [0, 1, 2, 3, 5, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[8], q[4];
// UNMAPPED c7x [0, 2, 3, 4, 5, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[5], q[6], q[8], q[7];
// UNMAPPED c7x [0, 2, 3, 4, 5, 6, 8, 1]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[5], q[6], q[8], q[1];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 7, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[5];
// UNMAPPED c7x [0, 1, 2, 4, 6, 7, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[4], q[6], q[7], q[8], q[3];
// UNMAPPED c7x [0, 2, 3, 4, 5, 6, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[5], q[6], q[9], q[1];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 6, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9];
// UNMAPPED c6x [0, 1, 2, 4, 5, 6, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[5], q[6], q[3];
// UNMAPPED c6x [0, 2, 3, 4, 5, 6, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[5], q[6], q[9];
// UNMAPPED c6x [0, 2, 3, 4, 5, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[5], q[6], q[8];
// UNMAPPED c6x [0, 2, 3, 4, 5, 6, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[5], q[6], q[7];
// UNMAPPED c6x [0, 2, 3, 4, 5, 6, 1]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[5], q[6], q[1];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[6];
// UNMAPPED c8x [0, 1, 2, 3, 4, 7, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[9], q[5];
// UNMAPPED c7x [0, 1, 2, 4, 7, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[4], q[7], q[8], q[9], q[3];
// UNMAPPED c8x [0, 2, 3, 4, 5, 7, 8, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[1];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[9], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 4, 7, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[7], q[9], q[5];
// UNMAPPED c7x [0, 2, 3, 4, 5, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[5], q[7], q[8], q[9];
// UNMAPPED c7x [0, 2, 3, 4, 5, 7, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[5], q[7], q[8], q[6];
// UNMAPPED c7x [0, 2, 3, 4, 5, 7, 8, 1]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[5], q[7], q[8], q[1];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[7];
// UNMAPPED c7x [0, 2, 3, 4, 5, 7, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[5], q[7], q[9], q[1];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[9], q[7];
// UNMAPPED c6x [0, 1, 2, 3, 4, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[9], q[5];
// UNMAPPED c5x [0, 1, 2, 3, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[9], q[4];
// UNMAPPED c4x [0, 1, 3, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[3], q[9], q[2];
// UNMAPPED c6x [0, 2, 3, 4, 5, 7, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[5], q[7], q[6];
// UNMAPPED c6x [0, 2, 3, 4, 5, 7, 1]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[5], q[7], q[1];
// UNMAPPED c7x [0, 2, 3, 4, 5, 8, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[5], q[8], q[9], q[1];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[9];
// UNMAPPED c6x [0, 1, 2, 3, 4, 5, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[5], q[8];
// UNMAPPED c5x [0, 1, 2, 4, 5, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[4], q[5], q[3];
// UNMAPPED c6x [0, 2, 3, 4, 5, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[5], q[8], q[9];
// UNMAPPED c6x [0, 2, 3, 4, 5, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[5], q[8], q[7];
// UNMAPPED c6x [0, 2, 3, 4, 5, 8, 1]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[5], q[8], q[1];
// UNMAPPED c8x [0, 1, 2, 3, 4, 7, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[9], q[5];
// UNMAPPED c7x [0, 1, 2, 3, 7, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[7], q[8], q[9], q[4];
// UNMAPPED c6x [0, 2, 3, 4, 5, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[5], q[9], q[6];
// UNMAPPED c6x [0, 2, 3, 4, 5, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[5], q[9], q[1];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 6, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9];
// UNMAPPED c6x [0, 1, 2, 3, 5, 6, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[6], q[4];
// UNMAPPED c5x [0, 2, 3, 4, 5, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[4], q[5], q[7];
// UNMAPPED c5x [0, 2, 3, 4, 5, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[4], q[5], q[6];
// UNMAPPED c5x [0, 2, 3, 4, 5, 1]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[4], q[5], q[1];
// UNMAPPED c7x [0, 1, 2, 3, 5, 6, 7, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[4];
// UNMAPPED c8x [0, 2, 3, 4, 6, 7, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[5];
// UNMAPPED c8x [0, 2, 3, 4, 6, 7, 8, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[1];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 7, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[6];
// UNMAPPED c6x [0, 1, 2, 3, 5, 7, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[7], q[4];
// UNMAPPED c7x [0, 2, 3, 4, 6, 7, 8, 1]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[6], q[7], q[8], q[1];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8];
// UNMAPPED c6x [0, 1, 2, 3, 4, 7, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[7], q[6];
// UNMAPPED c5x [0, 1, 3, 4, 7, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[4], q[7], q[2];
// UNMAPPED c7x [0, 2, 3, 4, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[6], q[7], q[9], q[8];
// UNMAPPED c7x [0, 2, 3, 4, 6, 7, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[6], q[7], q[9], q[1];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[7];
// UNMAPPED c6x [0, 1, 3, 4, 6, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[4], q[6], q[8], q[2];
// UNMAPPED c6x [0, 2, 3, 4, 6, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[6], q[7], q[9];
// UNMAPPED c6x [0, 2, 3, 4, 6, 7, 1]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[6], q[7], q[1];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[9], q[7];
// UNMAPPED c6x [0, 1, 2, 4, 6, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[6], q[9], q[3];
// UNMAPPED c7x [0, 2, 3, 4, 6, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[6], q[8], q[9], q[7];
// UNMAPPED c7x [0, 2, 3, 4, 6, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[6], q[8], q[9], q[5];
// UNMAPPED c7x [0, 2, 3, 4, 6, 8, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[6], q[8], q[9], q[1];
// UNMAPPED c6x [0, 2, 3, 4, 6, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[6], q[8], q[9];
// UNMAPPED c6x [0, 2, 3, 4, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[6], q[8], q[7];
// UNMAPPED c6x [0, 2, 3, 4, 6, 8, 1]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[6], q[8], q[1];
// UNMAPPED c8x [0, 1, 2, 4, 6, 7, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[4], q[6], q[7], q[8], q[9], q[3];
// UNMAPPED c6x [0, 2, 3, 4, 6, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[6], q[9], q[8];
// UNMAPPED c6x [0, 2, 3, 4, 6, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[6], q[9], q[5];
// UNMAPPED c6x [0, 2, 3, 4, 6, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[6], q[9], q[1];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 5, 6, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[4];
// UNMAPPED c5x [0, 2, 3, 4, 6, 1]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[4], q[6], q[1];
// UNMAPPED c7x [0, 2, 3, 4, 7, 8, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[7], q[8], q[9], q[1];
// UNMAPPED c7x [0, 1, 2, 3, 4, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[9];
// UNMAPPED c6x [0, 1, 2, 3, 4, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[7], q[8];
// UNMAPPED c5x [0, 1, 2, 3, 4, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[4], q[7];
// UNMAPPED c4x [0, 1, 2, 3, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[3], q[4];
// UNMAPPED c6x [0, 2, 3, 4, 7, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[7], q[8], q[6];
// UNMAPPED c6x [0, 2, 3, 4, 7, 8, 1]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[7], q[8], q[1];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8];
// UNMAPPED c6x [0, 1, 2, 3, 6, 7, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[6], q[7], q[4];
// UNMAPPED c5x [0, 1, 3, 6, 7, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[6], q[7], q[2];
// UNMAPPED c6x [0, 2, 3, 4, 7, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[7], q[9], q[6];
// UNMAPPED c6x [0, 2, 3, 4, 7, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[7], q[9], q[1];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[9];
// UNMAPPED c6x [0, 1, 2, 3, 4, 6, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[6], q[7];
// UNMAPPED c5x [0, 1, 2, 3, 6, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[6], q[4];
// UNMAPPED c4x [0, 1, 2, 6, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[6], q[3];
// UNMAPPED c5x [0, 2, 3, 4, 7, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[4], q[7], q[5];
// UNMAPPED c6x [0, 2, 3, 4, 8, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[8], q[9], q[1];
// UNMAPPED c6x [0, 1, 2, 3, 4, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[8], q[9];
// UNMAPPED c5x [0, 1, 2, 3, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[4], q[8];
// UNMAPPED c4x [0, 1, 2, 3, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[3], q[4];
// UNMAPPED c3x [0, 1, 2, 3]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[2], q[3];
// UNMAPPED c5x [0, 2, 3, 4, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[4], q[8], q[9];
// UNMAPPED c5x [0, 2, 3, 4, 8, 1]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[4], q[8], q[1];
// UNMAPPED c6x [0, 1, 2, 3, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[8], q[9], q[4];
// UNMAPPED c5x [0, 1, 2, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[8], q[9], q[3];
// UNMAPPED c4x [0, 1, 8, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[8], q[9], q[2];
// UNMAPPED c5x [0, 2, 3, 4, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[4], q[9], q[8];
// UNMAPPED c5x [0, 2, 3, 4, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[4], q[9], q[7];
// UNMAPPED c5x [0, 2, 3, 4, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[4], q[9], q[5];
// UNMAPPED c5x [0, 2, 3, 4, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[4], q[9], q[1];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9];
// UNMAPPED c7x [0, 1, 2, 4, 5, 7, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[4], q[5], q[7], q[8], q[3];
// UNMAPPED c6x [0, 1, 4, 5, 7, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[4], q[5], q[7], q[8], q[2];
// UNMAPPED c4x [0, 2, 3, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[3], q[4], q[9];
// UNMAPPED c4x [0, 2, 3, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[3], q[4], q[8];
// UNMAPPED c8x [0, 2, 3, 5, 6, 7, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[5], q[6], q[7], q[8], q[9], q[4];
// UNMAPPED c8x [0, 2, 3, 5, 6, 7, 8, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[5], q[6], q[7], q[8], q[9], q[1];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 7, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[9], q[6];
// UNMAPPED c7x [0, 1, 3, 4, 5, 7, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[4], q[5], q[7], q[9], q[2];
// UNMAPPED c7x [0, 2, 3, 5, 6, 7, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[5], q[6], q[7], q[8], q[4];
// UNMAPPED c7x [0, 2, 3, 5, 6, 7, 8, 1]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[5], q[6], q[7], q[8], q[1];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 7, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[6];
// UNMAPPED c6x [0, 1, 2, 4, 5, 7, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[5], q[7], q[3];
// UNMAPPED c5x [0, 1, 4, 5, 7, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[4], q[5], q[7], q[2];
// UNMAPPED c7x [0, 2, 3, 5, 6, 7, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[5], q[6], q[7], q[9], q[4];
// UNMAPPED c7x [0, 2, 3, 5, 6, 7, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[5], q[6], q[7], q[9], q[1];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 6, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7];
// UNMAPPED c6x [0, 1, 2, 3, 4, 6, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[6], q[5];
// UNMAPPED c5x [0, 1, 2, 4, 6, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[4], q[6], q[3];
// UNMAPPED c6x [0, 2, 3, 5, 6, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[5], q[6], q[7], q[9];
// UNMAPPED c6x [0, 2, 3, 5, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[5], q[6], q[7], q[8];
// UNMAPPED c6x [0, 2, 3, 5, 6, 7, 1]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[5], q[6], q[7], q[1];
// UNMAPPED c8x [0, 1, 2, 3, 5, 7, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[9], q[6];
// UNMAPPED c7x [0, 1, 2, 3, 7, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[7], q[8], q[9], q[5];
// UNMAPPED c6x [0, 1, 2, 7, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[7], q[8], q[9], q[3];
// UNMAPPED c7x [0, 2, 3, 5, 6, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[5], q[6], q[8], q[9], q[7];
// UNMAPPED c6x [0, 2, 3, 5, 6, 8, 1]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[5], q[6], q[8], q[1];
// UNMAPPED c6x [0, 1, 2, 3, 5, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[6], q[8];
// UNMAPPED c5x [0, 1, 2, 3, 5, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[5], q[6];
// UNMAPPED c4x [0, 1, 2, 3, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[3], q[5];
// UNMAPPED c6x [0, 2, 3, 5, 6, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[5], q[6], q[9], q[8];
// UNMAPPED c6x [0, 2, 3, 5, 6, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[5], q[6], q[9], q[7];
// UNMAPPED c6x [0, 2, 3, 5, 6, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[5], q[6], q[9], q[1];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c7x [0, 1, 2, 5, 6, 7, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[5], q[6], q[7], q[8], q[3];
// UNMAPPED c5x [0, 2, 3, 5, 6, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[5], q[6], q[9];
// UNMAPPED c5x [0, 2, 3, 5, 6, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[5], q[6], q[7];
// UNMAPPED c5x [0, 2, 3, 5, 6, 1]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[5], q[6], q[1];
// UNMAPPED c7x [0, 1, 2, 3, 6, 7, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[6], q[7], q[9], q[5];
// UNMAPPED c7x [0, 2, 3, 5, 7, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[5], q[7], q[8], q[9], q[6];
// UNMAPPED c7x [0, 2, 3, 5, 7, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[5], q[7], q[8], q[9], q[4];
// UNMAPPED c7x [0, 2, 3, 5, 7, 8, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[5], q[7], q[8], q[9], q[1];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c8x [0, 1, 2, 4, 5, 6, 7, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[4], q[5], q[6], q[7], q[8], q[3];
// UNMAPPED c7x [0, 1, 4, 5, 6, 7, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[4], q[5], q[6], q[7], q[8], q[2];
// UNMAPPED c6x [0, 2, 3, 5, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[5], q[7], q[8], q[9];
// UNMAPPED c6x [0, 2, 3, 5, 7, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[5], q[7], q[8], q[4];
// UNMAPPED c6x [0, 2, 3, 5, 7, 8, 1]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[5], q[7], q[8], q[1];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[9], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[9], q[7];
// UNMAPPED c6x [0, 1, 2, 4, 5, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[5], q[9], q[3];
// UNMAPPED c5x [0, 1, 4, 5, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[4], q[5], q[9], q[2];
// UNMAPPED c6x [0, 2, 3, 5, 7, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[5], q[7], q[9], q[6];
// UNMAPPED c6x [0, 2, 3, 5, 7, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[5], q[7], q[9], q[4];
// UNMAPPED c6x [0, 2, 3, 5, 7, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[5], q[7], q[9], q[1];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 7, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[9], q[5];
// UNMAPPED c7x [0, 1, 2, 4, 6, 7, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[4], q[6], q[7], q[9], q[3];
// UNMAPPED c6x [0, 1, 4, 6, 7, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[4], q[6], q[7], q[9], q[2];
// UNMAPPED c5x [0, 2, 3, 5, 7, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[5], q[7], q[6];
// UNMAPPED c5x [0, 2, 3, 5, 7, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[5], q[7], q[4];
// UNMAPPED c6x [0, 2, 3, 4, 6, 7, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[6], q[7], q[5];
// UNMAPPED c6x [0, 2, 3, 5, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[5], q[8], q[9], q[4];
// UNMAPPED c6x [0, 2, 3, 5, 8, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[5], q[8], q[9], q[1];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[9];
// UNMAPPED c6x [0, 1, 2, 3, 4, 5, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[5], q[8];
// UNMAPPED c5x [0, 1, 2, 4, 5, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[4], q[5], q[3];
// UNMAPPED c4x [0, 1, 4, 5, 2]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[4], q[5], q[2];
// UNMAPPED c5x [0, 2, 3, 5, 8, 1]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[5], q[8], q[1];
// UNMAPPED c5x [0, 1, 2, 3, 5, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[5], q[8];
// UNMAPPED c4x [0, 1, 2, 3, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[3], q[5];
// UNMAPPED c3x [0, 1, 3, 2]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[3], q[2];
// UNMAPPED c5x [0, 2, 3, 5, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[5], q[9], q[8];
// UNMAPPED c5x [0, 2, 3, 5, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[5], q[9], q[4];
// UNMAPPED c5x [0, 2, 3, 5, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[5], q[9], q[1];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[9];
// UNMAPPED c6x [0, 1, 2, 3, 4, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[8], q[5];
// UNMAPPED c4x [0, 2, 3, 5, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[3], q[5], q[7];
// UNMAPPED c4x [0, 2, 3, 5, 6]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[3], q[5], q[6];
// UNMAPPED c4x [0, 2, 3, 5, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[3], q[5], q[4];
// UNMAPPED c4x [0, 2, 3, 5, 1]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[3], q[5], q[1];
// UNMAPPED c7x [0, 1, 2, 4, 5, 6, 7, 3]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[4], q[5], q[6], q[7], q[3];
// UNMAPPED c7x [0, 2, 3, 6, 7, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[6], q[7], q[8], q[9], q[5];
// UNMAPPED c7x [0, 2, 3, 6, 7, 8, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[6], q[7], q[8], q[9], q[1];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 5, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8];
// UNMAPPED c6x [0, 1, 3, 5, 6, 7, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[5], q[6], q[7], q[2];
// UNMAPPED c6x [0, 2, 3, 6, 7, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[6], q[7], q[8], q[5];
// UNMAPPED c6x [0, 2, 3, 5, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[5], q[6], q[7], q[8];
// UNMAPPED c5x [0, 2, 3, 5, 6, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[5], q[6], q[7];
// UNMAPPED c6x [0, 2, 3, 6, 7, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[6], q[7], q[9], q[5];
// UNMAPPED c6x [0, 2, 3, 6, 7, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[6], q[7], q[9], q[4];
// UNMAPPED c6x [0, 2, 3, 6, 7, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[6], q[7], q[9], q[1];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 7, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[9], q[6];
// UNMAPPED c7x [0, 1, 3, 4, 5, 7, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[4], q[5], q[7], q[9], q[2];
// UNMAPPED c5x [0, 2, 3, 6, 7, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[6], q[7], q[4];
// UNMAPPED c5x [0, 2, 3, 6, 7, 1]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[6], q[7], q[1];
// UNMAPPED c6x [0, 1, 2, 3, 4, 6, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[6], q[7];
// UNMAPPED c5x [0, 1, 2, 4, 6, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[4], q[6], q[3];
// UNMAPPED c4x [0, 1, 4, 6, 2]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[4], q[6], q[2];
// UNMAPPED c6x [0, 2, 3, 6, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[6], q[8], q[9], q[4];
// UNMAPPED c6x [0, 2, 3, 6, 8, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[6], q[8], q[9], q[1];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[9];
// UNMAPPED c6x [0, 1, 2, 3, 4, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[6], q[8];
// UNMAPPED c5x [0, 1, 2, 4, 6, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[4], q[6], q[3];
// UNMAPPED c4x [0, 1, 4, 6, 2]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[4], q[6], q[2];
// UNMAPPED c5x [0, 2, 3, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[6], q[8], q[7];
// UNMAPPED c5x [0, 2, 3, 6, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[6], q[8], q[5];
// UNMAPPED c5x [0, 2, 3, 6, 8, 1]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[6], q[8], q[1];
// UNMAPPED c7x [0, 1, 2, 3, 5, 7, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[6];
// UNMAPPED c6x [0, 1, 2, 5, 7, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[5], q[7], q[8], q[3];
// UNMAPPED c5x [0, 2, 3, 6, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[6], q[9], q[8];
// UNMAPPED c5x [0, 2, 3, 6, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[6], q[9], q[5];
// UNMAPPED c5x [0, 2, 3, 6, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[6], q[9], q[4];
// UNMAPPED c7x [0, 2, 3, 4, 5, 6, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[5], q[6], q[8], q[9];
// UNMAPPED c4x [0, 2, 3, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[3], q[6], q[8];
// UNMAPPED c4x [0, 2, 3, 6, 1]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[3], q[6], q[1];
// UNMAPPED c6x [0, 2, 3, 7, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[7], q[8], q[9], q[6];
// UNMAPPED c6x [0, 2, 3, 7, 8, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[7], q[8], q[9], q[1];
// UNMAPPED c7x [0, 1, 2, 3, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[6], q[7], q[9], q[8];
// UNMAPPED c6x [0, 1, 2, 6, 7, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[6], q[7], q[9], q[3];
// UNMAPPED c5x [0, 1, 6, 7, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[6], q[7], q[9], q[2];
// UNMAPPED c5x [0, 2, 3, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[7], q[8], q[9];
// UNMAPPED c5x [0, 2, 3, 7, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[7], q[8], q[5];
// UNMAPPED c5x [0, 2, 3, 7, 8, 1]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[7], q[8], q[1];
// UNMAPPED c7x [0, 1, 2, 3, 5, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[8], q[9], q[7];
// UNMAPPED c6x [0, 1, 3, 5, 8, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[5], q[8], q[9], q[2];
// UNMAPPED c5x [0, 2, 3, 7, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[7], q[9], q[4];
// UNMAPPED c5x [0, 2, 3, 4, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[4], q[9], q[7];
// UNMAPPED c4x [0, 2, 3, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[3], q[7], q[9];
// UNMAPPED c4x [0, 2, 3, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[3], q[7], q[8];
// UNMAPPED c4x [0, 2, 3, 7, 6]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[3], q[7], q[6];
// UNMAPPED c4x [0, 2, 3, 7, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[3], q[7], q[4];
// UNMAPPED c4x [0, 2, 3, 7, 1]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[3], q[7], q[1];
// UNMAPPED c5x [0, 2, 3, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[8], q[9], q[6];
// UNMAPPED c5x [0, 2, 3, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[8], q[9], q[5];
// UNMAPPED c5x [0, 2, 3, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[8], q[9], q[4];
// UNMAPPED c5x [0, 2, 3, 8, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[8], q[9], q[1];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8];
// UNMAPPED c6x [0, 1, 2, 4, 5, 6, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[5], q[6], q[3];
// UNMAPPED c5x [0, 1, 4, 5, 6, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[4], q[5], q[6], q[2];
// UNMAPPED c4x [0, 2, 3, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[3], q[8], q[7];
// UNMAPPED c4x [0, 2, 3, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[3], q[8], q[5];
// UNMAPPED c4x [0, 2, 3, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[3], q[8], q[4];
// UNMAPPED c4x [0, 2, 3, 8, 1]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[3], q[8], q[1];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8];
// UNMAPPED c6x [0, 1, 3, 4, 5, 7, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[4], q[5], q[7], q[2];
// UNMAPPED c4x [0, 2, 3, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[3], q[9], q[6];
// UNMAPPED c4x [0, 2, 3, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[3], q[9], q[1];
// UNMAPPED c3x [0, 2, 3, 7]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[2], q[3], q[7];
// UNMAPPED c3x [0, 2, 3, 1]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[2], q[3], q[1];
// UNMAPPED c8x [0, 2, 4, 5, 6, 7, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[4], q[5], q[6], q[7], q[8], q[9], q[3];
// UNMAPPED c8x [0, 2, 4, 5, 6, 7, 8, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[4], q[5], q[6], q[7], q[8], q[9], q[1];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 5, 6, 7, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[4];
// UNMAPPED c7x [0, 2, 4, 5, 6, 7, 8, 1]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[4], q[5], q[6], q[7], q[8], q[1];
// UNMAPPED c7x [0, 1, 2, 4, 5, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[4], q[5], q[6], q[7], q[8];
// UNMAPPED c6x [0, 1, 2, 4, 5, 6, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[5], q[6], q[7];
// UNMAPPED c5x [0, 1, 4, 5, 6, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[4], q[5], q[6], q[2];
// UNMAPPED c7x [0, 2, 4, 5, 6, 7, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[4], q[5], q[6], q[7], q[9], q[3];
// UNMAPPED c7x [0, 2, 3, 4, 5, 6, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[5], q[6], q[7], q[9];
// UNMAPPED c6x [0, 2, 3, 4, 6, 7, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[6], q[7], q[5];
// UNMAPPED c5x [0, 2, 3, 6, 7, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[6], q[7], q[4];
// UNMAPPED c6x [0, 2, 4, 5, 6, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[4], q[5], q[6], q[7], q[9];
// UNMAPPED c6x [0, 2, 4, 5, 6, 7, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[4], q[5], q[6], q[7], q[3];
// UNMAPPED c7x [0, 2, 3, 4, 5, 6, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[5], q[6], q[9], q[7];
// UNMAPPED c6x [0, 2, 3, 4, 5, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[5], q[9], q[6];
// UNMAPPED c5x [0, 2, 3, 4, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[4], q[9], q[5];
// UNMAPPED c4x [0, 2, 3, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[3], q[9], q[4];
// UNMAPPED c7x [0, 2, 4, 5, 6, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[4], q[5], q[6], q[8], q[9], q[3];
// UNMAPPED c7x [0, 2, 3, 4, 5, 6, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[5], q[6], q[9], q[8];
// UNMAPPED c6x [0, 2, 3, 4, 5, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[5], q[9], q[6];
// UNMAPPED c6x [0, 2, 4, 5, 6, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[4], q[5], q[6], q[8], q[3];
// UNMAPPED c6x [0, 2, 4, 5, 6, 8, 1]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[4], q[5], q[6], q[8], q[1];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8];
// UNMAPPED c6x [0, 1, 2, 3, 4, 5, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[5], q[6];
// UNMAPPED c5x [0, 1, 2, 3, 4, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[4], q[5];
// UNMAPPED c6x [0, 2, 4, 5, 6, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[4], q[5], q[6], q[9], q[8];
// UNMAPPED c6x [0, 2, 4, 5, 6, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[4], q[5], q[6], q[9], q[7];
// UNMAPPED c6x [0, 2, 4, 5, 6, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[4], q[5], q[6], q[9], q[3];
// UNMAPPED c6x [0, 2, 4, 5, 6, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[4], q[5], q[6], q[9], q[1];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 7, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[6];
// UNMAPPED c7x [0, 1, 2, 3, 4, 7, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[5];
// UNMAPPED c6x [0, 1, 3, 4, 7, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[4], q[7], q[8], q[2];
// UNMAPPED c5x [0, 2, 4, 5, 6, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[4], q[5], q[6], q[9];
// UNMAPPED c5x [0, 2, 4, 5, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[4], q[5], q[6], q[8];
// UNMAPPED c5x [0, 2, 4, 5, 6, 1]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[4], q[5], q[6], q[1];
// UNMAPPED c7x [0, 1, 2, 4, 5, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[4], q[5], q[8], q[9], q[6];
// UNMAPPED c6x [0, 1, 2, 4, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[8], q[9], q[5];
// UNMAPPED c5x [0, 1, 2, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[8], q[9], q[4];
// UNMAPPED c7x [0, 2, 4, 5, 7, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[4], q[5], q[7], q[8], q[9], q[6];
// UNMAPPED c7x [0, 2, 4, 5, 7, 8, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[4], q[5], q[7], q[8], q[9], q[1];
// UNMAPPED c8x [0, 1, 2, 4, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[4], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c7x [0, 1, 2, 4, 5, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[4], q[5], q[6], q[7], q[8];
// UNMAPPED c6x [0, 1, 2, 4, 5, 6, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[5], q[6], q[7];
// UNMAPPED c5x [0, 1, 2, 4, 6, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[4], q[6], q[5];
// UNMAPPED c4x [0, 1, 2, 6, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[6], q[4];
// UNMAPPED c6x [0, 2, 4, 5, 7, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[4], q[5], q[7], q[8], q[6];
// UNMAPPED c6x [0, 2, 4, 5, 7, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[4], q[5], q[7], q[8], q[3];
// UNMAPPED c6x [0, 2, 4, 5, 7, 8, 1]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[4], q[5], q[7], q[8], q[1];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 7, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[5];
// UNMAPPED c6x [0, 1, 3, 4, 6, 7, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[4], q[6], q[7], q[2];
// UNMAPPED c6x [0, 2, 4, 5, 7, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[4], q[5], q[7], q[9], q[6];
// UNMAPPED c6x [0, 2, 4, 5, 7, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[4], q[5], q[7], q[9], q[3];
// UNMAPPED c6x [0, 2, 4, 5, 7, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[4], q[5], q[7], q[9], q[1];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 7, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[9], q[5];
// UNMAPPED c7x [0, 1, 2, 3, 6, 7, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[6], q[7], q[9], q[4];
// UNMAPPED c6x [0, 1, 3, 6, 7, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[6], q[7], q[9], q[2];
// UNMAPPED c5x [0, 2, 4, 5, 7, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[4], q[5], q[7], q[6];
// UNMAPPED c5x [0, 2, 4, 5, 7, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[4], q[5], q[7], q[3];
// UNMAPPED c6x [0, 2, 3, 4, 5, 6, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[5], q[6], q[7];
// UNMAPPED c6x [0, 2, 4, 5, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[4], q[5], q[8], q[9], q[7];
// UNMAPPED c6x [0, 2, 4, 5, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[4], q[5], q[8], q[9], q[3];
// UNMAPPED c7x [0, 2, 3, 4, 5, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[5], q[7], q[8], q[9];
// UNMAPPED c6x [0, 2, 3, 4, 5, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[5], q[7], q[8];
// UNMAPPED c5x [0, 2, 4, 5, 8, 1]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[4], q[5], q[8], q[1];
// UNMAPPED c5x [0, 1, 2, 4, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[4], q[8], q[5];
// UNMAPPED c4x [0, 1, 2, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[8], q[4];
// UNMAPPED c5x [0, 2, 4, 5, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[4], q[5], q[9], q[3];
// UNMAPPED c5x [0, 2, 4, 5, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[4], q[5], q[9], q[1];
// UNMAPPED c6x [0, 1, 2, 3, 4, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[9], q[5];
// UNMAPPED c4x [0, 2, 4, 5, 6]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[4], q[5], q[6];
// UNMAPPED c7x [0, 2, 4, 6, 7, 8, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[4], q[6], q[7], q[8], q[9], q[1];
// UNMAPPED c7x [0, 1, 2, 4, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[4], q[6], q[7], q[9], q[8];
// UNMAPPED c6x [0, 1, 4, 6, 7, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[4], q[6], q[7], q[9], q[2];
// UNMAPPED c6x [0, 2, 4, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[4], q[6], q[7], q[8], q[9];
// UNMAPPED c6x [0, 2, 4, 6, 7, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[4], q[6], q[7], q[8], q[5];
// UNMAPPED c6x [0, 2, 4, 6, 7, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[4], q[6], q[7], q[8], q[3];
// UNMAPPED c6x [0, 2, 4, 6, 7, 8, 1]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[4], q[6], q[7], q[8], q[1];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[8];
// UNMAPPED c8x [0, 1, 3, 4, 5, 6, 7, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[3], q[4], q[5], q[6], q[7], q[9], q[2];
// UNMAPPED c6x [0, 2, 4, 6, 7, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[4], q[6], q[7], q[9], q[5];
// UNMAPPED c6x [0, 2, 4, 6, 7, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[4], q[6], q[7], q[9], q[3];
// UNMAPPED c7x [0, 2, 3, 4, 5, 6, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[5], q[6], q[7], q[9];
// UNMAPPED c5x [0, 2, 4, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[4], q[6], q[7], q[8];
// UNMAPPED c5x [0, 2, 4, 6, 7, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[4], q[6], q[7], q[5];
// UNMAPPED c5x [0, 2, 4, 6, 7, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[4], q[6], q[7], q[3];
// UNMAPPED c5x [0, 2, 4, 6, 7, 1]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[4], q[6], q[7], q[1];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 7, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[4];
// UNMAPPED c7x [0, 1, 3, 5, 6, 7, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[5], q[6], q[7], q[8], q[2];
// UNMAPPED c6x [0, 2, 4, 6, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[4], q[6], q[8], q[9], q[7];
// UNMAPPED c6x [0, 2, 4, 6, 8, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[4], q[6], q[8], q[9], q[1];
// UNMAPPED c7x [0, 1, 4, 6, 7, 8, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[4], q[6], q[7], q[8], q[9], q[2];
// UNMAPPED c5x [0, 2, 4, 6, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[4], q[6], q[8], q[5];
// UNMAPPED c5x [0, 2, 4, 6, 8, 1]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[4], q[6], q[8], q[1];
// UNMAPPED c6x [0, 1, 2, 4, 5, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[5], q[6], q[8];
// UNMAPPED c5x [0, 1, 2, 4, 5, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[4], q[5], q[6];
// UNMAPPED c4x [0, 1, 2, 5, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[5], q[4];
// UNMAPPED c3x [0, 1, 5, 2]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[5], q[2];
// UNMAPPED c5x [0, 2, 4, 6, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[4], q[6], q[9], q[5];
// UNMAPPED c5x [0, 2, 4, 6, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[4], q[6], q[9], q[1];
// UNMAPPED c6x [0, 1, 2, 4, 5, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[5], q[9], q[6];
// UNMAPPED c5x [0, 1, 4, 5, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[4], q[5], q[9], q[2];
// UNMAPPED c4x [0, 2, 4, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[4], q[6], q[8];
// UNMAPPED c4x [0, 2, 4, 6, 1]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[4], q[6], q[1];
// UNMAPPED c5x [0, 1, 2, 4, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[4], q[8], q[6];
// UNMAPPED c4x [0, 1, 2, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[8], q[4];
// UNMAPPED c3x [0, 1, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[8], q[2];
// UNMAPPED c6x [0, 2, 4, 7, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[4], q[7], q[8], q[9], q[6];
// UNMAPPED c6x [0, 2, 4, 7, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[4], q[7], q[8], q[9], q[3];
// UNMAPPED c6x [0, 2, 4, 7, 8, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[4], q[7], q[8], q[9], q[1];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[9], q[7];
// UNMAPPED c7x [0, 1, 2, 3, 6, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[6], q[8], q[9], q[4];
// UNMAPPED c6x [0, 1, 3, 6, 8, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[6], q[8], q[9], q[2];
// UNMAPPED c5x [0, 2, 4, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[4], q[7], q[8], q[9];
// UNMAPPED c5x [0, 2, 4, 7, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[4], q[7], q[8], q[6];
// UNMAPPED c5x [0, 2, 4, 7, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[4], q[7], q[8], q[5];
// UNMAPPED c5x [0, 2, 4, 7, 8, 1]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[4], q[7], q[8], q[1];
// UNMAPPED c8x [0, 1, 2, 4, 5, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[4], q[5], q[6], q[7], q[9], q[8];
// UNMAPPED c7x [0, 1, 2, 4, 5, 6, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[4], q[5], q[6], q[9], q[7];
// UNMAPPED c6x [0, 1, 2, 5, 6, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[5], q[6], q[9], q[4];
// UNMAPPED c5x [0, 2, 4, 7, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[4], q[7], q[9], q[6];
// UNMAPPED c5x [0, 2, 4, 7, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[4], q[7], q[9], q[5];
// UNMAPPED c5x [0, 2, 4, 7, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[4], q[7], q[9], q[3];
// UNMAPPED c5x [0, 2, 4, 7, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[4], q[7], q[9], q[1];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 6, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7];
// UNMAPPED c6x [0, 1, 2, 3, 5, 6, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[6], q[4];
// UNMAPPED c4x [0, 2, 4, 7, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[4], q[7], q[3];
// UNMAPPED c4x [0, 2, 3, 4, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[3], q[4], q[7];
// UNMAPPED c3x [0, 2, 3, 4]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[2], q[3], q[4];
// UNMAPPED c5x [0, 2, 4, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[4], q[8], q[9], q[7];
// UNMAPPED c5x [0, 2, 4, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[4], q[7], q[8], q[9];
// UNMAPPED c4x [0, 2, 4, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[4], q[8], q[5];
// UNMAPPED c4x [0, 2, 4, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[4], q[8], q[3];
// UNMAPPED c5x [0, 2, 3, 4, 5, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[4], q[5], q[8];
// UNMAPPED c4x [0, 2, 4, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[4], q[9], q[5];
// UNMAPPED c3x [0, 2, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[2], q[4], q[8];
// UNMAPPED c3x [0, 2, 4, 7]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[2], q[4], q[7];
// UNMAPPED c3x [0, 2, 4, 6]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[2], q[4], q[6];
// UNMAPPED c7x [0, 2, 5, 6, 7, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[5], q[6], q[7], q[8], q[9], q[4];
// UNMAPPED c7x [0, 2, 5, 6, 7, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[5], q[6], q[7], q[8], q[9], q[3];
// UNMAPPED c8x [0, 2, 3, 4, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c7x [0, 2, 3, 4, 5, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[5], q[6], q[7], q[8];
// UNMAPPED c6x [0, 2, 3, 4, 5, 7, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[5], q[7], q[6];
// UNMAPPED c5x [0, 2, 3, 4, 7, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[4], q[7], q[5];
// UNMAPPED c6x [0, 2, 5, 6, 7, 8, 1]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[5], q[6], q[7], q[8], q[1];
// UNMAPPED c6x [0, 1, 2, 5, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[5], q[6], q[7], q[8];
// UNMAPPED c5x [0, 1, 2, 5, 7, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[5], q[7], q[6];
// UNMAPPED c4x [0, 1, 2, 7, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[7], q[5];
// UNMAPPED c3x [0, 1, 7, 2]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[7], q[2];
// UNMAPPED c6x [0, 2, 5, 6, 7, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[5], q[6], q[7], q[9], q[1];
// UNMAPPED c6x [0, 1, 2, 5, 6, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[5], q[6], q[9], q[7];
// UNMAPPED c5x [0, 2, 5, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[5], q[6], q[7], q[8];
// UNMAPPED c5x [0, 2, 5, 6, 7, 1]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[5], q[6], q[7], q[1];
// UNMAPPED c6x [0, 1, 2, 5, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[5], q[6], q[8], q[7];
// UNMAPPED c5x [0, 1, 2, 5, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[5], q[8], q[6];
// UNMAPPED c4x [0, 1, 2, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[8], q[5];
// UNMAPPED c3x [0, 1, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[8], q[2];
// UNMAPPED c6x [0, 2, 5, 6, 8, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[5], q[6], q[8], q[9], q[1];
// UNMAPPED c6x [0, 1, 2, 5, 6, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[5], q[6], q[9], q[8];
// UNMAPPED c5x [0, 1, 2, 5, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[5], q[9], q[6];
// UNMAPPED c4x [0, 1, 2, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[9], q[5];
// UNMAPPED c3x [0, 1, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[9], q[2];
// UNMAPPED c5x [0, 2, 5, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[5], q[6], q[8], q[7];
// UNMAPPED c5x [0, 2, 5, 6, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[5], q[6], q[8], q[4];
// UNMAPPED c6x [0, 2, 4, 6, 7, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[4], q[6], q[7], q[8], q[5];
// UNMAPPED c5x [0, 2, 5, 6, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[5], q[6], q[9], q[7];
// UNMAPPED c5x [0, 2, 5, 6, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[5], q[6], q[9], q[4];
// UNMAPPED c6x [0, 2, 4, 5, 6, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[4], q[5], q[6], q[7], q[9];
// UNMAPPED c5x [0, 2, 4, 5, 7, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[4], q[5], q[7], q[6];
// UNMAPPED c4x [0, 2, 5, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[5], q[6], q[8];
// UNMAPPED c4x [0, 2, 5, 6, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[5], q[6], q[7];
// UNMAPPED c4x [0, 2, 5, 6, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[5], q[6], q[4];
// UNMAPPED c4x [0, 2, 5, 6, 1]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[5], q[6], q[1];
// UNMAPPED c7x [0, 1, 2, 4, 6, 7, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[4], q[6], q[7], q[8], q[5];
// UNMAPPED c6x [0, 1, 4, 6, 7, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[4], q[6], q[7], q[8], q[2];
// UNMAPPED c6x [0, 2, 5, 7, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[5], q[7], q[8], q[9], q[6];
// UNMAPPED c6x [0, 2, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c5x [0, 2, 5, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[5], q[6], q[8], q[7];
// UNMAPPED c5x [0, 2, 5, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[5], q[7], q[8], q[9];
// UNMAPPED c5x [0, 2, 5, 7, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[5], q[7], q[8], q[6];
// UNMAPPED c5x [0, 2, 5, 7, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[5], q[7], q[8], q[3];
// UNMAPPED c5x [0, 2, 5, 7, 8, 1]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[5], q[7], q[8], q[1];
// UNMAPPED c5x [0, 2, 5, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[5], q[7], q[9], q[8];
// UNMAPPED c5x [0, 2, 5, 7, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[5], q[7], q[9], q[6];
// UNMAPPED c5x [0, 2, 5, 7, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[5], q[7], q[9], q[1];
// UNMAPPED c7x [0, 1, 2, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c6x [0, 1, 2, 5, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[5], q[6], q[8], q[7];
// UNMAPPED c5x [0, 1, 2, 6, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[6], q[8], q[5];
// UNMAPPED c4x [0, 1, 6, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[6], q[8], q[2];
// UNMAPPED c4x [0, 2, 5, 7, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[5], q[7], q[4];
// UNMAPPED c5x [0, 2, 5, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[5], q[8], q[9], q[6];
// UNMAPPED c5x [0, 2, 5, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[5], q[8], q[9], q[4];
// UNMAPPED c6x [0, 2, 4, 5, 6, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[4], q[5], q[6], q[8], q[9];
// UNMAPPED c4x [0, 2, 5, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[5], q[8], q[9];
// UNMAPPED c4x [0, 2, 5, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[5], q[8], q[6];
// UNMAPPED c4x [0, 2, 5, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[5], q[8], q[4];
// UNMAPPED c4x [0, 2, 5, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[5], q[8], q[3];
// UNMAPPED c4x [0, 2, 5, 8, 1]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[5], q[8], q[1];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[8];
// UNMAPPED c4x [0, 2, 5, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[5], q[9], q[8];
// UNMAPPED c4x [0, 2, 5, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[5], q[9], q[4];
// UNMAPPED c4x [0, 2, 5, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[5], q[9], q[3];
// UNMAPPED c4x [0, 2, 5, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[5], q[9], q[1];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[9];
// UNMAPPED c3x [0, 2, 5, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[2], q[5], q[9];
// UNMAPPED c3x [0, 2, 5, 7]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[2], q[5], q[7];
// UNMAPPED c3x [0, 2, 5, 6]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[2], q[5], q[6];
// UNMAPPED c3x [0, 2, 5, 4]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[2], q[5], q[4];
// UNMAPPED c6x [0, 2, 6, 7, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[6], q[7], q[8], q[9], q[5];
// UNMAPPED c6x [0, 2, 6, 7, 8, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[6], q[7], q[8], q[9], q[1];
// UNMAPPED c7x [0, 1, 2, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c6x [0, 1, 2, 5, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[5], q[6], q[8], q[7];
// UNMAPPED c5x [0, 2, 6, 7, 8, 1]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[6], q[7], q[8], q[1];
// UNMAPPED c5x [0, 1, 2, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[6], q[7], q[8];
// UNMAPPED c4x [0, 1, 2, 7, 6]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[7], q[6];
// UNMAPPED c5x [0, 2, 6, 7, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[6], q[7], q[9], q[5];
// UNMAPPED c5x [0, 2, 5, 6, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[5], q[6], q[7], q[9];
// UNMAPPED c4x [0, 2, 5, 6, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[5], q[6], q[7];
// UNMAPPED c4x [0, 2, 6, 7, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[6], q[7], q[5];
// UNMAPPED c4x [0, 2, 6, 7, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[6], q[7], q[4];
// UNMAPPED c4x [0, 2, 6, 7, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[6], q[7], q[3];
// UNMAPPED c6x [0, 2, 3, 4, 5, 7, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[5], q[7], q[6];
// UNMAPPED c5x [0, 2, 6, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[6], q[8], q[9], q[7];
// UNMAPPED c5x [0, 2, 6, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[6], q[8], q[9], q[5];
// UNMAPPED c5x [0, 2, 6, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[6], q[8], q[9], q[3];
// UNMAPPED c5x [0, 2, 6, 8, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[6], q[8], q[9], q[1];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 5, 7, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[6];
// UNMAPPED c6x [0, 1, 3, 5, 7, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[5], q[7], q[8], q[2];
// UNMAPPED c4x [0, 2, 6, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[6], q[8], q[9];
// UNMAPPED c4x [0, 2, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[6], q[8], q[7];
// UNMAPPED c4x [0, 2, 6, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[6], q[8], q[4];
// UNMAPPED c4x [0, 2, 6, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[6], q[8], q[3];
// UNMAPPED c4x [0, 2, 6, 8, 1]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[6], q[8], q[1];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[9], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 4, 7, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[7], q[9], q[6];
// UNMAPPED c6x [0, 1, 3, 4, 7, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[4], q[7], q[9], q[2];
// UNMAPPED c4x [0, 2, 6, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[6], q[9], q[8];
// UNMAPPED c4x [0, 2, 6, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[6], q[9], q[4];
// UNMAPPED c3x [0, 2, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[2], q[6], q[8];
// UNMAPPED c3x [0, 2, 6, 7]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[2], q[6], q[7];
// UNMAPPED c3x [0, 2, 6, 5]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[2], q[6], q[5];
// UNMAPPED c3x [0, 2, 6, 4]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[2], q[6], q[4];
// UNMAPPED c3x [0, 2, 6, 3]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[2], q[6], q[3];
// UNMAPPED c5x [0, 2, 7, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[7], q[8], q[9], q[5];
// UNMAPPED c5x [0, 2, 7, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[7], q[8], q[9], q[4];
// UNMAPPED c5x [0, 2, 7, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[7], q[8], q[9], q[3];
// UNMAPPED c5x [0, 2, 7, 8, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[7], q[8], q[9], q[1];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[9], q[7];
// UNMAPPED c4x [0, 2, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[7], q[8], q[9];
// UNMAPPED c4x [0, 2, 7, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[7], q[8], q[5];
// UNMAPPED c4x [0, 2, 7, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[7], q[8], q[4];
// UNMAPPED c4x [0, 2, 7, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[7], q[8], q[3];
// UNMAPPED c7x [0, 2, 3, 4, 5, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[5], q[7], q[9], q[8];
// UNMAPPED c4x [0, 2, 7, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[7], q[9], q[5];
// UNMAPPED c4x [0, 2, 7, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[7], q[9], q[4];
// UNMAPPED c4x [0, 2, 7, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[7], q[9], q[3];
// UNMAPPED c4x [0, 2, 7, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[7], q[9], q[1];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[9], q[7];
// UNMAPPED c3x [0, 2, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[2], q[7], q[9];
// UNMAPPED c3x [0, 2, 7, 5]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[2], q[7], q[5];
// UNMAPPED c3x [0, 2, 7, 4]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[2], q[7], q[4];
// UNMAPPED c3x [0, 2, 7, 3]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[2], q[7], q[3];
// UNMAPPED c3x [0, 2, 7, 1]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[2], q[7], q[1];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[9], q[7];
// UNMAPPED c4x [0, 2, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[8], q[9], q[5];
// UNMAPPED c4x [0, 2, 5, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[5], q[8], q[9];
// UNMAPPED c3x [0, 2, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[2], q[8], q[7];
// UNMAPPED c3x [0, 2, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[2], q[8], q[6];
// UNMAPPED c3x [0, 2, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[2], q[8], q[5];
// UNMAPPED c3x [0, 2, 8, 1]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[2], q[8], q[1];
// UNMAPPED c6x [0, 1, 2, 5, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[5], q[6], q[7], q[8];
// UNMAPPED c3x [0, 2, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[2], q[9], q[7];
// UNMAPPED c3x [0, 2, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[2], q[9], q[5];
// UNMAPPED c3x [0, 2, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[2], q[9], q[1];
ccx q[0], q[2], q[6];
ccx q[0], q[2], q[5];
ccx q[0], q[2], q[4];
ccx q[0], q[2], q[1];
// UNMAPPED c5x [0, 1, 4, 5, 6, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[4], q[5], q[6], q[2];
// UNMAPPED c8x [0, 3, 4, 5, 6, 7, 8, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[2];
// UNMAPPED c8x [0, 2, 3, 4, 5, 6, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[7];
// UNMAPPED c7x [0, 2, 3, 4, 5, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[5], q[8], q[9], q[6];
// UNMAPPED c6x [0, 2, 3, 5, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[5], q[8], q[9], q[4];
// UNMAPPED c7x [0, 3, 4, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[3], q[4], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c7x [0, 3, 4, 5, 6, 7, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[3], q[4], q[5], q[6], q[7], q[8], q[2];
// UNMAPPED c7x [0, 3, 4, 5, 6, 7, 8, 1]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[3], q[4], q[5], q[6], q[7], q[8], q[1];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 7, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[9], q[6];
// UNMAPPED c7x [0, 3, 4, 5, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[3], q[4], q[5], q[6], q[7], q[9], q[8];
// UNMAPPED c7x [0, 3, 4, 5, 6, 7, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[3], q[4], q[5], q[6], q[7], q[9], q[2];
// UNMAPPED c8x [0, 2, 3, 5, 6, 7, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[5], q[6], q[7], q[8], q[9], q[4];
// UNMAPPED c6x [0, 3, 4, 5, 6, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[3], q[4], q[5], q[6], q[7], q[9];
// UNMAPPED c6x [0, 3, 4, 5, 6, 7, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[3], q[4], q[5], q[6], q[7], q[2];
// UNMAPPED c7x [0, 2, 3, 4, 5, 6, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[5], q[6], q[9], q[7];
// UNMAPPED c6x [0, 2, 3, 4, 5, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[5], q[9], q[6];
// UNMAPPED c7x [0, 3, 4, 5, 6, 8, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[3], q[4], q[5], q[6], q[8], q[9], q[2];
// UNMAPPED c7x [0, 2, 3, 4, 5, 6, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[5], q[6], q[8], q[9];
// UNMAPPED c6x [0, 2, 3, 4, 5, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[5], q[6], q[8];
// UNMAPPED c5x [0, 2, 3, 4, 5, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[4], q[5], q[6];
// UNMAPPED c4x [0, 2, 3, 4, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[3], q[4], q[5];
// UNMAPPED c6x [0, 3, 4, 5, 6, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[3], q[4], q[5], q[6], q[8], q[2];
// UNMAPPED c6x [0, 3, 4, 5, 6, 8, 1]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[3], q[4], q[5], q[6], q[8], q[1];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8];
// UNMAPPED c6x [0, 1, 2, 3, 4, 6, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[6], q[5];
// UNMAPPED c6x [0, 3, 4, 5, 6, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[3], q[4], q[5], q[6], q[9], q[2];
// UNMAPPED c6x [0, 2, 3, 4, 5, 6, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[5], q[6], q[9];
// UNMAPPED c5x [0, 2, 3, 4, 5, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[4], q[5], q[6];
// UNMAPPED c4x [0, 2, 3, 4, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[3], q[4], q[5];
// UNMAPPED c3x [0, 2, 3, 4]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[2], q[3], q[4];
// UNMAPPED c5x [0, 3, 4, 5, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[4], q[5], q[6], q[8];
// UNMAPPED c5x [0, 3, 4, 5, 6, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[4], q[5], q[6], q[2];
// UNMAPPED c5x [0, 3, 4, 5, 6, 1]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[4], q[5], q[6], q[1];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[6];
// UNMAPPED c6x [0, 1, 2, 3, 5, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[8], q[4];
// UNMAPPED c7x [0, 3, 4, 5, 7, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[3], q[4], q[5], q[7], q[8], q[9], q[6];
// UNMAPPED c7x [0, 3, 4, 5, 7, 8, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[3], q[4], q[5], q[7], q[8], q[9], q[2];
// UNMAPPED c7x [0, 3, 4, 5, 7, 8, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[3], q[4], q[5], q[7], q[8], q[9], q[1];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[7];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[9], q[5];
// UNMAPPED c6x [0, 3, 4, 5, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[3], q[4], q[5], q[7], q[8], q[9];
// UNMAPPED c6x [0, 3, 4, 5, 7, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[3], q[4], q[5], q[7], q[8], q[2];
// UNMAPPED c7x [0, 2, 3, 4, 7, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[7], q[8], q[9], q[5];
// UNMAPPED c6x [0, 2, 3, 7, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[7], q[8], q[9], q[4];
// UNMAPPED c6x [0, 3, 4, 5, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[3], q[4], q[5], q[7], q[9], q[8];
// UNMAPPED c6x [0, 3, 4, 5, 7, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[3], q[4], q[5], q[7], q[9], q[6];
// UNMAPPED c6x [0, 3, 4, 5, 7, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[3], q[4], q[5], q[7], q[9], q[2];
// UNMAPPED c8x [0, 2, 3, 4, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c7x [0, 2, 3, 5, 6, 7, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[5], q[6], q[7], q[8], q[4];
// UNMAPPED c6x [0, 2, 5, 6, 7, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[5], q[6], q[7], q[8], q[3];
// UNMAPPED c5x [0, 3, 4, 5, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[4], q[5], q[7], q[9];
// UNMAPPED c5x [0, 3, 4, 5, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[4], q[5], q[7], q[8];
// UNMAPPED c5x [0, 3, 4, 5, 7, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[4], q[5], q[7], q[2];
// UNMAPPED c5x [0, 3, 4, 5, 7, 1]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[4], q[5], q[7], q[1];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[9], q[7];
// UNMAPPED c7x [0, 1, 2, 3, 5, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[8], q[9], q[4];
// UNMAPPED c6x [0, 1, 2, 5, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[5], q[8], q[9], q[3];
// UNMAPPED c6x [0, 3, 4, 5, 8, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[3], q[4], q[5], q[8], q[9], q[2];
// UNMAPPED c6x [0, 3, 4, 5, 8, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[3], q[4], q[5], q[8], q[9], q[1];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[9];
// UNMAPPED c6x [0, 1, 2, 3, 4, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[8], q[5];
// UNMAPPED c5x [0, 1, 2, 4, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[4], q[8], q[3];
// UNMAPPED c5x [0, 3, 4, 5, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[4], q[5], q[8], q[7];
// UNMAPPED c5x [0, 3, 4, 5, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[4], q[5], q[8], q[6];
// UNMAPPED c5x [0, 3, 4, 5, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[4], q[5], q[8], q[2];
// UNMAPPED c5x [0, 3, 4, 5, 8, 1]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[4], q[5], q[8], q[1];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 7, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[5];
// UNMAPPED c6x [0, 1, 2, 4, 6, 7, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[6], q[7], q[3];
// UNMAPPED c5x [0, 3, 4, 5, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[4], q[5], q[9], q[8];
// UNMAPPED c5x [0, 3, 4, 5, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[4], q[5], q[9], q[6];
// UNMAPPED c5x [0, 3, 4, 5, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[4], q[5], q[9], q[2];
// UNMAPPED c5x [0, 3, 4, 5, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[4], q[5], q[9], q[1];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[5];
// UNMAPPED c4x [0, 3, 4, 5, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[4], q[5], q[7];
// UNMAPPED c4x [0, 3, 4, 5, 6]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[4], q[5], q[6];
// UNMAPPED c4x [0, 3, 4, 5, 2]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[4], q[5], q[2];
// UNMAPPED c6x [0, 2, 3, 4, 6, 7, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[6], q[7], q[5];
// UNMAPPED c5x [0, 2, 4, 6, 7, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[4], q[6], q[7], q[3];
// UNMAPPED c7x [0, 3, 4, 6, 7, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[3], q[4], q[6], q[7], q[8], q[9], q[5];
// UNMAPPED c7x [0, 3, 4, 6, 7, 8, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[3], q[4], q[6], q[7], q[8], q[9], q[2];
// UNMAPPED c7x [0, 3, 4, 6, 7, 8, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[3], q[4], q[6], q[7], q[8], q[9], q[1];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 6, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7];
// UNMAPPED c6x [0, 1, 2, 4, 5, 6, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[5], q[6], q[3];
// UNMAPPED c6x [0, 3, 4, 6, 7, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[3], q[4], q[6], q[7], q[8], q[2];
// UNMAPPED c6x [0, 2, 3, 4, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[6], q[8], q[7];
// UNMAPPED c5x [0, 2, 3, 4, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[4], q[8], q[6];
// UNMAPPED c4x [0, 2, 3, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[3], q[8], q[4];
// UNMAPPED c6x [0, 3, 4, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[3], q[4], q[6], q[7], q[9], q[8];
// UNMAPPED c6x [0, 3, 4, 6, 7, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[3], q[4], q[6], q[7], q[9], q[2];
// UNMAPPED c6x [0, 3, 4, 6, 7, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[3], q[4], q[6], q[7], q[9], q[1];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[9], q[7];
// UNMAPPED c7x [0, 1, 2, 4, 6, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[4], q[6], q[8], q[9], q[3];
// UNMAPPED c5x [0, 3, 4, 6, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[4], q[6], q[7], q[9];
// UNMAPPED c5x [0, 3, 4, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[4], q[6], q[7], q[8];
// UNMAPPED c5x [0, 3, 4, 6, 7, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[4], q[6], q[7], q[5];
// UNMAPPED c5x [0, 3, 4, 6, 7, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[4], q[6], q[7], q[2];
// UNMAPPED c8x [0, 2, 3, 4, 5, 6, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[7];
// UNMAPPED c6x [0, 3, 4, 6, 8, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[3], q[4], q[6], q[8], q[9], q[2];
// UNMAPPED c6x [0, 3, 4, 6, 8, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[3], q[4], q[6], q[8], q[9], q[1];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[9];
// UNMAPPED c6x [0, 1, 2, 3, 4, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[8], q[6];
// UNMAPPED c5x [0, 1, 2, 3, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[8], q[4];
// UNMAPPED c5x [0, 3, 4, 6, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[4], q[6], q[8], q[9];
// UNMAPPED c5x [0, 3, 4, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[4], q[6], q[8], q[7];
// UNMAPPED c5x [0, 3, 4, 6, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[4], q[6], q[8], q[5];
// UNMAPPED c5x [0, 3, 4, 6, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[4], q[6], q[8], q[2];
// UNMAPPED c5x [0, 3, 4, 6, 8, 1]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[4], q[6], q[8], q[1];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[6];
// UNMAPPED c8x [0, 1, 2, 3, 5, 7, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[9], q[4];
// UNMAPPED c7x [0, 1, 2, 5, 7, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[5], q[7], q[8], q[9], q[3];
// UNMAPPED c5x [0, 3, 4, 6, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[4], q[6], q[9], q[8];
// UNMAPPED c5x [0, 3, 4, 6, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[4], q[6], q[9], q[2];
// UNMAPPED c6x [0, 2, 3, 4, 6, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[6], q[8], q[9];
// UNMAPPED c5x [0, 2, 3, 6, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[6], q[8], q[4];
// UNMAPPED c4x [0, 2, 6, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[6], q[8], q[3];
// UNMAPPED c4x [0, 3, 4, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[4], q[6], q[8];
// UNMAPPED c4x [0, 3, 4, 6, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[4], q[6], q[7];
// UNMAPPED c4x [0, 3, 4, 6, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[4], q[6], q[5];
// UNMAPPED c4x [0, 3, 4, 6, 2]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[4], q[6], q[2];
// UNMAPPED c7x [0, 2, 4, 5, 6, 7, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[4], q[5], q[6], q[7], q[8], q[3];
// UNMAPPED c6x [0, 3, 4, 7, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[3], q[4], q[7], q[8], q[9], q[6];
// UNMAPPED c6x [0, 3, 4, 7, 8, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[3], q[4], q[7], q[8], q[9], q[2];
// UNMAPPED c7x [0, 2, 3, 4, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[6], q[7], q[9], q[8];
// UNMAPPED c6x [0, 2, 3, 4, 6, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[6], q[9], q[7];
// UNMAPPED c5x [0, 3, 4, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[4], q[7], q[8], q[9];
// UNMAPPED c5x [0, 3, 4, 7, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[4], q[7], q[8], q[6];
// UNMAPPED c5x [0, 3, 4, 7, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[4], q[7], q[8], q[2];
// UNMAPPED c7x [0, 2, 3, 4, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[6], q[7], q[9], q[8];
// UNMAPPED c6x [0, 2, 3, 4, 6, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[6], q[9], q[7];
// UNMAPPED c5x [0, 2, 3, 6, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[6], q[9], q[4];
// UNMAPPED c5x [0, 3, 4, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[4], q[7], q[9], q[8];
// UNMAPPED c5x [0, 3, 4, 7, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[4], q[7], q[9], q[5];
// UNMAPPED c5x [0, 3, 4, 7, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[4], q[7], q[9], q[2];
// UNMAPPED c5x [0, 3, 4, 7, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[4], q[7], q[9], q[1];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[7];
// UNMAPPED c4x [0, 3, 4, 7, 6]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[4], q[7], q[6];
// UNMAPPED c4x [0, 3, 4, 7, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[4], q[7], q[5];
// UNMAPPED c4x [0, 3, 4, 7, 1]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[4], q[7], q[1];
// UNMAPPED c6x [0, 1, 3, 5, 6, 7, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[5], q[6], q[7], q[4];
// UNMAPPED c5x [0, 3, 4, 8, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[4], q[8], q[9], q[2];
// UNMAPPED c5x [0, 3, 4, 8, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[4], q[8], q[9], q[1];
// UNMAPPED c6x [0, 1, 2, 3, 4, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[8], q[9];
// UNMAPPED c4x [0, 3, 4, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[4], q[8], q[9];
// UNMAPPED c4x [0, 3, 4, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[4], q[8], q[7];
// UNMAPPED c4x [0, 3, 4, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[4], q[8], q[5];
// UNMAPPED c4x [0, 3, 4, 8, 1]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[4], q[8], q[1];
// UNMAPPED c7x [0, 1, 3, 5, 7, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[5], q[7], q[8], q[9], q[4];
// UNMAPPED c6x [0, 1, 5, 7, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[5], q[7], q[8], q[9], q[3];
// UNMAPPED c4x [0, 3, 4, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[4], q[9], q[8];
// UNMAPPED c4x [0, 3, 4, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[4], q[9], q[7];
// UNMAPPED c4x [0, 3, 4, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[4], q[9], q[5];
// UNMAPPED c4x [0, 3, 4, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[4], q[9], q[2];
// UNMAPPED c7x [0, 2, 3, 4, 5, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[5], q[7], q[8], q[9];
// UNMAPPED c6x [0, 2, 3, 5, 7, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[5], q[7], q[8], q[4];
// UNMAPPED c3x [0, 3, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[3], q[4], q[9];
// UNMAPPED c3x [0, 3, 4, 7]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[3], q[4], q[7];
// UNMAPPED c3x [0, 3, 4, 6]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[3], q[4], q[6];
// UNMAPPED c3x [0, 3, 4, 5]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[3], q[4], q[5];
// UNMAPPED c3x [0, 3, 4, 2]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[3], q[4], q[2];
// UNMAPPED c7x [0, 2, 3, 5, 6, 7, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[5], q[6], q[7], q[9], q[4];
// UNMAPPED c7x [0, 3, 5, 6, 7, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[3], q[5], q[6], q[7], q[8], q[9], q[4];
// UNMAPPED c7x [0, 3, 5, 6, 7, 8, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[3], q[5], q[6], q[7], q[8], q[9], q[1];
// UNMAPPED c8x [0, 1, 3, 4, 5, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[3], q[4], q[5], q[6], q[7], q[9], q[8];
// UNMAPPED c7x [0, 1, 3, 4, 6, 7, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[4], q[6], q[7], q[9], q[5];
// UNMAPPED c6x [0, 1, 4, 6, 7, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[4], q[6], q[7], q[9], q[3];
// UNMAPPED c6x [0, 3, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[3], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c6x [0, 3, 5, 6, 7, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[3], q[5], q[6], q[7], q[8], q[2];
// UNMAPPED c7x [0, 2, 3, 5, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[5], q[6], q[7], q[9], q[8];
// UNMAPPED c6x [0, 2, 3, 5, 6, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[5], q[6], q[9], q[7];
// UNMAPPED c5x [0, 2, 3, 5, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[5], q[9], q[6];
// UNMAPPED c4x [0, 2, 5, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[5], q[9], q[3];
// UNMAPPED c6x [0, 3, 5, 6, 7, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[3], q[5], q[6], q[7], q[9], q[2];
// UNMAPPED c6x [0, 3, 5, 6, 7, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[3], q[5], q[6], q[7], q[9], q[1];
// UNMAPPED c7x [0, 1, 2, 3, 5, 6, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[9];
// UNMAPPED c6x [0, 1, 2, 3, 5, 6, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[6], q[7];
// UNMAPPED c5x [0, 1, 2, 3, 5, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[5], q[6];
// UNMAPPED c4x [0, 1, 2, 5, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[5], q[3];
// UNMAPPED c5x [0, 3, 5, 6, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[5], q[6], q[7], q[9];
// UNMAPPED c5x [0, 3, 5, 6, 7, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[5], q[6], q[7], q[4];
// UNMAPPED c5x [0, 3, 5, 6, 7, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[5], q[6], q[7], q[2];
// UNMAPPED c7x [0, 2, 3, 4, 5, 6, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[5], q[6], q[9], q[7];
// UNMAPPED c6x [0, 2, 4, 5, 6, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[4], q[5], q[6], q[9], q[3];
// UNMAPPED c6x [0, 3, 5, 6, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[3], q[5], q[6], q[8], q[9], q[7];
// UNMAPPED c6x [0, 3, 5, 6, 8, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[3], q[5], q[6], q[8], q[9], q[1];
// UNMAPPED c7x [0, 1, 3, 5, 7, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[5], q[7], q[8], q[9], q[6];
// UNMAPPED c6x [0, 1, 3, 7, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[7], q[8], q[9], q[5];
// UNMAPPED c5x [0, 1, 7, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[7], q[8], q[9], q[3];
// UNMAPPED c5x [0, 3, 5, 6, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[5], q[6], q[8], q[9];
// UNMAPPED c5x [0, 3, 5, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[5], q[6], q[8], q[7];
// UNMAPPED c5x [0, 3, 5, 6, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[5], q[6], q[8], q[2];
// UNMAPPED c5x [0, 3, 5, 6, 8, 1]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[5], q[6], q[8], q[1];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[9], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 5, 7, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[7], q[9], q[6];
// UNMAPPED c6x [0, 1, 2, 3, 7, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[7], q[9], q[5];
// UNMAPPED c5x [0, 3, 5, 6, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[5], q[6], q[9], q[7];
// UNMAPPED c5x [0, 3, 5, 6, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[5], q[6], q[9], q[2];
// UNMAPPED c6x [0, 2, 3, 5, 7, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[5], q[7], q[9], q[6];
// UNMAPPED c5x [0, 2, 3, 7, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[7], q[9], q[5];
// UNMAPPED c4x [0, 2, 7, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[7], q[9], q[3];
// UNMAPPED c4x [0, 3, 5, 6, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[5], q[6], q[7];
// UNMAPPED c4x [0, 3, 5, 6, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[5], q[6], q[4];
// UNMAPPED c4x [0, 3, 5, 6, 2]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[5], q[6], q[2];
// UNMAPPED c4x [0, 3, 5, 6, 1]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[5], q[6], q[1];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 7, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[6];
// UNMAPPED c6x [0, 1, 2, 3, 4, 7, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[7], q[5];
// UNMAPPED c6x [0, 3, 5, 7, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[3], q[5], q[7], q[8], q[9], q[6];
// UNMAPPED c6x [0, 3, 5, 7, 8, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[3], q[5], q[7], q[8], q[9], q[1];
// UNMAPPED c7x [0, 1, 3, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c5x [0, 3, 5, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[5], q[7], q[8], q[9];
// UNMAPPED c5x [0, 3, 5, 7, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[5], q[7], q[8], q[6];
// UNMAPPED c5x [0, 3, 5, 7, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[5], q[7], q[8], q[4];
// UNMAPPED c5x [0, 3, 5, 7, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[5], q[7], q[8], q[2];
// UNMAPPED c8x [0, 2, 3, 4, 6, 7, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[5];
// UNMAPPED c5x [0, 3, 5, 7, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[5], q[7], q[9], q[6];
// UNMAPPED c5x [0, 3, 5, 7, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[5], q[7], q[9], q[2];
// UNMAPPED c6x [0, 2, 3, 5, 6, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[5], q[6], q[7], q[9];
// UNMAPPED c5x [0, 2, 3, 5, 6, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[5], q[6], q[7];
// UNMAPPED c4x [0, 2, 3, 6, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[2], q[3], q[6], q[5];
// UNMAPPED c3x [0, 2, 6, 3]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[2], q[6], q[3];
// UNMAPPED c4x [0, 3, 5, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[5], q[7], q[9];
// UNMAPPED c4x [0, 3, 5, 7, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[5], q[7], q[4];
// UNMAPPED c4x [0, 3, 5, 7, 2]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[5], q[7], q[2];
// UNMAPPED c4x [0, 3, 5, 7, 1]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[5], q[7], q[1];
// UNMAPPED c5x [0, 3, 5, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[5], q[8], q[9], q[7];
// UNMAPPED c5x [0, 3, 5, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[5], q[8], q[9], q[4];
// UNMAPPED c5x [0, 3, 5, 8, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[5], q[8], q[9], q[1];
// UNMAPPED c7x [0, 1, 3, 4, 5, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[4], q[5], q[7], q[8], q[9];
// UNMAPPED c6x [0, 1, 3, 4, 7, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[4], q[7], q[8], q[5];
// UNMAPPED c5x [0, 1, 4, 7, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[4], q[7], q[8], q[3];
// UNMAPPED c4x [0, 3, 5, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[5], q[8], q[9];
// UNMAPPED c4x [0, 3, 5, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[5], q[8], q[4];
// UNMAPPED c5x [0, 3, 4, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[4], q[8], q[9], q[5];
// UNMAPPED c4x [0, 3, 5, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[5], q[9], q[7];
// UNMAPPED c4x [0, 3, 5, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[5], q[9], q[2];
// UNMAPPED c4x [0, 3, 5, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[5], q[9], q[1];
// UNMAPPED c6x [0, 1, 2, 3, 5, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[7], q[9];
// UNMAPPED c5x [0, 1, 2, 3, 7, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[7], q[5];
// UNMAPPED c4x [0, 1, 2, 7, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[7], q[3];
// UNMAPPED c3x [0, 3, 5, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[3], q[5], q[9];
// UNMAPPED c3x [0, 3, 5, 7]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[3], q[5], q[7];
// UNMAPPED c3x [0, 3, 5, 6]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[3], q[5], q[6];
// UNMAPPED c3x [0, 3, 5, 2]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[3], q[5], q[2];
// UNMAPPED c3x [0, 3, 5, 1]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[3], q[5], q[1];
// UNMAPPED c7x [0, 1, 2, 3, 6, 7, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[6], q[7], q[9], q[5];
// UNMAPPED c6x [0, 3, 6, 7, 8, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[3], q[6], q[7], q[8], q[9], q[2];
// UNMAPPED c6x [0, 3, 6, 7, 8, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[3], q[6], q[7], q[8], q[9], q[1];
// UNMAPPED c7x [0, 1, 2, 3, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[6], q[7], q[8], q[9];
// UNMAPPED c6x [0, 1, 2, 3, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[6], q[8], q[7];
// UNMAPPED c5x [0, 1, 2, 3, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[8], q[6];
// UNMAPPED c4x [0, 1, 2, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[8], q[3];
// UNMAPPED c5x [0, 3, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[6], q[7], q[8], q[9];
// UNMAPPED c5x [0, 3, 6, 7, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[6], q[7], q[8], q[2];
// UNMAPPED c5x [0, 3, 6, 7, 8, 1]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[6], q[7], q[8], q[1];
// UNMAPPED c7x [0, 1, 2, 3, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[6], q[7], q[9], q[8];
// UNMAPPED c6x [0, 1, 2, 3, 6, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[6], q[9], q[7];
// UNMAPPED c5x [0, 1, 2, 3, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[9], q[6];
// UNMAPPED c4x [0, 1, 2, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[2], q[9], q[3];
// UNMAPPED c5x [0, 3, 6, 7, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[6], q[7], q[9], q[5];
// UNMAPPED c5x [0, 3, 6, 7, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[6], q[7], q[9], q[4];
// UNMAPPED c5x [0, 3, 6, 7, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[6], q[7], q[9], q[2];
// UNMAPPED c5x [0, 3, 6, 7, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[6], q[7], q[9], q[1];
// UNMAPPED c8x [0, 1, 2, 4, 5, 6, 7, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[4], q[5], q[6], q[7], q[9], q[3];
// UNMAPPED c4x [0, 3, 6, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[6], q[7], q[9];
// UNMAPPED c4x [0, 3, 6, 7, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[6], q[7], q[4];
// UNMAPPED c4x [0, 3, 6, 7, 1]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[6], q[7], q[1];
// UNMAPPED c6x [0, 1, 3, 4, 6, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[4], q[6], q[9], q[7];
// UNMAPPED c5x [0, 3, 6, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[6], q[8], q[9], q[7];
// UNMAPPED c5x [0, 3, 6, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[6], q[8], q[9], q[4];
// UNMAPPED c5x [0, 3, 6, 8, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[6], q[8], q[9], q[2];
// UNMAPPED c7x [0, 2, 3, 4, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[6], q[7], q[8], q[9];
// UNMAPPED c6x [0, 2, 3, 4, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[6], q[7], q[8];
// UNMAPPED c5x [0, 2, 4, 6, 7, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[4], q[6], q[7], q[3];
// UNMAPPED c4x [0, 3, 6, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[6], q[8], q[9];
// UNMAPPED c4x [0, 3, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[6], q[8], q[7];
// UNMAPPED c4x [0, 3, 6, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[6], q[8], q[5];
// UNMAPPED c4x [0, 3, 6, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[6], q[8], q[4];
// UNMAPPED c4x [0, 3, 6, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[6], q[8], q[2];
// UNMAPPED c8x [0, 2, 3, 4, 5, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[8];
// UNMAPPED c7x [0, 2, 3, 4, 5, 7, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[5], q[7], q[9], q[6];
// UNMAPPED c6x [0, 2, 4, 5, 7, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[4], q[5], q[7], q[9], q[3];
// UNMAPPED c4x [0, 3, 6, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[6], q[9], q[8];
// UNMAPPED c4x [0, 3, 6, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[6], q[9], q[7];
// UNMAPPED c4x [0, 3, 6, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[6], q[9], q[5];
// UNMAPPED c4x [0, 3, 6, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[6], q[9], q[4];
// UNMAPPED c4x [0, 3, 6, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[6], q[9], q[2];
// UNMAPPED c8x [0, 2, 3, 4, 5, 7, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[6];
// UNMAPPED c7x [0, 2, 4, 5, 7, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[4], q[5], q[7], q[8], q[9], q[3];
// UNMAPPED c3x [0, 3, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[3], q[6], q[8];
// UNMAPPED c3x [0, 3, 6, 4]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[3], q[6], q[4];
// UNMAPPED c3x [0, 3, 6, 1]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[3], q[6], q[1];
// UNMAPPED c5x [0, 1, 4, 6, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[4], q[6], q[8], q[3];
// UNMAPPED c5x [0, 3, 7, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[7], q[8], q[9], q[6];
// UNMAPPED c5x [0, 3, 7, 8, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[7], q[8], q[9], q[1];
// UNMAPPED c6x [0, 1, 3, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[6], q[7], q[8], q[9];
// UNMAPPED c5x [0, 1, 3, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[6], q[8], q[7];
// UNMAPPED c4x [0, 1, 6, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[6], q[8], q[3];
// UNMAPPED c4x [0, 3, 7, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[7], q[8], q[5];
// UNMAPPED c4x [0, 3, 7, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[7], q[8], q[4];
// UNMAPPED c4x [0, 3, 7, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[7], q[8], q[2];
// UNMAPPED c4x [0, 3, 7, 8, 1]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[7], q[8], q[1];
// UNMAPPED c4x [0, 3, 7, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[7], q[9], q[6];
// UNMAPPED c4x [0, 3, 7, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[7], q[9], q[5];
// UNMAPPED c4x [0, 3, 7, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[7], q[9], q[1];
// UNMAPPED c6x [0, 1, 3, 5, 6, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[5], q[6], q[9], q[7];
// UNMAPPED c3x [0, 3, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[3], q[7], q[9];
// UNMAPPED c3x [0, 3, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[3], q[7], q[8];
// UNMAPPED c3x [0, 3, 7, 5]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[3], q[7], q[5];
// UNMAPPED c3x [0, 3, 7, 4]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[3], q[7], q[4];
// UNMAPPED c3x [0, 3, 7, 1]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[3], q[7], q[1];
// UNMAPPED c7x [0, 1, 3, 4, 5, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[4], q[5], q[8], q[9], q[7];
// UNMAPPED c6x [0, 1, 4, 5, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[4], q[5], q[8], q[9], q[3];
// UNMAPPED c4x [0, 3, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[8], q[9], q[7];
// UNMAPPED c4x [0, 3, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[8], q[9], q[6];
// UNMAPPED c4x [0, 3, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[8], q[9], q[4];
// UNMAPPED c4x [0, 3, 8, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[8], q[9], q[2];
// UNMAPPED c7x [0, 2, 3, 4, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[6], q[7], q[9], q[8];
// UNMAPPED c3x [0, 3, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[3], q[8], q[7];
// UNMAPPED c3x [0, 3, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[3], q[8], q[6];
// UNMAPPED c3x [0, 3, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[3], q[8], q[2];
// UNMAPPED c3x [0, 3, 8, 1]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[3], q[8], q[1];
// UNMAPPED c6x [0, 1, 2, 6, 7, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[6], q[7], q[8], q[3];
// UNMAPPED c3x [0, 3, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[3], q[9], q[7];
// UNMAPPED c3x [0, 3, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[3], q[9], q[5];
// UNMAPPED c3x [0, 3, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[3], q[9], q[4];
// UNMAPPED c3x [0, 3, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[3], q[9], q[2];
// UNMAPPED c3x [0, 3, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[3], q[9], q[1];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[9];
// UNMAPPED c6x [0, 1, 2, 4, 5, 7, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[4], q[5], q[7], q[3];
ccx q[0], q[3], q[5];
ccx q[0], q[3], q[4];
// UNMAPPED c7x [0, 4, 5, 6, 7, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[4], q[5], q[6], q[7], q[8], q[9], q[3];
// UNMAPPED c7x [0, 4, 5, 6, 7, 8, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[4], q[5], q[6], q[7], q[8], q[9], q[2];
// UNMAPPED c8x [0, 2, 3, 5, 6, 7, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[5], q[6], q[7], q[8], q[9], q[4];
// UNMAPPED c6x [0, 4, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[4], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c6x [0, 4, 5, 6, 7, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[4], q[5], q[6], q[7], q[8], q[3];
// UNMAPPED c7x [0, 3, 4, 5, 6, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[3], q[4], q[5], q[6], q[8], q[9], q[7];
// UNMAPPED c6x [0, 4, 5, 6, 7, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[4], q[5], q[6], q[7], q[9], q[3];
// UNMAPPED c6x [0, 3, 4, 5, 6, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[3], q[4], q[5], q[6], q[7], q[9];
// UNMAPPED c5x [0, 3, 4, 5, 7, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[4], q[5], q[7], q[6];
// UNMAPPED c5x [0, 4, 5, 6, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[4], q[5], q[6], q[7], q[9];
// UNMAPPED c5x [0, 4, 5, 6, 7, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[4], q[5], q[6], q[7], q[3];
// UNMAPPED c6x [0, 3, 4, 5, 6, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[3], q[4], q[5], q[6], q[9], q[7];
// UNMAPPED c5x [0, 3, 4, 5, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[4], q[5], q[9], q[6];
// UNMAPPED c4x [0, 3, 5, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[5], q[9], q[4];
// UNMAPPED c6x [0, 4, 5, 6, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[4], q[5], q[6], q[8], q[9], q[3];
// UNMAPPED c6x [0, 3, 4, 5, 6, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[3], q[4], q[5], q[6], q[9], q[8];
// UNMAPPED c5x [0, 4, 5, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[4], q[5], q[6], q[8], q[7];
// UNMAPPED c5x [0, 4, 5, 6, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[4], q[5], q[6], q[8], q[3];
// UNMAPPED c5x [0, 4, 5, 6, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[4], q[5], q[6], q[8], q[2];
// UNMAPPED c7x [0, 2, 3, 4, 5, 7, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[5], q[7], q[8], q[6];
// UNMAPPED c5x [0, 4, 5, 6, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[4], q[5], q[6], q[9], q[7];
// UNMAPPED c5x [0, 4, 5, 6, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[4], q[5], q[6], q[9], q[3];
// UNMAPPED c6x [0, 3, 4, 5, 7, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[3], q[4], q[5], q[7], q[9], q[6];
// UNMAPPED c5x [0, 3, 4, 7, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[4], q[7], q[9], q[5];
// UNMAPPED c4x [0, 4, 5, 6, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[4], q[5], q[6], q[9];
// UNMAPPED c4x [0, 4, 5, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[4], q[5], q[6], q[8];
// UNMAPPED c4x [0, 4, 5, 6, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[4], q[5], q[6], q[7];
// UNMAPPED c4x [0, 4, 5, 6, 2]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[4], q[5], q[6], q[2];
// UNMAPPED c7x [0, 2, 4, 5, 7, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[4], q[5], q[7], q[8], q[9], q[6];
// UNMAPPED c6x [0, 4, 5, 7, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[4], q[5], q[7], q[8], q[9], q[3];
// UNMAPPED c6x [0, 4, 5, 7, 8, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[4], q[5], q[7], q[8], q[9], q[1];
// UNMAPPED c7x [0, 1, 3, 4, 5, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[4], q[5], q[7], q[8], q[9];
// UNMAPPED c6x [0, 1, 3, 4, 5, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[4], q[5], q[7], q[8];
// UNMAPPED c5x [0, 1, 3, 4, 5, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[4], q[5], q[7];
// UNMAPPED c5x [0, 4, 5, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[4], q[5], q[7], q[8], q[9];
// UNMAPPED c5x [0, 4, 5, 7, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[4], q[5], q[7], q[8], q[6];
// UNMAPPED c5x [0, 4, 5, 7, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[4], q[5], q[7], q[8], q[3];
// UNMAPPED c7x [0, 3, 4, 5, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[3], q[4], q[5], q[6], q[7], q[9], q[8];
// UNMAPPED c6x [0, 3, 4, 5, 6, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[3], q[4], q[5], q[6], q[9], q[7];
// UNMAPPED c5x [0, 3, 5, 6, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[5], q[6], q[9], q[4];
// UNMAPPED c5x [0, 4, 5, 7, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[4], q[5], q[7], q[9], q[1];
// UNMAPPED c4x [0, 4, 5, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[4], q[5], q[7], q[8];
// UNMAPPED c4x [0, 4, 5, 7, 6]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[4], q[5], q[7], q[6];
// UNMAPPED c4x [0, 4, 5, 7, 1]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[4], q[5], q[7], q[1];
// UNMAPPED c6x [0, 1, 4, 5, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[4], q[5], q[6], q[8], q[7];
// UNMAPPED c5x [0, 1, 5, 6, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[5], q[6], q[8], q[4];
// UNMAPPED c5x [0, 4, 5, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[4], q[5], q[8], q[9], q[7];
// UNMAPPED c5x [0, 4, 5, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[4], q[5], q[8], q[9], q[3];
// UNMAPPED c5x [0, 4, 5, 8, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[4], q[5], q[8], q[9], q[2];
// UNMAPPED c5x [0, 4, 5, 8, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[4], q[5], q[8], q[9], q[1];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[9], q[8];
// UNMAPPED c4x [0, 4, 5, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[4], q[5], q[8], q[9];
// UNMAPPED c4x [0, 4, 5, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[4], q[5], q[8], q[7];
// UNMAPPED c4x [0, 4, 5, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[4], q[5], q[8], q[6];
// UNMAPPED c4x [0, 4, 5, 8, 1]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[4], q[5], q[8], q[1];
// UNMAPPED c7x [0, 1, 4, 5, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[4], q[5], q[6], q[7], q[9], q[8];
// UNMAPPED c4x [0, 4, 5, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[4], q[5], q[9], q[1];
// UNMAPPED c3x [0, 4, 5, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[4], q[5], q[9];
// UNMAPPED c3x [0, 4, 5, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[4], q[5], q[8];
// UNMAPPED c3x [0, 4, 5, 6]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[4], q[5], q[6];
// UNMAPPED c3x [0, 4, 5, 2]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[4], q[5], q[2];
// UNMAPPED c3x [0, 4, 5, 1]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[4], q[5], q[1];
// UNMAPPED c7x [0, 1, 2, 4, 6, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[4], q[6], q[8], q[9], q[5];
// UNMAPPED c6x [0, 4, 6, 7, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[4], q[6], q[7], q[8], q[9], q[5];
// UNMAPPED c6x [0, 4, 6, 7, 8, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[4], q[6], q[7], q[8], q[9], q[2];
// UNMAPPED c6x [0, 4, 6, 7, 8, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[4], q[6], q[7], q[8], q[9], q[1];
// UNMAPPED c8x [0, 1, 2, 4, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[4], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c7x [0, 1, 2, 4, 5, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[4], q[5], q[6], q[8], q[7];
// UNMAPPED c5x [0, 4, 6, 7, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[4], q[6], q[7], q[8], q[5];
// UNMAPPED c5x [0, 4, 5, 7, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[4], q[5], q[7], q[8], q[6];
// UNMAPPED c5x [0, 4, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[4], q[6], q[7], q[9], q[8];
// UNMAPPED c5x [0, 4, 6, 7, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[4], q[6], q[7], q[9], q[5];
// UNMAPPED c5x [0, 4, 6, 7, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[4], q[6], q[7], q[9], q[3];
// UNMAPPED c5x [0, 4, 6, 7, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[4], q[6], q[7], q[9], q[2];
// UNMAPPED c8x [0, 2, 3, 4, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c7x [0, 2, 3, 4, 5, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[5], q[6], q[8], q[7];
// UNMAPPED c6x [0, 2, 3, 5, 6, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[5], q[6], q[8], q[4];
// UNMAPPED c4x [0, 4, 6, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[4], q[6], q[7], q[9];
// UNMAPPED c4x [0, 4, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[4], q[6], q[7], q[8];
// UNMAPPED c4x [0, 4, 6, 7, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[4], q[6], q[7], q[5];
// UNMAPPED c4x [0, 4, 6, 7, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[4], q[6], q[7], q[3];
// UNMAPPED c4x [0, 4, 6, 7, 2]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[4], q[6], q[7], q[2];
// UNMAPPED c4x [0, 4, 6, 7, 1]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[4], q[6], q[7], q[1];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[7];
// UNMAPPED c5x [0, 4, 6, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[4], q[6], q[8], q[9], q[5];
// UNMAPPED c5x [0, 4, 6, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[4], q[6], q[8], q[9], q[3];
// UNMAPPED c6x [0, 3, 4, 5, 6, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[3], q[4], q[5], q[6], q[8], q[9];
// UNMAPPED c5x [0, 3, 4, 5, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[4], q[5], q[6], q[8];
// UNMAPPED c4x [0, 3, 5, 6, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[5], q[6], q[4];
// UNMAPPED c4x [0, 4, 6, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[4], q[6], q[8], q[9];
// UNMAPPED c4x [0, 4, 6, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[4], q[6], q[8], q[5];
// UNMAPPED c4x [0, 4, 6, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[4], q[6], q[8], q[2];
// UNMAPPED c6x [0, 2, 4, 5, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[4], q[5], q[8], q[9], q[6];
// UNMAPPED c4x [0, 4, 6, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[4], q[6], q[9], q[7];
// UNMAPPED c4x [0, 4, 6, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[4], q[6], q[9], q[5];
// UNMAPPED c4x [0, 4, 6, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[4], q[6], q[9], q[1];
// UNMAPPED c6x [0, 1, 4, 5, 6, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[4], q[5], q[6], q[7], q[9];
// UNMAPPED c3x [0, 4, 6, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[4], q[6], q[9];
// UNMAPPED c3x [0, 4, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[4], q[6], q[8];
// UNMAPPED c3x [0, 4, 6, 5]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[4], q[6], q[5];
// UNMAPPED c3x [0, 4, 6, 3]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[4], q[6], q[3];
// UNMAPPED c3x [0, 4, 6, 1]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[4], q[6], q[1];
// UNMAPPED c7x [0, 1, 3, 4, 5, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[4], q[5], q[8], q[9], q[6];
// UNMAPPED c6x [0, 1, 3, 5, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[5], q[8], q[9], q[4];
// UNMAPPED c5x [0, 4, 7, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[4], q[7], q[8], q[9], q[6];
// UNMAPPED c5x [0, 4, 7, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[4], q[7], q[8], q[9], q[5];
// UNMAPPED c5x [0, 4, 7, 8, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[4], q[7], q[8], q[9], q[2];
// UNMAPPED c5x [0, 4, 7, 8, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[4], q[7], q[8], q[9], q[1];
// UNMAPPED c8x [0, 1, 2, 4, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[4], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c7x [0, 1, 2, 5, 6, 7, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[5], q[6], q[7], q[8], q[4];
// UNMAPPED c4x [0, 4, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[4], q[7], q[8], q[9];
// UNMAPPED c4x [0, 4, 7, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[4], q[7], q[8], q[5];
// UNMAPPED c4x [0, 4, 7, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[4], q[7], q[8], q[3];
// UNMAPPED c6x [0, 3, 4, 5, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[3], q[4], q[5], q[7], q[9], q[8];
// UNMAPPED c5x [0, 3, 5, 7, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[3], q[5], q[7], q[9], q[4];
// UNMAPPED c4x [0, 4, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[4], q[7], q[9], q[8];
// UNMAPPED c4x [0, 4, 7, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[4], q[7], q[9], q[5];
// UNMAPPED c4x [0, 4, 7, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[4], q[7], q[9], q[1];
// UNMAPPED c6x [0, 1, 4, 5, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[4], q[5], q[8], q[9], q[7];
// UNMAPPED c3x [0, 4, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[4], q[7], q[9];
// UNMAPPED c3x [0, 4, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[4], q[7], q[8];
// UNMAPPED c3x [0, 4, 7, 6]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[4], q[7], q[6];
// UNMAPPED c3x [0, 4, 7, 5]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[4], q[7], q[5];
// UNMAPPED c3x [0, 4, 7, 3]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[4], q[7], q[3];
// UNMAPPED c3x [0, 4, 7, 1]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[4], q[7], q[1];
// UNMAPPED c4x [0, 4, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[4], q[8], q[9], q[6];
// UNMAPPED c4x [0, 4, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[4], q[8], q[9], q[3];
// UNMAPPED c4x [0, 4, 8, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[4], q[8], q[9], q[1];
// UNMAPPED c6x [0, 1, 3, 4, 6, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[4], q[6], q[8], q[9];
// UNMAPPED c3x [0, 4, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[4], q[8], q[9];
// UNMAPPED c3x [0, 4, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[4], q[8], q[7];
// UNMAPPED c3x [0, 4, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[4], q[8], q[6];
// UNMAPPED c3x [0, 4, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[4], q[8], q[3];
// UNMAPPED c3x [0, 4, 8, 1]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[4], q[8], q[1];
// UNMAPPED c7x [0, 1, 3, 4, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[4], q[6], q[7], q[9], q[8];
// UNMAPPED c3x [0, 4, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[4], q[9], q[8];
// UNMAPPED c3x [0, 4, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[4], q[9], q[7];
// UNMAPPED c3x [0, 4, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[4], q[9], q[6];
// UNMAPPED c3x [0, 4, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[4], q[9], q[5];
// UNMAPPED c3x [0, 4, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[4], q[9], q[3];
// UNMAPPED c3x [0, 4, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[4], q[9], q[2];
ccx q[0], q[4], q[9];
ccx q[0], q[4], q[7];
ccx q[0], q[4], q[6];
ccx q[0], q[4], q[5];
ccx q[0], q[4], q[3];
ccx q[0], q[4], q[2];
ccx q[0], q[4], q[1];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 7, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[9], q[4];
// UNMAPPED c6x [0, 5, 6, 7, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[5], q[6], q[7], q[8], q[9], q[3];
// UNMAPPED c5x [0, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c5x [0, 5, 6, 7, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[5], q[6], q[7], q[8], q[4];
// UNMAPPED c5x [0, 5, 6, 7, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[5], q[6], q[7], q[8], q[3];
// UNMAPPED c7x [0, 3, 4, 5, 6, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[3], q[4], q[5], q[6], q[8], q[9], q[7];
// UNMAPPED c5x [0, 5, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[5], q[6], q[7], q[9], q[8];
// UNMAPPED c5x [0, 5, 6, 7, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[5], q[6], q[7], q[9], q[3];
// UNMAPPED c5x [0, 5, 6, 7, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[5], q[6], q[7], q[9], q[1];
// UNMAPPED c7x [0, 1, 3, 5, 7, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[5], q[7], q[8], q[9], q[6];
// UNMAPPED c6x [0, 1, 3, 7, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[7], q[8], q[9], q[5];
// UNMAPPED c4x [0, 5, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[5], q[6], q[7], q[8];
// UNMAPPED c4x [0, 5, 6, 7, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[5], q[6], q[7], q[3];
// UNMAPPED c4x [0, 5, 6, 7, 2]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[5], q[6], q[7], q[2];
// UNMAPPED c6x [0, 2, 3, 5, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[5], q[6], q[8], q[7];
// UNMAPPED c5x [0, 5, 6, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[5], q[6], q[8], q[9], q[7];
// UNMAPPED c5x [0, 5, 6, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[5], q[6], q[8], q[9], q[3];
// UNMAPPED c6x [0, 3, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[3], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c4x [0, 5, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[5], q[6], q[8], q[7];
// UNMAPPED c4x [0, 5, 6, 8, 1]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[5], q[6], q[8], q[1];
// UNMAPPED c5x [0, 1, 5, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[5], q[6], q[7], q[8];
// UNMAPPED c4x [0, 1, 5, 7, 6]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[5], q[7], q[6];
// UNMAPPED c4x [0, 5, 6, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[5], q[6], q[9], q[4];
// UNMAPPED c4x [0, 5, 6, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[5], q[6], q[9], q[3];
// UNMAPPED c4x [0, 5, 6, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[5], q[6], q[9], q[1];
// UNMAPPED c6x [0, 1, 3, 4, 6, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[4], q[6], q[9], q[5];
// UNMAPPED c3x [0, 5, 6, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[5], q[6], q[9];
// UNMAPPED c3x [0, 5, 6, 4]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[5], q[6], q[4];
// UNMAPPED c3x [0, 5, 6, 1]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[5], q[6], q[1];
// UNMAPPED c5x [0, 1, 4, 6, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[4], q[6], q[9], q[5];
// UNMAPPED c5x [0, 5, 7, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[5], q[7], q[8], q[9], q[6];
// UNMAPPED c5x [0, 5, 7, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[5], q[7], q[8], q[9], q[4];
// UNMAPPED c5x [0, 5, 7, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[5], q[7], q[8], q[9], q[3];
// UNMAPPED c5x [0, 5, 7, 8, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[5], q[7], q[8], q[9], q[2];
// UNMAPPED c5x [0, 5, 7, 8, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[5], q[7], q[8], q[9], q[1];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8];
// UNMAPPED c4x [0, 5, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[5], q[7], q[8], q[9];
// UNMAPPED c4x [0, 5, 7, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[5], q[7], q[8], q[4];
// UNMAPPED c4x [0, 5, 7, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[5], q[7], q[8], q[3];
// UNMAPPED c4x [0, 5, 7, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[5], q[7], q[8], q[2];
// UNMAPPED c4x [0, 5, 7, 8, 1]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[5], q[7], q[8], q[1];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[9], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 4, 7, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[7], q[9], q[5];
// UNMAPPED c4x [0, 5, 7, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[5], q[7], q[9], q[6];
// UNMAPPED c4x [0, 5, 7, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[5], q[7], q[9], q[4];
// UNMAPPED c5x [0, 4, 5, 6, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[4], q[5], q[6], q[7], q[9];
// UNMAPPED c3x [0, 5, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[5], q[7], q[8];
// UNMAPPED c3x [0, 5, 7, 4]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[5], q[7], q[4];
// UNMAPPED c3x [0, 5, 7, 3]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[5], q[7], q[3];
// UNMAPPED c3x [0, 5, 7, 2]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[5], q[7], q[2];
// UNMAPPED c3x [0, 5, 7, 1]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[5], q[7], q[1];
// UNMAPPED c7x [0, 1, 2, 3, 4, 7, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[5];
// UNMAPPED c4x [0, 5, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[5], q[8], q[9], q[7];
// UNMAPPED c4x [0, 5, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[5], q[8], q[9], q[6];
// UNMAPPED c3x [0, 5, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[5], q[8], q[6];
// UNMAPPED c3x [0, 5, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[5], q[8], q[2];
// UNMAPPED c3x [0, 5, 8, 1]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[5], q[8], q[1];
// UNMAPPED c3x [0, 5, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[5], q[9], q[8];
// UNMAPPED c3x [0, 5, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[5], q[9], q[2];
// UNMAPPED c3x [0, 5, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[5], q[9], q[1];
ccx q[0], q[5], q[9];
ccx q[0], q[5], q[6];
ccx q[0], q[5], q[4];
// UNMAPPED c5x [0, 6, 7, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[6], q[7], q[8], q[9], q[3];
// UNMAPPED c5x [0, 6, 7, 8, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[6], q[7], q[8], q[9], q[1];
// UNMAPPED c6x [0, 1, 3, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[6], q[7], q[8], q[9];
// UNMAPPED c5x [0, 1, 3, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[6], q[7], q[8];
// UNMAPPED c4x [0, 1, 3, 6, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[3], q[6], q[7];
// UNMAPPED c3x [0, 1, 3, 6]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[3], q[6];
// UNMAPPED c4x [0, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[6], q[7], q[8], q[9];
// UNMAPPED c4x [0, 6, 7, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[6], q[7], q[8], q[2];
// UNMAPPED c5x [0, 2, 7, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[7], q[8], q[9], q[6];
// UNMAPPED c4x [0, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[6], q[7], q[9], q[8];
// UNMAPPED c4x [0, 6, 7, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[6], q[7], q[9], q[5];
// UNMAPPED c4x [0, 6, 7, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[6], q[7], q[9], q[3];
// UNMAPPED c6x [0, 3, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[3], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c3x [0, 6, 7, 5]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[6], q[7], q[5];
// UNMAPPED c3x [0, 6, 7, 1]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[6], q[7], q[1];
// UNMAPPED c4x [0, 1, 5, 7, 6]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[5], q[7], q[6];
// UNMAPPED c4x [0, 6, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[6], q[8], q[9], q[5];
// UNMAPPED c4x [0, 6, 8, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[6], q[8], q[9], q[1];
// UNMAPPED c3x [0, 6, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[6], q[8], q[5];
// UNMAPPED c3x [0, 6, 8, 1]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[6], q[8], q[1];
// UNMAPPED c4x [0, 1, 5, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[5], q[8], q[6];
// UNMAPPED c3x [0, 6, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[6], q[9], q[5];
// UNMAPPED c3x [0, 6, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[6], q[9], q[1];
// UNMAPPED c4x [0, 1, 5, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[5], q[9], q[6];
ccx q[0], q[6], q[7];
ccx q[0], q[6], q[5];
ccx q[0], q[6], q[2];
ccx q[0], q[6], q[1];
// UNMAPPED c4x [0, 7, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[7], q[8], q[9], q[6];
// UNMAPPED c4x [0, 7, 8, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[7], q[8], q[9], q[2];
// UNMAPPED c4x [0, 7, 8, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[7], q[8], q[9], q[1];
// UNMAPPED c3x [0, 7, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[7], q[8], q[6];
// UNMAPPED c3x [0, 7, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[7], q[8], q[2];
// UNMAPPED c3x [0, 7, 8, 1]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[7], q[8], q[1];
// UNMAPPED c5x [0, 1, 2, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[6], q[8], q[7];
// UNMAPPED c3x [0, 7, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[7], q[9], q[6];
// UNMAPPED c3x [0, 7, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[7], q[9], q[2];
// UNMAPPED c3x [0, 7, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[7], q[9], q[1];
// UNMAPPED c5x [0, 1, 2, 6, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[6], q[9], q[7];
ccx q[0], q[7], q[8];
ccx q[0], q[7], q[6];
ccx q[0], q[7], q[3];
// UNMAPPED c3x [0, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[8], q[9], q[7];
// UNMAPPED c3x [0, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[8], q[9], q[3];
// UNMAPPED c4x [0, 3, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[3], q[7], q[9], q[8];
ccx q[0], q[8], q[9];
ccx q[0], q[8], q[7];
ccx q[0], q[8], q[4];
ccx q[0], q[9], q[7];
ccx q[0], q[9], q[6];
ccx q[0], q[9], q[5];
ccx q[0], q[9], q[4];
ccx q[0], q[9], q[3];
ccx q[0], q[9], q[1];
