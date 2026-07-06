OPENQASM 3.0;
include "stdgates.inc";
qubit[13] q;

gate qpgf_c10x q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10 { }  // opaque: c10x (11q), golden in registry/modules/c10x.sealed.json
gate qpgf_c11x q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11 { }  // opaque: c11x (12q), golden in registry/modules/c11x.sealed.json
gate qpgf_c12x q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12 { }  // opaque: c12x (13q), golden in registry/modules/c12x.sealed.json
gate qpgf_c3x q0, q1, q2, q3 { }  // opaque: c3x (4q), golden in registry/modules/c3x.sealed.json
gate qpgf_c4x q0, q1, q2, q3, q4 { }  // opaque: c4x (5q), golden in registry/modules/c4x.sealed.json
gate qpgf_c5x q0, q1, q2, q3, q4, q5 { }  // opaque: c5x (6q), golden in registry/modules/c5x.sealed.json
gate qpgf_c6x q0, q1, q2, q3, q4, q5, q6 { }  // opaque: c6x (7q), golden in registry/modules/c6x.sealed.json
gate qpgf_c7x q0, q1, q2, q3, q4, q5, q6, q7 { }  // opaque: c7x (8q), golden in registry/modules/c7x.sealed.json
gate qpgf_c8x q0, q1, q2, q3, q4, q5, q6, q7, q8 { }  // opaque: c8x (9q), golden in registry/modules/c8x.sealed.json
gate qpgf_c9x q0, q1, q2, q3, q4, q5, q6, q7, q8, q9 { }  // opaque: c9x (10q), golden in registry/modules/c9x.sealed.json

// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11];
// UNMAPPED c12x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c12x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[11], q[12], q[10];
// UNMAPPED c12x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c12x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[11], q[12];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[12], q[11];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[11], q[12];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[11];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[10], q[11], q[12];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[10], q[11], q[9];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[10], q[12], q[9];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[12];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[10], q[11];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 9]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[10], q[9];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[11], q[12], q[9];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 8, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[11], q[12];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 8, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[11], q[9];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[12], q[11];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[12], q[11];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[12], q[10];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[12], q[9];
// UNMAPPED c12x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c12x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 8, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[10];
// UNMAPPED c12x [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c12x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[10], q[11], q[12], q[8];
// UNMAPPED c12x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c12x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[11], q[10];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 8, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[11], q[9];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[10], q[11], q[12];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[10], q[11], q[8];
// UNMAPPED c12x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c12x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[12], q[11];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[10], q[12], q[9];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[10], q[11];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 8]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[10], q[8];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[10], q[11], q[9];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 9, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[11], q[12], q[10];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 9, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[11], q[12], q[8];
// UNMAPPED c12x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c12x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[12], q[11];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 9, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[11], q[8];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[11];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 9, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[12], q[11];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 9, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[12], q[8];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[11], q[12], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 9, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 9, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[10];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[10], q[11], q[12], q[8];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[11], q[12], q[10];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[10], q[11], q[12];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 10, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[10], q[11], q[9];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[10], q[12], q[11];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 9, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[12], q[10];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 10, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[10], q[12], q[9];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 9, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[12], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[10], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 10, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[10], q[8];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[12], q[10];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[11], q[12], q[10];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 11, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[11], q[12], q[9];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[11], q[12], q[8];
// UNMAPPED c12x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c12x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[11], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[12], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 7, 12]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[12];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 7, 11]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[11];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 7, 10]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[10];
// UNMAPPED c12x [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c12x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[10], q[11], q[12], q[7];
// UNMAPPED c12x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c12x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[11], q[10];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[10], q[11], q[7];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[11], q[10];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 8, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[11], q[9];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[10], q[12], q[11];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[10], q[12], q[7];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[10], q[12];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 7]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[10], q[7];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[10], q[12], q[8];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 8, 9, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[11], q[12], q[10];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 8, 9, 11, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[11], q[12], q[7];
// UNMAPPED c12x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c12x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[10], q[11], q[9];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 10, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[10], q[11], q[8];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 8, 9, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[11], q[7];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[11];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 8, 9, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[12], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 8, 9, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 8, 9, 11]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 8, 9, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[7];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 8, 10, 11, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[10], q[11], q[12], q[7];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[10], q[11], q[12];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[10], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 10, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[10], q[8];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 8, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[10], q[11], q[12];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 8, 10, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[10], q[11], q[9];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[10], q[12], q[11];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 8, 9, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[12], q[10];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[10], q[12], q[11];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[10], q[12], q[7];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[10], q[11], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 8, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[10], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 8, 10, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[10], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 8, 10, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[10], q[7];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[10], q[12], q[8];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 8, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[11], q[12], q[10];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 8, 11, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[11], q[12], q[7];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[10], q[12], q[11];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 10, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[10], q[12], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 8, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[11], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 8, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[11], q[9];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 8, 9, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[12], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 8, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[12], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 8, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[12], q[7];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 8, 12]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[12];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 8, 11]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[11];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 9, 10, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[10], q[11], q[12], q[8];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[10], q[12], q[11];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 8, 9, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[12], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 8, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[12], q[9];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[10], q[11], q[12];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 9, 10, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[10], q[11], q[7];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 9, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[11], q[12], q[10];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 9, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[10], q[12], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 9, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[10], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 9, 10, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[10], q[7];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 9, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[11], q[12], q[10];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[10], q[11], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 9, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[10], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 9, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[11], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 9, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[11], q[7];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 11, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[11], q[12], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 9, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[12], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 9, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[12], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 9, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[12], q[7];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[10], q[11], q[12];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 10, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[10], q[11], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 9, 12]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[12];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[7];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 10, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[10], q[11], q[12], q[8];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 10, 11, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[10], q[11], q[12], q[7];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[10], q[12], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 10, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[10], q[11], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 10, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[10], q[11], q[7];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[10], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[10], q[12], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 10, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[10], q[12], q[9];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[10], q[11], q[12];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[10], q[12];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 10, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[10], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 10, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[10], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[11], q[12], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[11], q[12], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 11, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[11], q[12], q[7];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[10], q[11], q[12];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[11], q[12];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[11], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[10], q[12], q[11];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[12], q[11];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[12], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[12], q[7];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 8, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[11], q[12];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 6, 12]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[12];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 6, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7];
// UNMAPPED c12x [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c12x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[10], q[11], q[12], q[6];
// UNMAPPED c12x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c12x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[11], q[12], q[10];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 9, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[11], q[12], q[8];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 9, 11, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[11], q[12], q[7];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 6]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[10], q[11], q[6];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[7];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[10], q[12], q[11];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[10], q[12], q[6];
// UNMAPPED c12x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c12x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[11], q[12], q[10];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 9, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[11], q[12], q[8];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 9, 11, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[11], q[12], q[7];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[10], q[12];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 6]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[10], q[6];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[10], q[12], q[9];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 10, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[10], q[12], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 10, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[10], q[12], q[7];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 7, 8, 9, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[11], q[12], q[10];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 7, 8, 9, 11, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[11], q[12], q[6];
// UNMAPPED c12x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c12x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[10], q[11], q[8];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 9, 10, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[10], q[11], q[7];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 7, 8, 9, 11, 6]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[11], q[6];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 8, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[11], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 8, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[11], q[7];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 7, 8, 9, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[12], q[10];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 7, 8, 9, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[12], q[6];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[10], q[12], q[7];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[6];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 7, 8, 10, 11, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[10], q[11], q[12], q[6];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[10], q[11], q[12];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[10], q[11];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 7, 8, 10, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[10], q[11], q[9];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 7, 8, 10, 11, 6]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[10], q[11], q[6];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 8]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[10], q[8];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 7, 8, 10, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[10], q[12], q[9];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 7, 8, 10, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[10], q[12], q[6];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[12];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[7];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 8, 10, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[10], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 8, 10, 6]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[10], q[6];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 7, 8, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[11], q[12], q[10];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 7, 8, 11, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[11], q[12], q[9];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 7, 8, 11, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[11], q[12], q[6];
// UNMAPPED c12x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c12x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 8, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[11], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 8, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[11], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 8, 11, 6]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[11], q[6];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[10], q[11], q[8];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 9, 10, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[10], q[11], q[7];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 8, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[12], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 8, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[12], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 8, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[12], q[9];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[10], q[11], q[12];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 7, 8, 12]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[12];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 7, 8, 10]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 7, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[6];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 10, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[10], q[12], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 10, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[10], q[12], q[7];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 7, 9, 10, 11, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[9], q[10], q[11], q[12], q[6];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 9, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[11], q[12], q[10];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 11, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[11], q[12], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 11, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[11], q[12], q[7];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 7, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[9], q[10], q[11], q[12];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 7, 9, 10, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[9], q[10], q[11], q[8];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 7, 9, 10, 11, 6]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[9], q[10], q[11], q[6];
// UNMAPPED c12x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c12x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[12], q[11];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 7, 9, 10, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[9], q[10], q[12], q[8];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 7, 9, 10, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[9], q[10], q[12], q[6];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 9, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[9], q[10], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 9, 10, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[9], q[10], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 9, 10, 6]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[9], q[10], q[6];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 7, 9, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[9], q[11], q[12], q[10];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 7, 9, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[9], q[11], q[12], q[8];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[10], q[11], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 9, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[9], q[11], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 9, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[9], q[11], q[8];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 7, 8, 9, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[12], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 8, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[12], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 9, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[9], q[12], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 9, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[9], q[12], q[6];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[7];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 7, 9, 12]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[9], q[12];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 7, 9, 11]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[9], q[11];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[9], q[8];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 7, 10, 11, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[10], q[11], q[12], q[9];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 7, 10, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[10], q[11], q[12], q[8];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 7, 10, 11, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[10], q[11], q[12], q[6];
// UNMAPPED c12x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c12x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[12], q[11];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[12], q[10];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 8, 9, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[12], q[7];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[10], q[11], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 10, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[10], q[11], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 10, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[10], q[11], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 10, 11, 6]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[10], q[11], q[6];
// UNMAPPED c12x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c12x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[12], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[10], q[12], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 10, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[10], q[12], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 10, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[10], q[12], q[8];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 7, 8, 9, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[11], q[12], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 7, 10, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[10], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 7, 8, 10]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 11, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[11], q[12], q[6];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[11], q[12];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[11], q[7];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 7, 11, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[11], q[6];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[11], q[7];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 7, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[12], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 7, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[12], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 7, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[12], q[6];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[7];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 7, 11]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[11];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 7, 10]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[10];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 7, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[6];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 8, 9, 10, 11, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[9], q[10], q[11], q[12], q[7];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 8, 9, 10, 11, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[9], q[10], q[11], q[12], q[6];
// UNMAPPED c12x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c12x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 9]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[10], q[9];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 8, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[9], q[10], q[11], q[12];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 8, 9, 10, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[9], q[10], q[11], q[7];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 8, 9, 10, 11, 6]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[9], q[10], q[11], q[6];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 8, 9, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[9], q[10], q[12], q[11];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 8, 9, 10, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[9], q[10], q[12], q[6];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 8, 10, 11, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[10], q[11], q[12], q[9];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 10, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[10], q[11], q[12], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 8, 9, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[9], q[10], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 8, 9, 10, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[9], q[10], q[7];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 7, 8, 9, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[11], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 8, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[11], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 7, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[11], q[8];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 8, 9, 11, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[9], q[11], q[12], q[7];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 8, 9, 11, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[9], q[11], q[12], q[6];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[11], q[12];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 8, 9, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[9], q[11], q[7];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 9, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[9], q[11], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 8, 9, 12]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[9], q[12];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 8, 9, 11]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[9], q[11];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 8, 9, 10]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[9], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[9], q[7];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[9], q[6];
// UNMAPPED c12x [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c12x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[10], q[11], q[12], q[9];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[10], q[11], q[12], q[8];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 8, 10, 11, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[10], q[11], q[12], q[7];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 7, 8, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[10], q[12], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 8, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[10], q[11], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 8, 10, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[10], q[11], q[7];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 7, 10, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[10], q[11], q[12], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 8, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[10], q[12], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 8, 10, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[10], q[12], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 8, 10, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[10], q[12], q[7];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 7, 8, 9, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[11], q[12], q[10];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 7, 9, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[9], q[11], q[12], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 8, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[10], q[11];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 8, 10, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[10], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 8, 10, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[10], q[6];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 8, 9, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[11], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 8, 11, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[11], q[12], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 8, 11, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[11], q[12], q[7];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 8, 11, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[11], q[6];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 8, 11]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[11];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 8, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[12], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 8, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[12], q[7];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 8, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[12], q[6];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 9, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[12], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 8, 12]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[12];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 8, 11]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[11];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 8, 10]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[10];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[7];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 7, 9, 10, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[9], q[10], q[11], q[12], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 9, 10, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[9], q[10], q[11], q[7];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 10, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[10], q[11], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 9, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[9], q[10], q[12], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 9, 10, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[9], q[10], q[12], q[7];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 7, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[9], q[10], q[11], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 10, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[10], q[11], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 9, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[9], q[10], q[12];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 9, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[9], q[10], q[11];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 9, 10, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[9], q[10], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 9, 10, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[9], q[10], q[7];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 7, 8, 9, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[11], q[12], q[10];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 7, 8, 11, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[11], q[12], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 9, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[9], q[11], q[12], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 9, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[9], q[11], q[12], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 9, 11, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[9], q[11], q[12], q[7];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[10], q[11], q[12];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 7, 8, 10, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[10], q[11], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 9, 11, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[9], q[11], q[6];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 9, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[9], q[12], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 9, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[9], q[12], q[6];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 9, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[10], q[12];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 9, 11]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[9], q[11];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[9], q[7];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 10, 11, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[10], q[11], q[12], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[9], q[10], q[11], q[12];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 9, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[9], q[10], q[11];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[10], q[11], q[12];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 10, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[10], q[11], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 10, 11, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[10], q[11], q[6];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 9, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[10], q[12], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 9, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[12], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[10], q[12], q[11];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 10, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[10], q[12], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 10, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[10], q[12], q[6];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[10], q[11];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 10, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[10], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 11, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[11], q[12], q[6];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[11], q[12];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 6, 11]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[11];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[11], q[10];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 11, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[11], q[6];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[12], q[11];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[12], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[12], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[12], q[7];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[12], q[6];
// UNMAPPED c6x [0, 1, 2, 3, 4, 5, 10]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[5], q[10];
// UNMAPPED c6x [0, 1, 2, 3, 4, 5, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[5], q[8];
// UNMAPPED c6x [0, 1, 2, 3, 4, 5, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[5], q[7];
// UNMAPPED c12x [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 5]  (QASM3 비표준 — opaque)
qpgf_c12x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[5];
// UNMAPPED c12x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c12x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[7];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[9], q[6];
// UNMAPPED c11x [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[10], q[11], q[12];
// UNMAPPED c11x [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 5]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[10], q[11], q[5];
// UNMAPPED c12x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c12x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[12], q[11];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[10], q[12], q[9];
// UNMAPPED c11x [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 12, 5]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[10], q[12], q[5];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[10], q[12], q[7];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[10], q[12];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 5]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[10], q[5];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[10], q[12], q[9];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[10], q[12], q[7];
// UNMAPPED c11x [0, 1, 2, 3, 4, 6, 7, 8, 9, 11, 12, 5]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[11], q[12], q[5];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[12], q[11];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 9, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[12], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 9, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[12], q[7];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 7, 8, 9, 11, 5]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[11], q[5];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[7];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 7, 8, 9, 12, 5]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[12], q[5];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[12], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[12], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[12], q[7];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 7, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[5];
// UNMAPPED c11x [0, 1, 2, 3, 4, 6, 7, 8, 10, 11, 12, 5]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[10], q[11], q[12], q[5];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 7, 8, 10, 11, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[10], q[11], q[12], q[6];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 7, 8, 10, 11, 5]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[10], q[11], q[5];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[10], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 8, 10, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[10], q[7];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 7, 8, 10, 12, 5]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[10], q[12], q[5];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[12], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[12], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 7, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[12], q[6];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 7, 8, 10, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[10], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 7, 8, 10, 5]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[10], q[5];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 8]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[10], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 9, 10, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[10], q[7];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 7, 8, 11, 12, 5]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[11], q[12], q[5];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[11], q[12], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 7, 8, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[11], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 7, 8, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[11], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 7, 8, 11, 5]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[11], q[5];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[10], q[11], q[12], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 7, 8, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[12], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 7, 8, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[12], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 7, 8, 12, 5]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[12], q[5];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[12];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 8]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[10], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 9, 10, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[10], q[7];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 9, 10, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[9], q[10], q[6];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 7, 8, 12]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[12];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 7, 8, 11]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[11];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 7, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[5];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[11], q[12], q[8];
// UNMAPPED c11x [0, 1, 2, 3, 4, 6, 7, 9, 10, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[9], q[10], q[11], q[12], q[8];
// UNMAPPED c11x [0, 1, 2, 3, 4, 6, 7, 8, 9, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[11], q[12], q[10];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 7, 8, 11, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[11], q[12], q[9];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 7, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[9], q[10], q[11], q[12];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 7, 9, 10, 11, 5]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[9], q[10], q[11], q[5];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 9, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[11], q[12], q[10];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 9, 11, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[11], q[12], q[7];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 9, 11, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[9], q[11], q[12], q[6];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 7, 9, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[9], q[10], q[12], q[11];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 7, 9, 10, 12, 5]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[9], q[10], q[12], q[5];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 9, 10, 11, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[10], q[11], q[12], q[7];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 9, 10, 11, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[9], q[10], q[11], q[12], q[6];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 7, 9, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[9], q[10], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 7, 9, 10, 5]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[9], q[10], q[5];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 9, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[11], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[11], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[11], q[7];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 7, 9, 11, 12, 5]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[9], q[11], q[12], q[5];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 9, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[11], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 9, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[11], q[7];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 7, 9, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[9], q[11], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 7, 9, 11, 5]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[9], q[11], q[5];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[10], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 7, 9, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[9], q[12], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 7, 9, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[9], q[12], q[8];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 7, 8, 10, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[10], q[12], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 7, 9, 12]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[9], q[12];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 7, 9, 10]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[9], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[9], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 7, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[9], q[5];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[10], q[12], q[7];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 8, 9, 10, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[9], q[10], q[12], q[6];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 7, 10, 11, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[10], q[11], q[12], q[9];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 7, 10, 11, 12, 5]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[10], q[11], q[12], q[5];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[10], q[11], q[12];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[10], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 9, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 7, 10, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[10], q[11], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 7, 10, 11, 5]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[10], q[11], q[5];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 9, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[11], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 9, 11, 6]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[9], q[11], q[6];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 7, 10, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[10], q[12], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 7, 8, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[12], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 7, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[10], q[12];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 7, 10, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[10], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 7, 10, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[10], q[5];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 9, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[12], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 7, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[11], q[12], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 7, 11, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[11], q[12], q[9];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 7, 9, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[9], q[10], q[12], q[11];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 7, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[11], q[12];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 7, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[11], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 7, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[11], q[9];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 7, 9, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[9], q[10], q[12], q[11];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 7, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[12], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 7, 12, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[12], q[5];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 8, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[12];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 7, 12]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[12];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 7, 11]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[11];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 7, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[5];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 8, 11, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[11], q[12], q[7];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 8, 11, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[11], q[12], q[6];
// UNMAPPED c11x [0, 1, 2, 3, 4, 6, 8, 9, 10, 11, 12, 5]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[9], q[10], q[11], q[12], q[5];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[10], q[11], q[12];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 8, 10, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[10], q[11], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 10, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[10], q[11], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 10, 11, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[10], q[11], q[6];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 8, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[9], q[10], q[11], q[12];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 8, 9, 10, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[9], q[10], q[11], q[7];
// UNMAPPED c11x [0, 1, 2, 3, 4, 6, 7, 8, 9, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[11], q[12], q[10];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 7, 9, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[9], q[11], q[12], q[8];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 8, 9, 10, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[9], q[10], q[12], q[7];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[10], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 7, 9, 10, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[9], q[10], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 8, 9, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[9], q[10], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 8, 9, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[9], q[10], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 8, 9, 10, 5]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[9], q[10], q[5];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 9, 10, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[10], q[11], q[12], q[8];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 9, 10, 11, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[9], q[10], q[11], q[12], q[6];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 8, 9, 11, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[9], q[11], q[12], q[7];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 7, 8, 9, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[11], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 7, 8, 9, 11]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[11];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[9], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 8, 9, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[9], q[11], q[7];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 8, 9, 11, 5]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[9], q[11], q[5];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 9, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[11], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 8, 9, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[9], q[12], q[7];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 8, 9, 12, 5]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[9], q[12], q[5];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 7, 8, 9, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[12], q[6];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 8, 9, 10]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[9], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[9], q[7];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[9], q[5];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 8]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[10], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 9, 10, 6]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[9], q[10], q[6];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 8, 10, 11, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[10], q[11], q[12], q[7];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 7, 8, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[11], q[12], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 7, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[11], q[12], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 8, 10, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[10], q[11], q[7];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 8, 10, 11, 5]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[10], q[11], q[5];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[10], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 8, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 7, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[6];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 8, 10, 12, 5]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[10], q[12], q[5];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 8, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[10], q[12];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 8, 10]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[10];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 8, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[10], q[11];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 8, 10, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[10], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 8, 10, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[10], q[7];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 7, 9, 10, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[9], q[10], q[11], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 8, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[11], q[12], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 8, 11, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[11], q[12], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 8, 11, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[11], q[12], q[7];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 8, 11, 12, 5]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[11], q[12], q[5];
// UNMAPPED c12x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c12x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 8]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[10], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 9, 10, 6]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[9], q[10], q[6];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 8, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[11], q[7];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 7, 8, 11]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[11];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 8, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[12], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 8, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[12], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 8, 12, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[12], q[5];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 9, 10, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[10], q[12], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 9, 10, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[9], q[10], q[12], q[6];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 8, 12]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[12];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 8, 11]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[11];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[7];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 7, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[11], q[12], q[8];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 9, 10, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[9], q[10], q[11], q[12], q[8];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 9, 10, 11, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[9], q[10], q[11], q[12], q[7];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 9, 10, 11, 12, 5]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[9], q[10], q[11], q[12], q[5];
// UNMAPPED c12x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c12x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 6]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[10], q[6];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 9, 10, 11, 5]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[9], q[10], q[11], q[5];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 9, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[10], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 9, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[9], q[10], q[12], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 9, 10, 12, 5]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[9], q[10], q[12], q[5];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[10], q[11], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 10, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[10], q[11], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 10, 11, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[10], q[11], q[6];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 9, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[9], q[10], q[11];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 9, 10, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[9], q[10], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 9, 10, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[9], q[10], q[7];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 7, 8, 9, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[11], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 9, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[9], q[11], q[12], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 9, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[9], q[11], q[12];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 9, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[9], q[11], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 9, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[9], q[11], q[7];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 9, 11, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[9], q[11], q[5];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[12], q[11];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 9, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[9], q[12], q[11];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 9, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[9], q[12], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 9, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[9], q[12], q[7];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 9, 12, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[9], q[12], q[5];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[10], q[11], q[12], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[9], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[9], q[7];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[9], q[5];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 10, 11, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[10], q[11], q[12], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 10, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[10], q[11], q[12], q[8];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 8, 9, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[9], q[11], q[12], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 10, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[10], q[11], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 10, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[10], q[11], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 10, 11, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[10], q[11], q[5];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[10], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 8, 9, 10, 6]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[9], q[10], q[6];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[10], q[12], q[11];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 10, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[10], q[12], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 10, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[10], q[12], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[10], q[12];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[10], q[11];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 10, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[10], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 10, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[10], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 10, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[10], q[7];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 10, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[10], q[5];
// UNMAPPED c12x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c12x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[11], q[12], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[11], q[12], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 11, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[11], q[12], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 11, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[11], q[12], q[7];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[11], q[12];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 11, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[11], q[5];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 11, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[11], q[12], q[6];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[12], q[10];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[12], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 12, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[12], q[5];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 8, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[10], q[12];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 8, 10, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[10], q[6];
// UNMAPPED c6x [0, 1, 2, 3, 4, 6, 12]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[6], q[12];
// UNMAPPED c6x [0, 1, 2, 3, 4, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[6], q[8];
// UNMAPPED c11x [0, 1, 2, 3, 4, 7, 8, 9, 10, 11, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[9], q[10], q[11], q[12], q[6];
// UNMAPPED c11x [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[10], q[12], q[11];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 7, 8, 9, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[12], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 7, 9, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[9], q[12], q[8];
// UNMAPPED c10x [0, 1, 2, 3, 4, 7, 8, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[9], q[10], q[11], q[12];
// UNMAPPED c10x [0, 1, 2, 3, 4, 7, 8, 9, 10, 11, 6]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[9], q[10], q[11], q[6];
// UNMAPPED c10x [0, 1, 2, 3, 4, 7, 8, 9, 10, 11, 5]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[9], q[10], q[11], q[5];
// UNMAPPED c12x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c12x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[11], q[12], q[10];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[11], q[12], q[9];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[11], q[12], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 11, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[11], q[12], q[7];
// UNMAPPED c10x [0, 1, 2, 3, 4, 7, 8, 9, 10, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[9], q[10], q[12], q[6];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 7, 8, 10, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[10], q[12], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 7, 10, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[10], q[12], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 10, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[10], q[12], q[7];
// UNMAPPED c9x [0, 1, 2, 3, 4, 7, 8, 9, 10, 5]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[9], q[10], q[5];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 8, 9, 10, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[9], q[10], q[7];
// UNMAPPED c10x [0, 1, 2, 3, 4, 7, 8, 9, 11, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[9], q[11], q[12], q[6];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 7, 8, 9, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[12], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 7, 9, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[9], q[12], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 4, 7, 8, 9, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[9], q[11], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 4, 7, 8, 9, 11, 6]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[9], q[11], q[6];
// UNMAPPED c9x [0, 1, 2, 3, 4, 7, 8, 9, 11, 5]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[9], q[11], q[5];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[10], q[11], q[8];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 9, 10, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[10], q[11], q[7];
// UNMAPPED c9x [0, 1, 2, 3, 4, 7, 8, 9, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[9], q[12], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 4, 7, 8, 9, 12, 5]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[9], q[12], q[5];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 7, 8, 9, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[11], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 8, 9, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[9], q[11], q[7];
// UNMAPPED c8x [0, 1, 2, 3, 4, 7, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[9], q[6];
// UNMAPPED c8x [0, 1, 2, 3, 4, 7, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[9], q[5];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[7];
// UNMAPPED c10x [0, 1, 2, 3, 4, 7, 8, 10, 11, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[10], q[11], q[12], q[9];
// UNMAPPED c10x [0, 1, 2, 3, 4, 7, 8, 9, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[9], q[10], q[12], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 4, 7, 8, 9, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[9], q[12], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 4, 7, 8, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[10], q[11], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 7, 8, 10, 11, 6]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[10], q[11], q[6];
// UNMAPPED c9x [0, 1, 2, 3, 4, 7, 8, 10, 11, 5]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[10], q[11], q[5];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[10], q[12], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 4, 7, 8, 10, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[10], q[12], q[6];
// UNMAPPED c9x [0, 1, 2, 3, 4, 7, 8, 10, 12, 5]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[10], q[12], q[5];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[10], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 8, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 4, 7, 8, 10, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[10], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 7, 8, 10, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[10], q[5];
// UNMAPPED c9x [0, 1, 2, 3, 4, 7, 8, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[11], q[12], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 4, 7, 8, 11, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[11], q[12], q[6];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 7, 8, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[10], q[11], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 7, 10, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[10], q[11], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 4, 7, 8, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[11], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 7, 8, 11, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[11], q[5];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 8, 9, 11]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[11];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[9], q[7];
// UNMAPPED c8x [0, 1, 2, 3, 4, 7, 8, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[12], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 4, 7, 8, 12, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[12], q[5];
// UNMAPPED c7x [0, 1, 2, 3, 4, 7, 8, 12]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[12];
// UNMAPPED c7x [0, 1, 2, 3, 4, 7, 8, 11]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[11];
// UNMAPPED c7x [0, 1, 2, 3, 4, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 4, 7, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[6];
// UNMAPPED c7x [0, 1, 2, 3, 4, 7, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[5];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 8, 9, 11, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[11], q[12], q[7];
// UNMAPPED c10x [0, 1, 2, 3, 4, 7, 9, 10, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[7], q[9], q[10], q[11], q[12], q[8];
// UNMAPPED c10x [0, 1, 2, 3, 4, 7, 9, 10, 11, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[7], q[9], q[10], q[11], q[12], q[6];
// UNMAPPED c11x [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[10], q[11], q[12];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 7, 8, 9, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[11], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 7, 8, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[11], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 8, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[11], q[7];
// UNMAPPED c9x [0, 1, 2, 3, 4, 7, 9, 10, 11, 6]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[7], q[9], q[10], q[11], q[6];
// UNMAPPED c9x [0, 1, 2, 3, 4, 7, 9, 10, 11, 5]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[7], q[9], q[10], q[11], q[5];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[10], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 10, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[10], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 10, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[10], q[7];
// UNMAPPED c9x [0, 1, 2, 3, 4, 7, 9, 10, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[7], q[9], q[10], q[12], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 4, 7, 9, 10, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[7], q[9], q[10], q[12], q[6];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[10], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 7, 8, 9, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 4, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[7];
// UNMAPPED c8x [0, 1, 2, 3, 4, 7, 9, 10, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[7], q[9], q[10], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 4, 7, 8, 10, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[10], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 4, 7, 9, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[7], q[9], q[11], q[12], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 4, 7, 9, 11, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[7], q[9], q[11], q[12], q[6];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 7, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[9], q[10], q[11], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 7, 9, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[9], q[10], q[11];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 9, 10, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[9], q[10], q[7];
// UNMAPPED c8x [0, 1, 2, 3, 4, 7, 9, 11, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[7], q[9], q[11], q[5];
// UNMAPPED c8x [0, 1, 2, 3, 4, 7, 9, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[7], q[9], q[12], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 4, 7, 8, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[12], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 4, 7, 9, 10]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[7], q[9], q[10];
// UNMAPPED c7x [0, 1, 2, 3, 4, 7, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[7], q[9], q[6];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 7, 10, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[10], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 4, 7, 10, 11, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[7], q[10], q[11], q[12], q[6];
// UNMAPPED c9x [0, 1, 2, 3, 4, 7, 10, 11, 12, 5]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[7], q[10], q[11], q[12], q[5];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[10], q[11], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[11], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 4, 7, 10, 11, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[7], q[10], q[11], q[6];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 10, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[10], q[11], q[7];
// UNMAPPED c8x [0, 1, 2, 3, 4, 7, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[7], q[10], q[12], q[11];
// UNMAPPED c8x [0, 1, 2, 3, 4, 7, 10, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[7], q[10], q[12], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 7, 10, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[7], q[10], q[12], q[6];
// UNMAPPED c8x [0, 1, 2, 3, 4, 7, 10, 12, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[7], q[10], q[12], q[5];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[10], q[11], q[12];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 9, 10, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[10], q[11], q[7];
// UNMAPPED c7x [0, 1, 2, 3, 4, 7, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[7], q[10], q[11];
// UNMAPPED c7x [0, 1, 2, 3, 4, 7, 10, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[7], q[10], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 4, 7, 10, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[7], q[10], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 4, 7, 10, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[7], q[10], q[5];
// UNMAPPED c8x [0, 1, 2, 3, 4, 7, 11, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[7], q[11], q[12], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 7, 11, 12, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[7], q[11], q[12], q[5];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 9, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[9], q[11], q[12];
// UNMAPPED c7x [0, 1, 2, 3, 4, 7, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[7], q[11], q[10];
// UNMAPPED c7x [0, 1, 2, 3, 4, 7, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[7], q[11], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 4, 7, 11, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[7], q[11], q[6];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 7, 8, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[10], q[11];
// UNMAPPED c7x [0, 1, 2, 3, 4, 7, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[7], q[12], q[11];
// UNMAPPED c7x [0, 1, 2, 3, 4, 7, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[7], q[12], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 4, 7, 12, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[7], q[12], q[5];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 9, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[9], q[11], q[12];
// UNMAPPED c6x [0, 1, 2, 3, 4, 7, 12]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[7], q[12];
// UNMAPPED c6x [0, 1, 2, 3, 4, 7, 11]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[7], q[11];
// UNMAPPED c6x [0, 1, 2, 3, 4, 7, 10]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[7], q[10];
// UNMAPPED c6x [0, 1, 2, 3, 4, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[7], q[9];
// UNMAPPED c6x [0, 1, 2, 3, 4, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[7], q[8];
// UNMAPPED c6x [0, 1, 2, 3, 4, 7, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[7], q[5];
// UNMAPPED c10x [0, 1, 2, 3, 4, 8, 9, 10, 11, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[8], q[9], q[10], q[11], q[12], q[6];
// UNMAPPED c10x [0, 1, 2, 3, 4, 8, 9, 10, 11, 12, 5]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[8], q[9], q[10], q[11], q[12], q[5];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[10], q[11], q[12];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 8, 10, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[10], q[11], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 10, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[10], q[11], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 4, 8, 9, 10, 11, 5]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[8], q[9], q[10], q[11], q[5];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 8, 9, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[9], q[10], q[11];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 8, 9, 10]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[9], q[10];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[9];
// UNMAPPED c6x [0, 1, 2, 3, 4, 5, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[5], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 4, 8, 9, 10, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[8], q[9], q[10], q[12], q[7];
// UNMAPPED c9x [0, 1, 2, 3, 4, 8, 9, 10, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[8], q[9], q[10], q[12], q[6];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 7, 8, 10, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[10], q[12], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 7, 10, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[10], q[12], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 4, 8, 9, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[8], q[9], q[10], q[12];
// UNMAPPED c8x [0, 1, 2, 3, 4, 8, 9, 10, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[8], q[9], q[10], q[7];
// UNMAPPED c8x [0, 1, 2, 3, 4, 8, 9, 10, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[8], q[9], q[10], q[5];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 7, 8, 10, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[10], q[12], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 4, 8, 9, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[8], q[9], q[11], q[12], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 4, 8, 9, 11, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[8], q[9], q[11], q[12], q[7];
// UNMAPPED c9x [0, 1, 2, 3, 4, 8, 9, 11, 12, 5]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[8], q[9], q[11], q[12], q[5];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 7, 9, 10, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[9], q[10], q[11], q[12], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 4, 8, 9, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[8], q[9], q[11], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 4, 8, 9, 11, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[8], q[9], q[11], q[6];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 8, 9, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[9], q[10], q[11];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 8, 10, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[8], q[10], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 8, 9, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[8], q[9], q[12], q[7];
// UNMAPPED c8x [0, 1, 2, 3, 4, 8, 9, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[8], q[9], q[12], q[6];
// UNMAPPED c8x [0, 1, 2, 3, 4, 8, 9, 12, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[8], q[9], q[12], q[5];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 4, 8, 9, 12]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[8], q[9], q[12];
// UNMAPPED c7x [0, 1, 2, 3, 4, 8, 9, 11]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[8], q[9], q[11];
// UNMAPPED c7x [0, 1, 2, 3, 4, 8, 9, 10]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[8], q[9], q[10];
// UNMAPPED c7x [0, 1, 2, 3, 4, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[8], q[9], q[7];
// UNMAPPED c7x [0, 1, 2, 3, 4, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[8], q[9], q[5];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 7, 8, 10, 11, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[10], q[11], q[12], q[9];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 7, 10, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[10], q[11], q[12], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 4, 8, 10, 11, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[8], q[10], q[11], q[12], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 4, 8, 10, 11, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[8], q[10], q[11], q[12], q[6];
// UNMAPPED c9x [0, 1, 2, 3, 4, 8, 10, 11, 12, 5]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[8], q[10], q[11], q[12], q[5];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[10], q[11], q[12];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[10], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 9, 10, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[10], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 4, 8, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[8], q[10], q[11], q[12];
// UNMAPPED c8x [0, 1, 2, 3, 4, 8, 10, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[8], q[10], q[11], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 8, 10, 11, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[8], q[10], q[11], q[5];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 8, 9, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[9], q[10], q[12], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 8, 9, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[9], q[12], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 9, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[9], q[12], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 4, 8, 10, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[8], q[10], q[12], q[7];
// UNMAPPED c8x [0, 1, 2, 3, 4, 8, 10, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[8], q[10], q[12], q[6];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 7, 8, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[10], q[12];
// UNMAPPED c7x [0, 1, 2, 3, 4, 8, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[8], q[10], q[12];
// UNMAPPED c7x [0, 1, 2, 3, 4, 8, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[8], q[10], q[11];
// UNMAPPED c7x [0, 1, 2, 3, 4, 8, 10, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[8], q[10], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 4, 8, 9, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[8], q[9], q[11], q[12], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 4, 8, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[8], q[11], q[12], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 4, 8, 11, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[8], q[11], q[12], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 8, 11, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[8], q[11], q[12], q[7];
// UNMAPPED c8x [0, 1, 2, 3, 4, 8, 11, 12, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[8], q[11], q[12], q[5];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[10], q[11], q[12];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[10], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 9, 10, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[9], q[10], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 4, 8, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[8], q[11], q[12];
// UNMAPPED c7x [0, 1, 2, 3, 4, 8, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[8], q[11], q[10];
// UNMAPPED c7x [0, 1, 2, 3, 4, 8, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[8], q[11], q[7];
// UNMAPPED c7x [0, 1, 2, 3, 4, 8, 11, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[8], q[11], q[5];
// UNMAPPED c7x [0, 1, 2, 3, 4, 8, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[8], q[12], q[11];
// UNMAPPED c7x [0, 1, 2, 3, 4, 8, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[8], q[12], q[10];
// UNMAPPED c7x [0, 1, 2, 3, 4, 8, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[8], q[12], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 4, 8, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[8], q[12], q[6];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 9, 10, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[9], q[10], q[11], q[12], q[8];
// UNMAPPED c6x [0, 1, 2, 3, 4, 8, 11]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[8], q[11];
// UNMAPPED c6x [0, 1, 2, 3, 4, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[8], q[5];
// UNMAPPED c9x [0, 1, 2, 3, 4, 9, 10, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[9], q[10], q[11], q[12], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 4, 9, 10, 11, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[9], q[10], q[11], q[12], q[7];
// UNMAPPED c10x [0, 1, 2, 3, 4, 7, 8, 9, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[9], q[10], q[12], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 4, 7, 8, 9, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[9], q[12], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 4, 9, 10, 11, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[9], q[10], q[11], q[5];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 9, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[9], q[11], q[10];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[11], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 9, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[9], q[10], q[12], q[11];
// UNMAPPED c8x [0, 1, 2, 3, 4, 9, 10, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[9], q[10], q[12], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 4, 9, 10, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[9], q[10], q[12], q[7];
// UNMAPPED c8x [0, 1, 2, 3, 4, 9, 10, 12, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[9], q[10], q[12], q[5];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[10], q[11], q[12];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 7, 8, 9, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[11], q[10];
// UNMAPPED c7x [0, 1, 2, 3, 4, 9, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[9], q[10], q[12];
// UNMAPPED c7x [0, 1, 2, 3, 4, 9, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[9], q[10], q[11];
// UNMAPPED c7x [0, 1, 2, 3, 4, 9, 10, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[9], q[10], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 4, 9, 10, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[9], q[10], q[7];
// UNMAPPED c7x [0, 1, 2, 3, 4, 9, 10, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[9], q[10], q[5];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 7, 8, 10, 11, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[10], q[11], q[12], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 9, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[9], q[11], q[12], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 4, 9, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[9], q[11], q[12], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 4, 9, 11, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[9], q[11], q[12], q[7];
// UNMAPPED c8x [0, 1, 2, 3, 4, 9, 11, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[9], q[11], q[12], q[6];
// UNMAPPED c11x [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[10], q[12], q[11];
// UNMAPPED c7x [0, 1, 2, 3, 4, 9, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[9], q[11], q[10];
// UNMAPPED c7x [0, 1, 2, 3, 4, 9, 11, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[9], q[11], q[6];
// UNMAPPED c7x [0, 1, 2, 3, 4, 9, 11, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[9], q[11], q[5];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 9, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[10], q[11];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 10, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[10], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 4, 9, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[9], q[12], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 4, 9, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[9], q[12], q[7];
// UNMAPPED c7x [0, 1, 2, 3, 4, 9, 12, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[9], q[12], q[5];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 8, 9, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[12];
// UNMAPPED c6x [0, 1, 2, 3, 4, 9, 11]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[9], q[11];
// UNMAPPED c6x [0, 1, 2, 3, 4, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[9], q[8];
// UNMAPPED c6x [0, 1, 2, 3, 4, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[9], q[7];
// UNMAPPED c6x [0, 1, 2, 3, 4, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[9], q[6];
// UNMAPPED c6x [0, 1, 2, 3, 4, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[9], q[5];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 8, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[11], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 10, 11, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[10], q[11], q[12], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 10, 11, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[10], q[11], q[12], q[6];
// UNMAPPED c8x [0, 1, 2, 3, 4, 10, 11, 12, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[10], q[11], q[12], q[5];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[10], q[11], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 9, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[11], q[10];
// UNMAPPED c7x [0, 1, 2, 3, 4, 10, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[10], q[11], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 4, 10, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[10], q[11], q[7];
// UNMAPPED c7x [0, 1, 2, 3, 4, 10, 11, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[10], q[11], q[5];
// UNMAPPED c7x [0, 1, 2, 3, 4, 10, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[10], q[12], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 4, 10, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[10], q[12], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 4, 10, 12, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[10], q[12], q[5];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 8, 9, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[9], q[10], q[12];
// UNMAPPED c6x [0, 1, 2, 3, 4, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[10], q[11];
// UNMAPPED c6x [0, 1, 2, 3, 4, 10, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[10], q[9];
// UNMAPPED c6x [0, 1, 2, 3, 4, 10, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[10], q[6];
// UNMAPPED c8x [0, 1, 2, 3, 4, 6, 9, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[6], q[9], q[11], q[10];
// UNMAPPED c7x [0, 1, 2, 3, 4, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[11], q[12], q[10];
// UNMAPPED c7x [0, 1, 2, 3, 4, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[11], q[12], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 4, 11, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[11], q[12], q[6];
// UNMAPPED c7x [0, 1, 2, 3, 4, 11, 12, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[11], q[12], q[5];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 8, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[10], q[11], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 8, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[10], q[11];
// UNMAPPED c6x [0, 1, 2, 3, 4, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[11], q[9];
// UNMAPPED c6x [0, 1, 2, 3, 4, 11, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[11], q[6];
// UNMAPPED c6x [0, 1, 2, 3, 4, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[12], q[11];
// UNMAPPED c6x [0, 1, 2, 3, 4, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[12], q[10];
// UNMAPPED c7x [0, 1, 2, 3, 4, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[10], q[11], q[12];
// UNMAPPED c5x [0, 1, 2, 3, 4, 12]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[4], q[12];
// UNMAPPED c5x [0, 1, 2, 3, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[4], q[11];
// UNMAPPED c5x [0, 1, 2, 3, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[4], q[10];
// UNMAPPED c5x [0, 1, 2, 3, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[4], q[9];
// UNMAPPED c5x [0, 1, 2, 3, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[4], q[8];
// UNMAPPED c5x [0, 1, 2, 3, 4, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[4], q[7];
// UNMAPPED c5x [0, 1, 2, 3, 4, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[4], q[6];
// UNMAPPED c12x [0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c12x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[4];
// UNMAPPED c12x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c12x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[10], q[11], q[7];
// UNMAPPED c11x [0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 4]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[4];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[10], q[11], q[9];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 7, 8, 10, 11, 5]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[10], q[11], q[5];
// UNMAPPED c11x [0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[9], q[10], q[12], q[11];
// UNMAPPED c11x [0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[9], q[10], q[12], q[4];
// UNMAPPED c12x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c12x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[11], q[10];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 7, 8, 9, 11, 6]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[11], q[6];
// UNMAPPED c10x [0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[9], q[10], q[12];
// UNMAPPED c10x [0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[9], q[10], q[11];
// UNMAPPED c10x [0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 4]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[9], q[10], q[4];
// UNMAPPED c12x [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c12x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[10], q[11], q[12], q[7];
// UNMAPPED c11x [0, 1, 2, 3, 5, 6, 7, 8, 9, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[9], q[11], q[12], q[10];
// UNMAPPED c11x [0, 1, 2, 3, 5, 6, 7, 8, 9, 11, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[9], q[11], q[12], q[4];
// UNMAPPED c12x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c12x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 8]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[10], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 9, 10, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[10], q[7];
// UNMAPPED c10x [0, 1, 2, 3, 5, 6, 7, 8, 9, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[9], q[11], q[12];
// UNMAPPED c10x [0, 1, 2, 3, 5, 6, 7, 8, 9, 11, 4]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[9], q[11], q[4];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[12], q[11];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[12], q[9];
// UNMAPPED c10x [0, 1, 2, 3, 5, 6, 7, 8, 9, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[9], q[12], q[11];
// UNMAPPED c10x [0, 1, 2, 3, 5, 6, 7, 8, 9, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[9], q[12], q[4];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 9, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[11], q[12], q[8];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 9, 11, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[11], q[12], q[7];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 7, 8, 9, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[9], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 7, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[9], q[4];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[12], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 8, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[12], q[6];
// UNMAPPED c11x [0, 1, 2, 3, 5, 6, 7, 8, 10, 11, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[10], q[11], q[12], q[4];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[11], q[12], q[10];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 7, 8, 11, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[11], q[12], q[6];
// UNMAPPED c10x [0, 1, 2, 3, 5, 6, 7, 8, 10, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[10], q[11], q[9];
// UNMAPPED c10x [0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[9], q[10], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 7, 8, 9, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[9], q[10];
// UNMAPPED c10x [0, 1, 2, 3, 5, 6, 7, 8, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[10], q[12], q[11];
// UNMAPPED c10x [0, 1, 2, 3, 5, 6, 7, 8, 10, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[10], q[12], q[4];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[10], q[11], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 7, 8, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[10], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 7, 8, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[10], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 7, 8, 10, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[10], q[9];
// UNMAPPED c11x [0, 1, 2, 3, 5, 6, 7, 8, 9, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[9], q[11], q[12], q[10];
// UNMAPPED c10x [0, 1, 2, 3, 5, 6, 7, 8, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[11], q[12], q[10];
// UNMAPPED c10x [0, 1, 2, 3, 5, 6, 7, 8, 11, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[11], q[12], q[4];
// UNMAPPED c11x [0, 1, 2, 3, 4, 6, 7, 8, 10, 11, 12, 5]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[10], q[11], q[12], q[5];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 7, 8, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[11], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 7, 8, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[11], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 7, 8, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[11], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 7, 8, 11, 4]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[11], q[4];
// UNMAPPED c12x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c12x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[12], q[11];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[10], q[12], q[8];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 7, 9, 10, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[9], q[10], q[12], q[6];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 7, 8, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[12], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 7, 8, 9, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[9], q[12];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 7, 8, 12]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[12];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 7, 8, 10]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 7, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[4];
// UNMAPPED c11x [0, 1, 2, 3, 5, 6, 7, 9, 10, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[9], q[10], q[11], q[12], q[8];
// UNMAPPED c11x [0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[9], q[10], q[12], q[11];
// UNMAPPED c10x [0, 1, 2, 3, 5, 6, 7, 8, 9, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[9], q[12], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 7, 8, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[12], q[9];
// UNMAPPED c10x [0, 1, 2, 3, 5, 6, 7, 9, 10, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[9], q[10], q[11], q[8];
// UNMAPPED c10x [0, 1, 2, 3, 5, 6, 7, 9, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[9], q[10], q[12], q[11];
// UNMAPPED c10x [0, 1, 2, 3, 5, 6, 7, 9, 10, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[9], q[10], q[12], q[8];
// UNMAPPED c10x [0, 1, 2, 3, 5, 6, 7, 9, 10, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[9], q[10], q[12], q[4];
// UNMAPPED c12x [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c12x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[10], q[11], q[12], q[6];
// UNMAPPED c11x [0, 1, 2, 3, 4, 7, 8, 9, 10, 11, 12, 5]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[9], q[10], q[11], q[12], q[5];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 7, 9, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[9], q[10], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 7, 9, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[9], q[10], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 7, 9, 10, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[9], q[10], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 7, 9, 10, 4]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[9], q[10], q[4];
// UNMAPPED c12x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c12x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[11], q[12], q[10];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[11], q[12], q[9];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 8, 11, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[11], q[12], q[7];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 8, 11, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[11], q[12], q[6];
// UNMAPPED c10x [0, 1, 2, 3, 5, 6, 7, 9, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[9], q[11], q[12], q[10];
// UNMAPPED c10x [0, 1, 2, 3, 5, 6, 7, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[9], q[10], q[11], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 7, 9, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[9], q[10], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 7, 9, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[9], q[11], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 7, 9, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[9], q[11], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 7, 9, 11, 4]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[9], q[11], q[4];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 9]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[10], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 8, 10, 6]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[10], q[6];
// UNMAPPED c8x [0, 1, 2, 3, 4, 7, 8, 10, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[10], q[5];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 7, 9, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[9], q[12], q[4];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 9, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[12];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[9], q[8];
// UNMAPPED c10x [0, 1, 2, 3, 5, 6, 7, 10, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[10], q[11], q[12], q[8];
// UNMAPPED c10x [0, 1, 2, 3, 5, 6, 7, 10, 11, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[10], q[11], q[12], q[4];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 7, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[10], q[11], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 7, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[10], q[12], q[11];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 7, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[10], q[11];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 7, 10, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[10], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 7, 10, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[10], q[4];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 8, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[11], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 8, 11, 6]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[11], q[6];
// UNMAPPED c8x [0, 1, 2, 3, 4, 7, 8, 11, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[11], q[5];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 7, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[11], q[12], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 7, 11, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[11], q[12], q[4];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[10], q[11], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 10, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[10], q[11], q[7];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 7, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[11], q[12];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 7, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[11], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 7, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[11], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 7, 11, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[11], q[4];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 7, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[12], q[11];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 7, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[12], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 7, 8, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[11], q[12];
// UNMAPPED c7x [0, 1, 2, 3, 5, 6, 7, 12]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[12];
// UNMAPPED c7x [0, 1, 2, 3, 5, 6, 7, 11]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[11];
// UNMAPPED c7x [0, 1, 2, 3, 5, 6, 7, 10]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[10];
// UNMAPPED c7x [0, 1, 2, 3, 5, 6, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 5, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 5, 6, 7, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[4];
// UNMAPPED c11x [0, 1, 2, 3, 5, 6, 8, 9, 10, 11, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[9], q[10], q[11], q[12], q[7];
// UNMAPPED c11x [0, 1, 2, 3, 5, 6, 8, 9, 10, 11, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[9], q[10], q[11], q[12], q[4];
// UNMAPPED c12x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c12x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[12], q[11];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[12], q[10];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[12], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[12], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 7, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[12], q[6];
// UNMAPPED c10x [0, 1, 2, 3, 5, 6, 8, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[9], q[10], q[11], q[12];
// UNMAPPED c10x [0, 1, 2, 3, 5, 6, 8, 9, 10, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[9], q[10], q[11], q[7];
// UNMAPPED c10x [0, 1, 2, 3, 5, 6, 8, 9, 10, 11, 4]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[9], q[10], q[11], q[4];
// UNMAPPED c12x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c12x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[12], q[11];
// UNMAPPED c11x [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 12, 5]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[10], q[12], q[5];
// UNMAPPED c10x [0, 1, 2, 3, 5, 6, 8, 9, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[9], q[10], q[12], q[11];
// UNMAPPED c10x [0, 1, 2, 3, 5, 6, 8, 9, 10, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[9], q[10], q[12], q[7];
// UNMAPPED c11x [0, 1, 2, 3, 5, 6, 7, 8, 9, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[9], q[11], q[12], q[10];
// UNMAPPED c10x [0, 1, 2, 3, 5, 6, 7, 9, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[9], q[11], q[12], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 8, 9, 10, 4]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[9], q[10], q[4];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 9, 10, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[10], q[8];
// UNMAPPED c10x [0, 1, 2, 3, 5, 6, 8, 9, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[9], q[11], q[12], q[10];
// UNMAPPED c10x [0, 1, 2, 3, 5, 6, 8, 9, 11, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[9], q[11], q[12], q[7];
// UNMAPPED c10x [0, 1, 2, 3, 5, 6, 8, 9, 11, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[9], q[11], q[12], q[4];
// UNMAPPED c12x [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c12x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[10], q[11], q[12], q[9];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[10], q[11], q[12], q[8];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 7, 10, 11, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[10], q[11], q[12], q[6];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 8, 9, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[9], q[11], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 8, 9, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[9], q[11], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 8, 9, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[9], q[11], q[7];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 8, 9, 11, 4]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[9], q[11], q[4];
// UNMAPPED c12x [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c12x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[10], q[11], q[12], q[9];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[10], q[11], q[12], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 8, 9, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[9], q[12], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 8, 9, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[9], q[12], q[7];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 8, 9, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[9], q[12], q[4];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[11], q[12];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 7, 8, 9, 11, 5]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[11], q[5];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 8, 9, 11]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[9], q[11];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 8, 9, 10]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[9], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[9], q[4];
// UNMAPPED c10x [0, 1, 2, 3, 5, 6, 8, 10, 11, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[10], q[11], q[12], q[9];
// UNMAPPED c10x [0, 1, 2, 3, 5, 6, 8, 10, 11, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[10], q[11], q[12], q[4];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 9, 10, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[10], q[11], q[12], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 8, 10, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[10], q[11], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 8, 10, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[10], q[11], q[7];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 8, 10, 11, 4]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[10], q[11], q[4];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[10], q[11], q[8];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 7, 9, 10, 11, 6]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[9], q[10], q[11], q[6];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 8, 10, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[10], q[12], q[7];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 7, 8, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[10], q[12];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 7, 8, 10]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 8, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[10], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 8, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[11], q[12], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 8, 11, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[11], q[12], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 8, 11, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[11], q[12], q[4];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[10], q[11], q[12];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 8, 9, 10, 11, 6]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[9], q[10], q[11], q[6];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 8, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[11], q[12];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 8, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[11], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 8, 11, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[11], q[4];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 10, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[10], q[11], q[12], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 8, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[12], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 8, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[12], q[4];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 8, 9, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[12];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[9], q[6];
// UNMAPPED c7x [0, 1, 2, 3, 5, 6, 8, 12]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[12];
// UNMAPPED c7x [0, 1, 2, 3, 5, 6, 8, 10]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[10];
// UNMAPPED c7x [0, 1, 2, 3, 5, 6, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 5, 6, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[6], q[8], q[4];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 8, 9, 10, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[9], q[10], q[12], q[6];
// UNMAPPED c10x [0, 1, 2, 3, 5, 6, 9, 10, 11, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[6], q[9], q[10], q[11], q[12], q[4];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[10], q[11], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 9, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[10], q[11];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 9, 10]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[10];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 6, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 9, 10, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[9], q[10], q[11], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 9, 10, 11, 4]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[9], q[10], q[11], q[4];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 8, 9, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[11], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 8, 9, 11, 6]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[9], q[11], q[6];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 9, 10, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[9], q[10], q[12], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 9, 10, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[9], q[10], q[12], q[7];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 9, 10, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[9], q[10], q[12], q[4];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[12];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[6];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 9, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[9], q[10], q[11];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 9, 10, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[9], q[10], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 9, 10, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[9], q[10], q[4];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 8, 10, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[10], q[11], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 8, 10, 11, 6]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[10], q[11], q[6];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 9, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[9], q[11], q[12], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 9, 11, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[9], q[11], q[12], q[4];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 8, 9, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[11], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 8, 9, 11]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[11];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 9, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[9], q[11], q[7];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 9, 11, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[9], q[11], q[4];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 9, 11]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[11];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 9, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[9], q[12], q[11];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 9, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[9], q[12], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 9, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[9], q[12], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 9, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[9], q[12], q[4];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[10], q[11], q[12];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 8, 9, 10, 11, 6]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[9], q[10], q[11], q[6];
// UNMAPPED c7x [0, 1, 2, 3, 5, 6, 9, 11]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[6], q[9], q[11];
// UNMAPPED c7x [0, 1, 2, 3, 5, 6, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[6], q[9], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 5, 6, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[6], q[9], q[7];
// UNMAPPED c7x [0, 1, 2, 3, 5, 6, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[6], q[9], q[4];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 8, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[11], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 10, 11, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[10], q[11], q[12], q[7];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 10, 11, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[10], q[11], q[12], q[4];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[10], q[12], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[12], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[10], q[11], q[12];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 10, 11, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[10], q[11], q[4];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[11], q[12], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 10, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[10], q[12], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 10, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[10], q[12], q[7];
// UNMAPPED c9x [0, 1, 2, 3, 5, 6, 7, 8, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[10], q[12];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 7, 8, 10]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[7], q[8], q[10];
// UNMAPPED c7x [0, 1, 2, 3, 5, 6, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[6], q[10], q[12];
// UNMAPPED c7x [0, 1, 2, 3, 5, 6, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[6], q[10], q[11];
// UNMAPPED c7x [0, 1, 2, 3, 5, 6, 10, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[6], q[10], q[7];
// UNMAPPED c7x [0, 1, 2, 3, 5, 6, 10, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[6], q[10], q[4];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[11], q[12], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 11, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[11], q[12], q[6];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[11], q[12], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 5, 6, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[6], q[10], q[12], q[11];
// UNMAPPED c7x [0, 1, 2, 3, 5, 6, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[6], q[11], q[12];
// UNMAPPED c7x [0, 1, 2, 3, 5, 6, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[6], q[11], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 5, 6, 11, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[6], q[11], q[4];
// UNMAPPED c7x [0, 1, 2, 3, 5, 6, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[6], q[12], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 5, 6, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[6], q[12], q[4];
// UNMAPPED c6x [0, 1, 2, 3, 5, 6, 12]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[6], q[12];
// UNMAPPED c6x [0, 1, 2, 3, 5, 6, 10]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[6], q[10];
// UNMAPPED c6x [0, 1, 2, 3, 5, 6, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[6], q[9];
// UNMAPPED c6x [0, 1, 2, 3, 5, 6, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[6], q[7];
// UNMAPPED c6x [0, 1, 2, 3, 5, 6, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[6], q[4];
// UNMAPPED c11x [0, 1, 2, 3, 5, 7, 8, 9, 10, 11, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[9], q[10], q[11], q[12], q[6];
// UNMAPPED c11x [0, 1, 2, 3, 5, 7, 8, 9, 10, 11, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[9], q[10], q[11], q[12], q[4];
// UNMAPPED c12x [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c12x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[10], q[11], q[12], q[9];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[10], q[11], q[12], q[8];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 10, 11, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[10], q[11], q[12], q[7];
// UNMAPPED c10x [0, 1, 2, 3, 5, 7, 8, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[9], q[10], q[11], q[12];
// UNMAPPED c10x [0, 1, 2, 3, 5, 7, 8, 9, 10, 11, 6]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[9], q[10], q[11], q[6];
// UNMAPPED c10x [0, 1, 2, 3, 5, 7, 8, 9, 10, 11, 4]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[9], q[10], q[11], q[4];
// UNMAPPED c12x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c12x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[12], q[11];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[12], q[10];
// UNMAPPED c10x [0, 1, 2, 3, 5, 7, 8, 9, 10, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[9], q[10], q[12], q[4];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 7, 9, 10, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[9], q[10], q[12], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 5, 7, 8, 9, 10, 4]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[9], q[10], q[4];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 8, 9, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9];
// UNMAPPED c10x [0, 1, 2, 3, 5, 7, 8, 9, 11, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[9], q[11], q[12], q[4];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 7, 8, 9, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[12], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 8, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[12], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 7, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[12], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 5, 7, 8, 9, 11, 4]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[9], q[11], q[4];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 8, 9, 11]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[11];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[8], q[9], q[7];
// UNMAPPED c9x [0, 1, 2, 3, 5, 7, 8, 9, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[9], q[12], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 5, 7, 8, 9, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[9], q[12], q[6];
// UNMAPPED c9x [0, 1, 2, 3, 5, 7, 8, 9, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[9], q[12], q[4];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[10], q[12], q[8];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 9, 10, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[9], q[10], q[12], q[7];
// UNMAPPED c8x [0, 1, 2, 3, 5, 7, 8, 9, 12]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[9], q[12];
// UNMAPPED c8x [0, 1, 2, 3, 5, 7, 8, 9, 11]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[9], q[11];
// UNMAPPED c8x [0, 1, 2, 3, 5, 7, 8, 9, 10]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[9], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 5, 7, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[9], q[4];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 7, 9, 10, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[9], q[10], q[11], q[12], q[8];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 9, 10, 11, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[9], q[10], q[11], q[12], q[7];
// UNMAPPED c10x [0, 1, 2, 3, 5, 7, 8, 10, 11, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[10], q[11], q[12], q[6];
// UNMAPPED c10x [0, 1, 2, 3, 5, 7, 8, 10, 11, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[10], q[11], q[12], q[4];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[10], q[11], q[12];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 8, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[11], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[11], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 5, 7, 8, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[10], q[11], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 5, 7, 8, 10, 11, 6]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[10], q[11], q[6];
// UNMAPPED c9x [0, 1, 2, 3, 5, 7, 8, 10, 11, 4]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[10], q[11], q[4];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[10], q[11], q[12], q[8];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 10, 11, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[10], q[11], q[12], q[7];
// UNMAPPED c9x [0, 1, 2, 3, 5, 7, 8, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[10], q[12], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 5, 7, 8, 10, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[10], q[12], q[9];
// UNMAPPED c10x [0, 1, 2, 3, 5, 7, 8, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[9], q[10], q[11], q[12];
// UNMAPPED c8x [0, 1, 2, 3, 5, 7, 8, 10, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[10], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 5, 7, 8, 10, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[10], q[4];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 8, 9, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[9], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 5, 7, 8, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[11], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 5, 7, 8, 11, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[11], q[4];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 8, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[10], q[11];
// UNMAPPED c8x [0, 1, 2, 3, 5, 7, 8, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[12], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 5, 7, 8, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[12], q[6];
// UNMAPPED c8x [0, 1, 2, 3, 5, 7, 8, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[12], q[4];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 5, 7, 8, 11]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[11];
// UNMAPPED c7x [0, 1, 2, 3, 5, 7, 8, 10]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[10];
// UNMAPPED c7x [0, 1, 2, 3, 5, 7, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[6];
// UNMAPPED c10x [0, 1, 2, 3, 5, 7, 9, 10, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[7], q[9], q[10], q[11], q[12], q[8];
// UNMAPPED c10x [0, 1, 2, 3, 5, 7, 9, 10, 11, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[7], q[9], q[10], q[11], q[12], q[4];
// UNMAPPED c9x [0, 1, 2, 3, 5, 7, 9, 10, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[7], q[9], q[10], q[11], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 5, 7, 9, 10, 11, 4]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[7], q[9], q[10], q[11], q[4];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 7, 8, 9, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[11], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 5, 7, 9, 10, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[7], q[9], q[10], q[12], q[6];
// UNMAPPED c9x [0, 1, 2, 3, 5, 7, 9, 10, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[7], q[9], q[10], q[12], q[4];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[10], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 9, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 7, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 6, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7];
// UNMAPPED c8x [0, 1, 2, 3, 5, 7, 9, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[7], q[9], q[10], q[12];
// UNMAPPED c8x [0, 1, 2, 3, 5, 7, 9, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[7], q[9], q[10], q[11];
// UNMAPPED c8x [0, 1, 2, 3, 5, 7, 9, 10, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[7], q[9], q[10], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 5, 7, 9, 10, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[7], q[9], q[10], q[6];
// UNMAPPED c8x [0, 1, 2, 3, 5, 7, 9, 10, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[7], q[9], q[10], q[4];
// UNMAPPED c12x [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c12x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[10], q[11], q[12], q[7];
// UNMAPPED c9x [0, 1, 2, 3, 5, 7, 9, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[7], q[9], q[11], q[12], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 5, 7, 9, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[7], q[9], q[11], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 5, 7, 8, 9, 11]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[9], q[11];
// UNMAPPED c7x [0, 1, 2, 3, 5, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 5, 7, 9, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[7], q[9], q[12], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 5, 7, 9, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[7], q[9], q[12], q[6];
// UNMAPPED c8x [0, 1, 2, 3, 5, 7, 9, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[7], q[9], q[12], q[4];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 5, 7, 9, 10]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[7], q[9], q[10];
// UNMAPPED c7x [0, 1, 2, 3, 5, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[7], q[9], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 5, 7, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[7], q[9], q[4];
// UNMAPPED c9x [0, 1, 2, 3, 4, 7, 8, 9, 10, 5]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[9], q[10], q[5];
// UNMAPPED c9x [0, 1, 2, 3, 5, 7, 10, 11, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[7], q[10], q[11], q[12], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 5, 7, 10, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[7], q[10], q[11], q[12], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 5, 7, 10, 11, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[7], q[10], q[11], q[12], q[6];
// UNMAPPED c9x [0, 1, 2, 3, 5, 7, 10, 11, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[7], q[10], q[11], q[12], q[4];
// UNMAPPED c12x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c12x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12];
// UNMAPPED c8x [0, 1, 2, 3, 5, 7, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[7], q[10], q[11], q[12];
// UNMAPPED c8x [0, 1, 2, 3, 5, 7, 10, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[7], q[10], q[11], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 5, 7, 10, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[7], q[10], q[11], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 5, 7, 10, 11, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[7], q[10], q[11], q[6];
// UNMAPPED c8x [0, 1, 2, 3, 5, 7, 10, 11, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[7], q[10], q[11], q[4];
// UNMAPPED c12x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c12x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[11], q[12], q[10];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 6, 8, 9, 11, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[11], q[12], q[7];
// UNMAPPED c8x [0, 1, 2, 3, 5, 7, 10, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[7], q[10], q[12], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 5, 7, 10, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[7], q[10], q[12], q[6];
// UNMAPPED c8x [0, 1, 2, 3, 5, 7, 10, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[7], q[10], q[12], q[4];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[10], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 7, 8, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[7];
// UNMAPPED c7x [0, 1, 2, 3, 5, 7, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[7], q[10], q[11];
// UNMAPPED c7x [0, 1, 2, 3, 5, 7, 10, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[7], q[10], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 5, 7, 10, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[7], q[10], q[6];
// UNMAPPED c7x [0, 1, 2, 3, 5, 7, 10, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[7], q[10], q[4];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 8, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[11], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 5, 7, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[7], q[11], q[12], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 5, 7, 11, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[7], q[11], q[12], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 5, 7, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[7], q[11], q[12], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 5, 7, 11, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[7], q[11], q[12], q[6];
// UNMAPPED c8x [0, 1, 2, 3, 5, 7, 11, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[7], q[11], q[12], q[4];
// UNMAPPED c7x [0, 1, 2, 3, 5, 7, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[7], q[11], q[10];
// UNMAPPED c7x [0, 1, 2, 3, 5, 7, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[7], q[11], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 5, 7, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[7], q[11], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 5, 7, 11, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[7], q[11], q[6];
// UNMAPPED c7x [0, 1, 2, 3, 5, 7, 11, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[7], q[11], q[4];
// UNMAPPED c7x [0, 1, 2, 3, 5, 7, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[7], q[12], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 5, 7, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[7], q[12], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 5, 7, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[7], q[12], q[6];
// UNMAPPED c7x [0, 1, 2, 3, 5, 7, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[7], q[12], q[4];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[7];
// UNMAPPED c6x [0, 1, 2, 3, 5, 7, 12]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[7], q[12];
// UNMAPPED c6x [0, 1, 2, 3, 5, 7, 10]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[7], q[10];
// UNMAPPED c6x [0, 1, 2, 3, 5, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[7], q[8];
// UNMAPPED c10x [0, 1, 2, 3, 5, 8, 9, 10, 11, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[8], q[9], q[10], q[11], q[12], q[7];
// UNMAPPED c10x [0, 1, 2, 3, 5, 8, 9, 10, 11, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[8], q[9], q[10], q[11], q[12], q[4];
// UNMAPPED c9x [0, 1, 2, 3, 5, 8, 9, 10, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[8], q[9], q[10], q[11], q[7];
// UNMAPPED c9x [0, 1, 2, 3, 5, 8, 9, 10, 11, 4]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[8], q[9], q[10], q[11], q[4];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[10], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 4, 7, 8, 9, 10, 5]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[9], q[10], q[5];
// UNMAPPED c9x [0, 1, 2, 3, 5, 8, 9, 10, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[8], q[9], q[10], q[12], q[6];
// UNMAPPED c9x [0, 1, 2, 3, 5, 8, 9, 10, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[8], q[9], q[10], q[12], q[4];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[10], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 6, 8, 9, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 4, 5, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 5, 8, 9, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[8], q[9], q[10], q[12];
// UNMAPPED c8x [0, 1, 2, 3, 5, 8, 9, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[8], q[9], q[10], q[11];
// UNMAPPED c8x [0, 1, 2, 3, 5, 8, 9, 10, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[8], q[9], q[10], q[7];
// UNMAPPED c8x [0, 1, 2, 3, 5, 8, 9, 10, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[8], q[9], q[10], q[4];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 7, 8, 9, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[11], q[12], q[10];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 7, 8, 11, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[11], q[12], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 5, 8, 9, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[8], q[9], q[11], q[12], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 5, 8, 9, 11, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[8], q[9], q[11], q[12], q[7];
// UNMAPPED c8x [0, 1, 2, 3, 5, 8, 9, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[8], q[9], q[11], q[12];
// UNMAPPED c8x [0, 1, 2, 3, 5, 8, 9, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[8], q[9], q[11], q[7];
// UNMAPPED c9x [0, 1, 2, 3, 5, 7, 9, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[7], q[9], q[11], q[12], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 5, 8, 9, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[8], q[9], q[12], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 5, 8, 9, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[8], q[9], q[12], q[7];
// UNMAPPED c9x [0, 1, 2, 3, 5, 7, 9, 10, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[7], q[9], q[10], q[12], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 5, 8, 9, 12]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[8], q[9], q[12];
// UNMAPPED c7x [0, 1, 2, 3, 5, 8, 9, 11]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[8], q[9], q[11];
// UNMAPPED c7x [0, 1, 2, 3, 5, 8, 9, 10]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[8], q[9], q[10];
// UNMAPPED c7x [0, 1, 2, 3, 5, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[8], q[9], q[7];
// UNMAPPED c10x [0, 1, 2, 3, 5, 7, 8, 10, 11, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[10], q[11], q[12], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 5, 8, 10, 11, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[8], q[10], q[11], q[12], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 5, 8, 10, 11, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[8], q[10], q[11], q[12], q[4];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 9, 10, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[9], q[10], q[11], q[12], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 5, 8, 10, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[8], q[10], q[11], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 5, 8, 10, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[8], q[10], q[11], q[7];
// UNMAPPED c9x [0, 1, 2, 3, 5, 7, 9, 10, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[7], q[9], q[10], q[11], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 5, 8, 10, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[8], q[10], q[12], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 5, 8, 10, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[8], q[10], q[12], q[7];
// UNMAPPED c9x [0, 1, 2, 3, 5, 7, 8, 9, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[9], q[10], q[12];
// UNMAPPED c8x [0, 1, 2, 3, 5, 7, 9, 10, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[7], q[9], q[10], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 5, 8, 11, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[8], q[11], q[12], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 5, 8, 11, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[8], q[11], q[12], q[7];
// UNMAPPED c8x [0, 1, 2, 3, 5, 8, 11, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[8], q[11], q[12], q[4];
// UNMAPPED c10x [0, 1, 2, 3, 4, 5, 7, 8, 9, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[11], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 5, 7, 8, 9, 11]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[11];
// UNMAPPED c8x [0, 1, 2, 3, 4, 7, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[9], q[5];
// UNMAPPED c7x [0, 1, 2, 3, 5, 8, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[8], q[11], q[10];
// UNMAPPED c7x [0, 1, 2, 3, 5, 8, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[8], q[11], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 5, 8, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[8], q[11], q[7];
// UNMAPPED c9x [0, 1, 2, 3, 5, 7, 9, 10, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[7], q[9], q[10], q[11], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 5, 8, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[8], q[12], q[11];
// UNMAPPED c7x [0, 1, 2, 3, 5, 8, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[8], q[12], q[10];
// UNMAPPED c7x [0, 1, 2, 3, 5, 8, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[8], q[12], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 5, 8, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[8], q[12], q[7];
// UNMAPPED c6x [0, 1, 2, 3, 5, 8, 12]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[8], q[12];
// UNMAPPED c6x [0, 1, 2, 3, 5, 8, 11]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[8], q[11];
// UNMAPPED c6x [0, 1, 2, 3, 5, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[8], q[7];
// UNMAPPED c9x [0, 1, 2, 3, 5, 9, 10, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[9], q[10], q[11], q[12], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 5, 9, 10, 11, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[9], q[10], q[11], q[12], q[7];
// UNMAPPED c9x [0, 1, 2, 3, 5, 9, 10, 11, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[9], q[10], q[11], q[12], q[4];
// UNMAPPED c11x [0, 1, 2, 3, 4, 5, 7, 8, 9, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[11], q[12], q[10];
// UNMAPPED c10x [0, 1, 2, 3, 4, 7, 8, 9, 11, 12, 5]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[9], q[11], q[12], q[5];
// UNMAPPED c8x [0, 1, 2, 3, 5, 9, 10, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[9], q[10], q[11], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 5, 9, 10, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[9], q[10], q[11], q[7];
// UNMAPPED c9x [0, 1, 2, 3, 5, 7, 8, 9, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[9], q[10], q[11];
// UNMAPPED c8x [0, 1, 2, 3, 5, 7, 8, 9, 10]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[9], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 5, 9, 10, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[9], q[10], q[12], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 5, 9, 10, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[9], q[10], q[12], q[7];
// UNMAPPED c9x [0, 1, 2, 3, 5, 7, 8, 9, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[9], q[10], q[12];
// UNMAPPED c7x [0, 1, 2, 3, 5, 9, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[9], q[10], q[11];
// UNMAPPED c7x [0, 1, 2, 3, 5, 9, 10, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[9], q[10], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 5, 9, 11, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[9], q[11], q[12], q[7];
// UNMAPPED c8x [0, 1, 2, 3, 5, 7, 11, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[7], q[11], q[12], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 5, 9, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[9], q[11], q[12];
// UNMAPPED c7x [0, 1, 2, 3, 5, 9, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[9], q[11], q[10];
// UNMAPPED c7x [0, 1, 2, 3, 5, 9, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[9], q[11], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 5, 9, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[9], q[11], q[7];
// UNMAPPED c10x [0, 1, 2, 3, 5, 7, 8, 9, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[9], q[10], q[12], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 5, 7, 8, 10, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[10], q[12], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 5, 9, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[9], q[12], q[7];
// UNMAPPED c7x [0, 1, 2, 3, 5, 7, 9, 12]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[7], q[9], q[12];
// UNMAPPED c6x [0, 1, 2, 3, 5, 9, 11]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[9], q[11];
// UNMAPPED c6x [0, 1, 2, 3, 5, 9, 10]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[9], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 5, 10, 11, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[10], q[11], q[12], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 5, 10, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[10], q[11], q[12], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 5, 10, 11, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[5], q[10], q[11], q[12], q[7];
// UNMAPPED c10x [0, 1, 2, 3, 5, 7, 8, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[9], q[10], q[11], q[12];
// UNMAPPED c7x [0, 1, 2, 3, 5, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[10], q[11], q[12];
// UNMAPPED c7x [0, 1, 2, 3, 5, 10, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[10], q[11], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 5, 10, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[10], q[11], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 5, 10, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[10], q[11], q[7];
// UNMAPPED c10x [0, 1, 2, 3, 5, 7, 8, 9, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[9], q[10], q[12], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 5, 7, 8, 9, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[9], q[12], q[10];
// UNMAPPED c7x [0, 1, 2, 3, 5, 10, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[10], q[12], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 5, 10, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[10], q[12], q[7];
// UNMAPPED c6x [0, 1, 2, 3, 5, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[10], q[12];
// UNMAPPED c6x [0, 1, 2, 3, 5, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[10], q[11];
// UNMAPPED c7x [0, 1, 2, 3, 5, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[11], q[12], q[10];
// UNMAPPED c7x [0, 1, 2, 3, 5, 11, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[11], q[12], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 5, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[11], q[12], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 5, 11, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[5], q[11], q[12], q[7];
// UNMAPPED c10x [0, 1, 2, 3, 5, 7, 8, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[5], q[7], q[8], q[9], q[10], q[11], q[12];
// UNMAPPED c6x [0, 1, 2, 3, 5, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[11], q[12];
// UNMAPPED c6x [0, 1, 2, 3, 5, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[11], q[9];
// UNMAPPED c6x [0, 1, 2, 3, 5, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[11], q[8];
// UNMAPPED c6x [0, 1, 2, 3, 5, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[11], q[7];
// UNMAPPED c6x [0, 1, 2, 3, 5, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[12], q[11];
// UNMAPPED c6x [0, 1, 2, 3, 5, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[12], q[9];
// UNMAPPED c6x [0, 1, 2, 3, 5, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[12], q[8];
// UNMAPPED c6x [0, 1, 2, 3, 5, 12, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[5], q[12], q[7];
// UNMAPPED c5x [0, 1, 2, 3, 5, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[5], q[6];
// UNMAPPED c5x [0, 1, 2, 3, 5, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[2], q[3], q[5], q[4];
// UNMAPPED c6x [0, 1, 2, 3, 4, 6, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[2], q[3], q[4], q[6], q[5];
// UNMAPPED c11x [0, 1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[4];
// UNMAPPED c11x [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[10], q[12], q[11];
// UNMAPPED c10x [0, 1, 2, 3, 6, 7, 8, 9, 10, 11, 4]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[6], q[7], q[8], q[9], q[10], q[11], q[4];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[10], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 7, 8, 10, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[10], q[9];
// UNMAPPED c10x [0, 1, 2, 3, 6, 7, 8, 9, 10, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[6], q[7], q[8], q[9], q[10], q[12], q[4];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[10], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 7, 8, 9, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 4, 7, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[9], q[6];
// UNMAPPED c9x [0, 1, 2, 3, 6, 7, 8, 9, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[6], q[7], q[8], q[9], q[10], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 6, 7, 8, 9, 10, 4]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[6], q[7], q[8], q[9], q[10], q[4];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 7, 8, 9, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[12], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 4, 7, 8, 9, 12, 6]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[9], q[12], q[6];
// UNMAPPED c10x [0, 1, 2, 3, 6, 7, 8, 9, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[6], q[7], q[8], q[9], q[11], q[12], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 6, 7, 8, 9, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[6], q[7], q[8], q[9], q[11], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 6, 7, 8, 9, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[6], q[7], q[8], q[9], q[11], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 6, 7, 8, 9, 11, 4]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[6], q[7], q[8], q[9], q[11], q[4];
// UNMAPPED c11x [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[10], q[12], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 6, 7, 8, 9, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[6], q[7], q[8], q[9], q[12], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 6, 7, 8, 9, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[6], q[7], q[8], q[9], q[12], q[4];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[10], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 7, 8, 10, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[10], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 7, 8, 10, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[10], q[6];
// UNMAPPED c8x [0, 1, 2, 3, 6, 7, 8, 9, 10]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[6], q[7], q[8], q[9], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 6, 7, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[6], q[7], q[8], q[9], q[4];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 7, 8, 10, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[10], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 7, 8, 10, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[10], q[6];
// UNMAPPED c10x [0, 1, 2, 3, 6, 7, 8, 10, 11, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[6], q[7], q[8], q[10], q[11], q[12], q[4];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 7, 8, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[10], q[12], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 6, 7, 8, 10, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[6], q[7], q[8], q[10], q[11], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 6, 7, 8, 9, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[6], q[7], q[8], q[9], q[11], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 6, 7, 8, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[6], q[7], q[8], q[10], q[12], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 6, 7, 8, 10, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[6], q[7], q[8], q[10], q[12], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 6, 7, 8, 10, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[6], q[7], q[8], q[10], q[12], q[4];
// UNMAPPED c11x [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[10], q[11], q[12];
// UNMAPPED c8x [0, 1, 2, 3, 6, 7, 8, 10, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[6], q[7], q[8], q[10], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 6, 7, 8, 10, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[6], q[7], q[8], q[10], q[4];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 7, 8, 9, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 4, 7, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[9], q[6];
// UNMAPPED c8x [0, 1, 2, 3, 6, 7, 8, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[6], q[7], q[8], q[11], q[12];
// UNMAPPED c8x [0, 1, 2, 3, 6, 7, 8, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[6], q[7], q[8], q[11], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 6, 7, 8, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[6], q[7], q[8], q[11], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 6, 7, 8, 11, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[6], q[7], q[8], q[11], q[4];
// UNMAPPED c11x [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[10], q[12], q[11];
// UNMAPPED c8x [0, 1, 2, 3, 6, 7, 8, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[6], q[7], q[8], q[12], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 6, 7, 8, 12, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[6], q[7], q[8], q[12], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 6, 7, 8, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[6], q[7], q[8], q[12], q[4];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[10], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 7, 8, 9, 10, 6]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[9], q[10], q[6];
// UNMAPPED c7x [0, 1, 2, 3, 6, 7, 8, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[6], q[7], q[8], q[9];
// UNMAPPED c7x [0, 1, 2, 3, 6, 7, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[6], q[7], q[8], q[4];
// UNMAPPED c8x [0, 1, 2, 3, 4, 7, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[9], q[6];
// UNMAPPED c10x [0, 1, 2, 3, 6, 7, 9, 10, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[6], q[7], q[9], q[10], q[11], q[12], q[8];
// UNMAPPED c10x [0, 1, 2, 3, 6, 7, 9, 10, 11, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[6], q[7], q[9], q[10], q[11], q[12], q[4];
// UNMAPPED c11x [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[10], q[11], q[12];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[10], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 6, 7, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[6], q[7], q[9], q[10], q[11], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 6, 7, 9, 10, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[6], q[7], q[9], q[10], q[11], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 6, 7, 9, 10, 11, 4]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[6], q[7], q[9], q[10], q[11], q[4];
// UNMAPPED c11x [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[10], q[12], q[11];
// UNMAPPED c9x [0, 1, 2, 3, 6, 7, 9, 10, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[6], q[7], q[9], q[10], q[12], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 6, 7, 9, 10, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[6], q[7], q[9], q[10], q[12], q[4];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[10], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 7, 8, 9, 10, 6]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[9], q[10], q[6];
// UNMAPPED c8x [0, 1, 2, 3, 6, 7, 9, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[6], q[7], q[9], q[10], q[11];
// UNMAPPED c8x [0, 1, 2, 3, 6, 7, 9, 10, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[6], q[7], q[9], q[10], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 6, 7, 9, 10, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[6], q[7], q[9], q[10], q[4];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 7, 8, 9, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[11], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 7, 8, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[11], q[9];
// UNMAPPED c9x [0, 1, 2, 3, 6, 7, 9, 11, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[6], q[7], q[9], q[11], q[12], q[10];
// UNMAPPED c9x [0, 1, 2, 3, 6, 7, 9, 11, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[6], q[7], q[9], q[11], q[12], q[8];
// UNMAPPED c9x [0, 1, 2, 3, 6, 7, 9, 11, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[6], q[7], q[9], q[11], q[12], q[4];
// UNMAPPED c11x [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[10], q[11], q[12];
// UNMAPPED c8x [0, 1, 2, 3, 6, 7, 9, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[6], q[7], q[9], q[11], q[12];
// UNMAPPED c8x [0, 1, 2, 3, 6, 7, 9, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[6], q[7], q[9], q[11], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 6, 7, 9, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[6], q[7], q[9], q[11], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 6, 7, 9, 11, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[6], q[7], q[9], q[11], q[4];
// UNMAPPED c11x [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[10], q[12], q[11];
// UNMAPPED c8x [0, 1, 2, 3, 6, 7, 9, 12, 10]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[6], q[7], q[9], q[12], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 6, 7, 9, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[6], q[7], q[9], q[12], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 6, 7, 9, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[6], q[7], q[9], q[12], q[4];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[10], q[12];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 7, 8, 10, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[10], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 7, 8, 10, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[10], q[6];
// UNMAPPED c7x [0, 1, 2, 3, 6, 7, 9, 10]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[6], q[7], q[9], q[10];
// UNMAPPED c7x [0, 1, 2, 3, 6, 7, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[6], q[7], q[9], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 6, 7, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[6], q[7], q[9], q[4];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 7, 8, 10, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[10], q[9];
// UNMAPPED c8x [0, 1, 2, 3, 4, 7, 8, 10, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[10], q[6];
// UNMAPPED c8x [0, 1, 2, 3, 6, 7, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[6], q[7], q[10], q[11], q[12];
// UNMAPPED c8x [0, 1, 2, 3, 6, 7, 10, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[6], q[7], q[10], q[11], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 6, 7, 10, 11, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[6], q[7], q[10], q[11], q[4];
// UNMAPPED c8x [0, 1, 2, 3, 6, 7, 10, 12, 11]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[6], q[7], q[10], q[12], q[11];
// UNMAPPED c8x [0, 1, 2, 3, 6, 7, 10, 12, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[6], q[7], q[10], q[12], q[8];
// UNMAPPED c8x [0, 1, 2, 3, 6, 7, 10, 12, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[6], q[7], q[10], q[12], q[4];
// UNMAPPED c10x [0, 1, 2, 3, 4, 6, 7, 8, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[10], q[11], q[12];
// UNMAPPED c7x [0, 1, 2, 3, 6, 7, 10, 11]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[6], q[7], q[10], q[11];
// UNMAPPED c7x [0, 1, 2, 3, 6, 7, 10, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[6], q[7], q[10], q[8];
// UNMAPPED c7x [0, 1, 2, 3, 6, 7, 10, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[2], q[3], q[6], q[7], q[10], q[4];
// UNMAPPED c9x [0, 1, 2, 3, 4, 6, 7, 8, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[2], q[3], q[4], q[6], q[7], q[8], q[11], q[10];
// UNMAPPED c8x [0, 1, 2, 3, 4, 7, 8, 11, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[7], q[8], q[11], q[6];
// UNMAPPED c11x [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 2]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[1], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[2];
// UNMAPPED c10x [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 2]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[2];
// UNMAPPED c10x [0, 1, 3, 4, 5, 6, 7, 8, 9, 11, 2]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[11], q[2];
// UNMAPPED c9x [0, 1, 3, 4, 5, 6, 7, 8, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[2];
// UNMAPPED c10x [0, 1, 3, 4, 5, 6, 7, 8, 10, 11, 2]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[3], q[4], q[5], q[6], q[7], q[8], q[10], q[11], q[2];
// UNMAPPED c9x [0, 1, 3, 4, 5, 6, 7, 8, 10, 2]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[3], q[4], q[5], q[6], q[7], q[8], q[10], q[2];
// UNMAPPED c9x [0, 1, 3, 4, 5, 6, 7, 8, 11, 2]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[3], q[4], q[5], q[6], q[7], q[8], q[11], q[2];
// UNMAPPED c6x [0, 1, 3, 4, 5, 6, 2]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[3], q[4], q[5], q[6], q[2];
// UNMAPPED c10x [0, 1, 3, 4, 5, 7, 8, 9, 10, 11, 2]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[3], q[4], q[5], q[7], q[8], q[9], q[10], q[11], q[2];
// UNMAPPED c9x [0, 1, 3, 4, 5, 7, 8, 9, 10, 2]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[3], q[4], q[5], q[7], q[8], q[9], q[10], q[2];
// UNMAPPED c9x [0, 1, 3, 4, 5, 7, 8, 9, 11, 2]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[3], q[4], q[5], q[7], q[8], q[9], q[11], q[2];
// UNMAPPED c8x [0, 1, 3, 4, 5, 7, 8, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[3], q[4], q[5], q[7], q[8], q[9], q[2];
// UNMAPPED c9x [0, 1, 3, 4, 5, 7, 8, 10, 11, 2]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[3], q[4], q[5], q[7], q[8], q[10], q[11], q[2];
// UNMAPPED c8x [0, 1, 3, 4, 5, 7, 8, 10, 2]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[3], q[4], q[5], q[7], q[8], q[10], q[2];
// UNMAPPED c8x [0, 1, 3, 4, 5, 7, 8, 11, 2]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[3], q[4], q[5], q[7], q[8], q[11], q[2];
// UNMAPPED c5x [0, 1, 3, 4, 5, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[4], q[5], q[2];
// UNMAPPED c10x [0, 1, 3, 4, 6, 7, 8, 9, 10, 11, 2]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[3], q[4], q[6], q[7], q[8], q[9], q[10], q[11], q[2];
// UNMAPPED c9x [0, 1, 3, 4, 6, 7, 8, 9, 10, 2]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[3], q[4], q[6], q[7], q[8], q[9], q[10], q[2];
// UNMAPPED c9x [0, 1, 3, 4, 6, 7, 8, 9, 11, 2]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[3], q[4], q[6], q[7], q[8], q[9], q[11], q[2];
// UNMAPPED c8x [0, 1, 3, 4, 6, 7, 8, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[3], q[4], q[6], q[7], q[8], q[9], q[2];
// UNMAPPED c9x [0, 1, 3, 4, 6, 7, 8, 10, 11, 2]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[3], q[4], q[6], q[7], q[8], q[10], q[11], q[2];
// UNMAPPED c8x [0, 1, 3, 4, 6, 7, 8, 10, 2]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[3], q[4], q[6], q[7], q[8], q[10], q[2];
// UNMAPPED c8x [0, 1, 3, 4, 6, 7, 8, 11, 2]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[3], q[4], q[6], q[7], q[8], q[11], q[2];
// UNMAPPED c5x [0, 1, 3, 4, 6, 2]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[3], q[4], q[6], q[2];
// UNMAPPED c9x [0, 1, 3, 4, 7, 8, 9, 10, 11, 2]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[3], q[4], q[7], q[8], q[9], q[10], q[11], q[2];
// UNMAPPED c8x [0, 1, 3, 4, 7, 8, 9, 10, 2]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[3], q[4], q[7], q[8], q[9], q[10], q[2];
// UNMAPPED c8x [0, 1, 3, 4, 7, 8, 9, 11, 2]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[3], q[4], q[7], q[8], q[9], q[11], q[2];
// UNMAPPED c7x [0, 1, 3, 4, 7, 8, 9, 2]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[4], q[7], q[8], q[9], q[2];
// UNMAPPED c8x [0, 1, 3, 4, 7, 8, 10, 11, 2]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[3], q[4], q[7], q[8], q[10], q[11], q[2];
// UNMAPPED c7x [0, 1, 3, 4, 7, 8, 10, 2]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[4], q[7], q[8], q[10], q[2];
// UNMAPPED c7x [0, 1, 3, 4, 7, 8, 11, 2]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[3], q[4], q[7], q[8], q[11], q[2];
// UNMAPPED c10x [0, 1, 4, 5, 6, 7, 8, 9, 10, 11, 3]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[1], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[3];
// UNMAPPED c9x [0, 1, 4, 5, 6, 7, 8, 9, 10, 3]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[3];
// UNMAPPED c9x [0, 1, 4, 5, 6, 7, 8, 9, 11, 3]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[4], q[5], q[6], q[7], q[8], q[9], q[11], q[3];
// UNMAPPED c8x [0, 1, 4, 5, 6, 7, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[4], q[5], q[6], q[7], q[8], q[9], q[3];
// UNMAPPED c9x [0, 1, 4, 5, 6, 7, 8, 10, 11, 3]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[4], q[5], q[6], q[7], q[8], q[10], q[11], q[3];
// UNMAPPED c8x [0, 1, 4, 5, 6, 7, 8, 10, 3]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[4], q[5], q[6], q[7], q[8], q[10], q[3];
// UNMAPPED c8x [0, 1, 4, 5, 6, 7, 8, 11, 3]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[4], q[5], q[6], q[7], q[8], q[11], q[3];
// UNMAPPED c5x [0, 1, 4, 5, 6, 3]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[4], q[5], q[6], q[3];
// UNMAPPED c9x [0, 1, 4, 5, 7, 8, 9, 10, 11, 3]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[4], q[5], q[7], q[8], q[9], q[10], q[11], q[3];
// UNMAPPED c8x [0, 1, 4, 5, 7, 8, 9, 10, 3]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[4], q[5], q[7], q[8], q[9], q[10], q[3];
// UNMAPPED c8x [0, 1, 4, 5, 7, 8, 9, 11, 3]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[4], q[5], q[7], q[8], q[9], q[11], q[3];
// UNMAPPED c7x [0, 1, 4, 5, 7, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[4], q[5], q[7], q[8], q[9], q[3];
// UNMAPPED c8x [0, 1, 4, 5, 7, 8, 10, 11, 3]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[4], q[5], q[7], q[8], q[10], q[11], q[3];
// UNMAPPED c7x [0, 1, 4, 5, 7, 8, 10, 3]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[4], q[5], q[7], q[8], q[10], q[3];
// UNMAPPED c7x [0, 1, 4, 5, 7, 8, 11, 3]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[4], q[5], q[7], q[8], q[11], q[3];
// UNMAPPED c4x [0, 1, 4, 5, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[4], q[5], q[3];
// UNMAPPED c9x [0, 1, 4, 6, 7, 8, 9, 10, 11, 3]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[4], q[6], q[7], q[8], q[9], q[10], q[11], q[3];
// UNMAPPED c8x [0, 1, 4, 6, 7, 8, 9, 10, 3]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[4], q[6], q[7], q[8], q[9], q[10], q[3];
// UNMAPPED c8x [0, 1, 4, 6, 7, 8, 9, 11, 3]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[4], q[6], q[7], q[8], q[9], q[11], q[3];
// UNMAPPED c7x [0, 1, 4, 6, 7, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[4], q[6], q[7], q[8], q[9], q[3];
// UNMAPPED c8x [0, 1, 4, 6, 7, 8, 10, 11, 3]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[4], q[6], q[7], q[8], q[10], q[11], q[3];
// UNMAPPED c7x [0, 1, 4, 6, 7, 8, 10, 3]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[4], q[6], q[7], q[8], q[10], q[3];
// UNMAPPED c7x [0, 1, 4, 6, 7, 8, 11, 3]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[4], q[6], q[7], q[8], q[11], q[3];
// UNMAPPED c4x [0, 1, 4, 6, 3]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[4], q[6], q[3];
// UNMAPPED c8x [0, 1, 4, 7, 8, 9, 10, 11, 3]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[4], q[7], q[8], q[9], q[10], q[11], q[3];
// UNMAPPED c7x [0, 1, 4, 7, 8, 9, 10, 3]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[4], q[7], q[8], q[9], q[10], q[3];
// UNMAPPED c7x [0, 1, 4, 7, 8, 9, 11, 3]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[4], q[7], q[8], q[9], q[11], q[3];
// UNMAPPED c6x [0, 1, 4, 7, 8, 9, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[4], q[7], q[8], q[9], q[3];
// UNMAPPED c7x [0, 1, 4, 7, 8, 10, 11, 3]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[4], q[7], q[8], q[10], q[11], q[3];
// UNMAPPED c6x [0, 1, 4, 7, 8, 10, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[4], q[7], q[8], q[10], q[3];
// UNMAPPED c6x [0, 1, 4, 7, 8, 11, 3]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[4], q[7], q[8], q[11], q[3];
// UNMAPPED c9x [0, 1, 5, 6, 7, 8, 9, 10, 11, 4]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[1], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[4];
// UNMAPPED c8x [0, 1, 5, 6, 7, 8, 9, 10, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[5], q[6], q[7], q[8], q[9], q[10], q[4];
// UNMAPPED c8x [0, 1, 5, 6, 7, 8, 9, 11, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[5], q[6], q[7], q[8], q[9], q[11], q[4];
// UNMAPPED c7x [0, 1, 5, 6, 7, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[5], q[6], q[7], q[8], q[9], q[4];
// UNMAPPED c8x [0, 1, 5, 6, 7, 8, 10, 11, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[5], q[6], q[7], q[8], q[10], q[11], q[4];
// UNMAPPED c7x [0, 1, 5, 6, 7, 8, 10, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[5], q[6], q[7], q[8], q[10], q[4];
// UNMAPPED c7x [0, 1, 5, 6, 7, 8, 11, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[5], q[6], q[7], q[8], q[11], q[4];
// UNMAPPED c4x [0, 1, 5, 6, 4]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[5], q[6], q[4];
// UNMAPPED c8x [0, 1, 5, 7, 8, 9, 10, 11, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[5], q[7], q[8], q[9], q[10], q[11], q[4];
// UNMAPPED c7x [0, 1, 5, 7, 8, 9, 10, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[5], q[7], q[8], q[9], q[10], q[4];
// UNMAPPED c7x [0, 1, 5, 7, 8, 9, 11, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[5], q[7], q[8], q[9], q[11], q[4];
// UNMAPPED c6x [0, 1, 5, 7, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[5], q[7], q[8], q[9], q[4];
// UNMAPPED c7x [0, 1, 5, 7, 8, 10, 11, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[5], q[7], q[8], q[10], q[11], q[4];
// UNMAPPED c6x [0, 1, 5, 7, 8, 10, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[5], q[7], q[8], q[10], q[4];
// UNMAPPED c6x [0, 1, 5, 7, 8, 11, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[5], q[7], q[8], q[11], q[4];
// UNMAPPED c3x [0, 1, 5, 4]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[5], q[4];
// UNMAPPED c8x [0, 1, 6, 7, 8, 9, 10, 11, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[6], q[7], q[8], q[9], q[10], q[11], q[5];
// UNMAPPED c8x [0, 1, 6, 7, 8, 9, 10, 11, 4]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[6], q[7], q[8], q[9], q[10], q[11], q[4];
// UNMAPPED c7x [0, 1, 6, 7, 8, 9, 10, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[6], q[7], q[8], q[9], q[10], q[5];
// UNMAPPED c7x [0, 1, 6, 7, 8, 9, 10, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[6], q[7], q[8], q[9], q[10], q[4];
// UNMAPPED c7x [0, 1, 6, 7, 8, 9, 11, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[6], q[7], q[8], q[9], q[11], q[5];
// UNMAPPED c7x [0, 1, 6, 7, 8, 9, 11, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[6], q[7], q[8], q[9], q[11], q[4];
// UNMAPPED c6x [0, 1, 6, 7, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[6], q[7], q[8], q[9], q[5];
// UNMAPPED c6x [0, 1, 6, 7, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[6], q[7], q[8], q[9], q[4];
// UNMAPPED c7x [0, 1, 6, 7, 8, 10, 11, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[6], q[7], q[8], q[10], q[11], q[5];
// UNMAPPED c7x [0, 1, 6, 7, 8, 10, 11, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[6], q[7], q[8], q[10], q[11], q[4];
// UNMAPPED c6x [0, 1, 6, 7, 8, 10, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[6], q[7], q[8], q[10], q[5];
// UNMAPPED c6x [0, 1, 6, 7, 8, 10, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[6], q[7], q[8], q[10], q[4];
// UNMAPPED c6x [0, 1, 6, 7, 8, 11, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[6], q[7], q[8], q[11], q[5];
// UNMAPPED c6x [0, 1, 6, 7, 8, 11, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[6], q[7], q[8], q[11], q[4];
// UNMAPPED c3x [0, 1, 6, 5]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[6], q[5];
// UNMAPPED c3x [0, 1, 6, 4]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[6], q[4];
// UNMAPPED c7x [0, 1, 7, 8, 9, 10, 11, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[7], q[8], q[9], q[10], q[11], q[6];
// UNMAPPED c7x [0, 1, 7, 8, 9, 10, 11, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[7], q[8], q[9], q[10], q[11], q[5];
// UNMAPPED c7x [0, 1, 7, 8, 9, 10, 11, 4]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[7], q[8], q[9], q[10], q[11], q[4];
// UNMAPPED c6x [0, 1, 7, 8, 9, 10, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[7], q[8], q[9], q[10], q[6];
// UNMAPPED c6x [0, 1, 7, 8, 9, 10, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[7], q[8], q[9], q[10], q[5];
// UNMAPPED c6x [0, 1, 7, 8, 9, 10, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[7], q[8], q[9], q[10], q[4];
// UNMAPPED c6x [0, 1, 7, 8, 9, 11, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[7], q[8], q[9], q[11], q[6];
// UNMAPPED c6x [0, 1, 7, 8, 9, 11, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[7], q[8], q[9], q[11], q[5];
// UNMAPPED c6x [0, 1, 7, 8, 9, 11, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[7], q[8], q[9], q[11], q[4];
// UNMAPPED c5x [0, 1, 7, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[7], q[8], q[9], q[6];
// UNMAPPED c5x [0, 1, 7, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[7], q[8], q[9], q[5];
// UNMAPPED c5x [0, 1, 7, 8, 9, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[7], q[8], q[9], q[4];
// UNMAPPED c6x [0, 1, 7, 8, 10, 11, 6]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[7], q[8], q[10], q[11], q[6];
// UNMAPPED c6x [0, 1, 7, 8, 10, 11, 5]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[7], q[8], q[10], q[11], q[5];
// UNMAPPED c6x [0, 1, 7, 8, 10, 11, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[7], q[8], q[10], q[11], q[4];
// UNMAPPED c5x [0, 1, 7, 8, 10, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[7], q[8], q[10], q[6];
// UNMAPPED c5x [0, 1, 7, 8, 10, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[7], q[8], q[10], q[5];
// UNMAPPED c5x [0, 1, 7, 8, 10, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[7], q[8], q[10], q[4];
// UNMAPPED c5x [0, 1, 7, 8, 11, 6]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[7], q[8], q[11], q[6];
// UNMAPPED c5x [0, 1, 7, 8, 11, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[7], q[8], q[11], q[5];
// UNMAPPED c5x [0, 1, 7, 8, 11, 4]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[7], q[8], q[11], q[4];
// UNMAPPED c6x [0, 1, 8, 9, 10, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[8], q[9], q[10], q[11], q[7];
// UNMAPPED c5x [0, 1, 8, 9, 10, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[8], q[9], q[10], q[7];
// UNMAPPED c5x [0, 1, 8, 9, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[8], q[9], q[11], q[7];
// UNMAPPED c4x [0, 1, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[8], q[9], q[7];
// UNMAPPED c5x [0, 1, 8, 10, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[8], q[10], q[11], q[7];
// UNMAPPED c4x [0, 1, 8, 10, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[8], q[10], q[7];
// UNMAPPED c4x [0, 1, 8, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[8], q[11], q[7];
// UNMAPPED c5x [0, 1, 9, 10, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[9], q[10], q[11], q[8];
// UNMAPPED c4x [0, 1, 9, 10, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[9], q[10], q[8];
// UNMAPPED c4x [0, 1, 9, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[9], q[11], q[8];
// UNMAPPED c3x [0, 1, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[9], q[8];
// UNMAPPED c4x [0, 1, 10, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[10], q[11], q[9];
// UNMAPPED c4x [0, 1, 10, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[10], q[11], q[8];
// UNMAPPED c3x [0, 1, 10, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[10], q[9];
// UNMAPPED c3x [0, 1, 10, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[10], q[8];
// UNMAPPED c3x [0, 1, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[11], q[10];
// UNMAPPED c3x [0, 1, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[11], q[9];
// UNMAPPED c3x [0, 1, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[11], q[8];
ccx q[0], q[1], q[12];
ccx q[0], q[1], q[8];
ccx q[0], q[1], q[7];
ccx q[0], q[1], q[4];
ccx q[0], q[1], q[3];
ccx q[0], q[1], q[2];
// UNMAPPED c11x [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12];
// UNMAPPED c11x [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 1]  (QASM3 비표준 — opaque)
qpgf_c11x q[0], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[1];
// UNMAPPED c10x [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[12];
// UNMAPPED c10x [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[1];
// UNMAPPED c10x [0, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[11], q[12];
// UNMAPPED c10x [0, 2, 3, 4, 5, 6, 7, 8, 9, 11, 1]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[11], q[1];
// UNMAPPED c9x [0, 2, 3, 4, 5, 6, 7, 8, 9, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[12];
// UNMAPPED c9x [0, 2, 3, 4, 5, 6, 7, 8, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[1];
// UNMAPPED c10x [0, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[10], q[11], q[12];
// UNMAPPED c10x [0, 2, 3, 4, 5, 6, 7, 8, 10, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[10], q[11], q[9];
// UNMAPPED c10x [0, 2, 3, 4, 5, 6, 7, 8, 10, 11, 1]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[10], q[11], q[1];
// UNMAPPED c9x [0, 2, 3, 4, 5, 6, 7, 8, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[10], q[12];
// UNMAPPED c9x [0, 2, 3, 4, 5, 6, 7, 8, 10, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[10], q[9];
// UNMAPPED c9x [0, 2, 3, 4, 5, 6, 7, 8, 10, 1]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[10], q[1];
// UNMAPPED c9x [0, 2, 3, 4, 5, 6, 7, 8, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[11], q[12];
// UNMAPPED c9x [0, 2, 3, 4, 5, 6, 7, 8, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[11], q[10];
// UNMAPPED c9x [0, 2, 3, 4, 5, 6, 7, 8, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[11], q[9];
// UNMAPPED c9x [0, 2, 3, 4, 5, 6, 7, 8, 11, 1]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[11], q[1];
// UNMAPPED c10x [0, 2, 3, 4, 5, 6, 8, 9, 10, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[10], q[11], q[7];
// UNMAPPED c9x [0, 2, 3, 4, 5, 6, 8, 9, 10, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[10], q[7];
// UNMAPPED c9x [0, 2, 3, 4, 5, 6, 8, 9, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[11], q[7];
// UNMAPPED c8x [0, 2, 3, 4, 5, 6, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[5], q[6], q[8], q[9], q[7];
// UNMAPPED c9x [0, 2, 3, 4, 5, 6, 8, 10, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[2], q[3], q[4], q[5], q[6], q[8], q[10], q[11], q[7];
// UNMAPPED c8x [0, 2, 3, 4, 5, 6, 8, 10, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[5], q[6], q[8], q[10], q[7];
// UNMAPPED c8x [0, 2, 3, 4, 5, 6, 8, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[5], q[6], q[8], q[11], q[7];
// UNMAPPED c9x [0, 2, 3, 4, 5, 6, 9, 10, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[2], q[3], q[4], q[5], q[6], q[9], q[10], q[11], q[8];
// UNMAPPED c8x [0, 2, 3, 4, 5, 6, 9, 10, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[5], q[6], q[9], q[10], q[8];
// UNMAPPED c8x [0, 2, 3, 4, 5, 6, 9, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[5], q[6], q[9], q[11], q[8];
// UNMAPPED c7x [0, 2, 3, 4, 5, 6, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[5], q[6], q[9], q[8];
// UNMAPPED c8x [0, 2, 3, 4, 5, 6, 10, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[5], q[6], q[10], q[11], q[9];
// UNMAPPED c8x [0, 2, 3, 4, 5, 6, 10, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[5], q[6], q[10], q[11], q[8];
// UNMAPPED c7x [0, 2, 3, 4, 5, 6, 10, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[5], q[6], q[10], q[9];
// UNMAPPED c7x [0, 2, 3, 4, 5, 6, 10, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[5], q[6], q[10], q[8];
// UNMAPPED c7x [0, 2, 3, 4, 5, 6, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[5], q[6], q[11], q[10];
// UNMAPPED c7x [0, 2, 3, 4, 5, 6, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[5], q[6], q[11], q[9];
// UNMAPPED c7x [0, 2, 3, 4, 5, 6, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[5], q[6], q[11], q[8];
// UNMAPPED c6x [0, 2, 3, 4, 5, 6, 12]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[5], q[6], q[12];
// UNMAPPED c6x [0, 2, 3, 4, 5, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[5], q[6], q[8];
// UNMAPPED c6x [0, 2, 3, 4, 5, 6, 7]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[5], q[6], q[7];
// UNMAPPED c6x [0, 2, 3, 4, 5, 6, 1]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[5], q[6], q[1];
// UNMAPPED c10x [0, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[10], q[11], q[12];
// UNMAPPED c10x [0, 2, 3, 4, 5, 7, 8, 9, 10, 11, 1]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[10], q[11], q[1];
// UNMAPPED c9x [0, 2, 3, 4, 5, 7, 8, 9, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[10], q[12];
// UNMAPPED c9x [0, 2, 3, 4, 5, 7, 8, 9, 10, 1]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[10], q[1];
// UNMAPPED c9x [0, 2, 3, 4, 5, 7, 8, 9, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[11], q[12];
// UNMAPPED c9x [0, 2, 3, 4, 5, 7, 8, 9, 11, 1]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[11], q[1];
// UNMAPPED c8x [0, 2, 3, 4, 5, 7, 8, 9, 12]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[12];
// UNMAPPED c8x [0, 2, 3, 4, 5, 7, 8, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[5], q[7], q[8], q[9], q[1];
// UNMAPPED c9x [0, 2, 3, 4, 5, 7, 8, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[2], q[3], q[4], q[5], q[7], q[8], q[10], q[11], q[12];
// UNMAPPED c9x [0, 2, 3, 4, 5, 7, 8, 10, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[2], q[3], q[4], q[5], q[7], q[8], q[10], q[11], q[9];
// UNMAPPED c9x [0, 2, 3, 4, 5, 7, 8, 10, 11, 1]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[2], q[3], q[4], q[5], q[7], q[8], q[10], q[11], q[1];
// UNMAPPED c8x [0, 2, 3, 4, 5, 7, 8, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[5], q[7], q[8], q[10], q[12];
// UNMAPPED c8x [0, 2, 3, 4, 5, 7, 8, 10, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[5], q[7], q[8], q[10], q[9];
// UNMAPPED c8x [0, 2, 3, 4, 5, 7, 8, 10, 1]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[5], q[7], q[8], q[10], q[1];
// UNMAPPED c8x [0, 2, 3, 4, 5, 7, 8, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[5], q[7], q[8], q[11], q[12];
// UNMAPPED c8x [0, 2, 3, 4, 5, 7, 8, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[5], q[7], q[8], q[11], q[10];
// UNMAPPED c8x [0, 2, 3, 4, 5, 7, 8, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[5], q[7], q[8], q[11], q[9];
// UNMAPPED c8x [0, 2, 3, 4, 5, 7, 8, 11, 1]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[5], q[7], q[8], q[11], q[1];
// UNMAPPED c9x [0, 2, 3, 4, 5, 8, 9, 10, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[2], q[3], q[4], q[5], q[8], q[9], q[10], q[11], q[7];
// UNMAPPED c8x [0, 2, 3, 4, 5, 8, 9, 10, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[5], q[8], q[9], q[10], q[7];
// UNMAPPED c8x [0, 2, 3, 4, 5, 8, 9, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[5], q[8], q[9], q[11], q[7];
// UNMAPPED c7x [0, 2, 3, 4, 5, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[5], q[8], q[9], q[7];
// UNMAPPED c8x [0, 2, 3, 4, 5, 8, 10, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[5], q[8], q[10], q[11], q[7];
// UNMAPPED c7x [0, 2, 3, 4, 5, 8, 10, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[5], q[8], q[10], q[7];
// UNMAPPED c7x [0, 2, 3, 4, 5, 8, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[5], q[8], q[11], q[7];
// UNMAPPED c8x [0, 2, 3, 4, 5, 9, 10, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[5], q[9], q[10], q[11], q[8];
// UNMAPPED c7x [0, 2, 3, 4, 5, 9, 10, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[5], q[9], q[10], q[8];
// UNMAPPED c7x [0, 2, 3, 4, 5, 9, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[5], q[9], q[11], q[8];
// UNMAPPED c6x [0, 2, 3, 4, 5, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[5], q[9], q[8];
// UNMAPPED c7x [0, 2, 3, 4, 5, 10, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[5], q[10], q[11], q[9];
// UNMAPPED c7x [0, 2, 3, 4, 5, 10, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[5], q[10], q[11], q[8];
// UNMAPPED c6x [0, 2, 3, 4, 5, 10, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[5], q[10], q[9];
// UNMAPPED c6x [0, 2, 3, 4, 5, 10, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[5], q[10], q[8];
// UNMAPPED c6x [0, 2, 3, 4, 5, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[5], q[11], q[10];
// UNMAPPED c6x [0, 2, 3, 4, 5, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[5], q[11], q[9];
// UNMAPPED c6x [0, 2, 3, 4, 5, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[5], q[11], q[8];
// UNMAPPED c5x [0, 2, 3, 4, 5, 12]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[4], q[5], q[12];
// UNMAPPED c5x [0, 2, 3, 4, 5, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[4], q[5], q[8];
// UNMAPPED c5x [0, 2, 3, 4, 5, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[4], q[5], q[7];
// UNMAPPED c5x [0, 2, 3, 4, 5, 1]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[4], q[5], q[1];
// UNMAPPED c10x [0, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[10], q[11], q[12];
// UNMAPPED c10x [0, 2, 3, 4, 6, 7, 8, 9, 10, 11, 5]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[10], q[11], q[5];
// UNMAPPED c10x [0, 2, 3, 4, 6, 7, 8, 9, 10, 11, 1]  (QASM3 비표준 — opaque)
qpgf_c10x q[0], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[10], q[11], q[1];
// UNMAPPED c9x [0, 2, 3, 4, 6, 7, 8, 9, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[10], q[12];
// UNMAPPED c9x [0, 2, 3, 4, 6, 7, 8, 9, 10, 5]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[10], q[5];
// UNMAPPED c9x [0, 2, 3, 4, 6, 7, 8, 9, 10, 1]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[10], q[1];
// UNMAPPED c9x [0, 2, 3, 4, 6, 7, 8, 9, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[11], q[12];
// UNMAPPED c9x [0, 2, 3, 4, 6, 7, 8, 9, 11, 5]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[11], q[5];
// UNMAPPED c9x [0, 2, 3, 4, 6, 7, 8, 9, 11, 1]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[11], q[1];
// UNMAPPED c8x [0, 2, 3, 4, 6, 7, 8, 9, 12]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[12];
// UNMAPPED c8x [0, 2, 3, 4, 6, 7, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[5];
// UNMAPPED c8x [0, 2, 3, 4, 6, 7, 8, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[6], q[7], q[8], q[9], q[1];
// UNMAPPED c9x [0, 2, 3, 4, 6, 7, 8, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[2], q[3], q[4], q[6], q[7], q[8], q[10], q[11], q[12];
// UNMAPPED c9x [0, 2, 3, 4, 6, 7, 8, 10, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[2], q[3], q[4], q[6], q[7], q[8], q[10], q[11], q[9];
// UNMAPPED c9x [0, 2, 3, 4, 6, 7, 8, 10, 11, 5]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[2], q[3], q[4], q[6], q[7], q[8], q[10], q[11], q[5];
// UNMAPPED c9x [0, 2, 3, 4, 6, 7, 8, 10, 11, 1]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[2], q[3], q[4], q[6], q[7], q[8], q[10], q[11], q[1];
// UNMAPPED c8x [0, 2, 3, 4, 6, 7, 8, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[6], q[7], q[8], q[10], q[12];
// UNMAPPED c8x [0, 2, 3, 4, 6, 7, 8, 10, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[6], q[7], q[8], q[10], q[9];
// UNMAPPED c8x [0, 2, 3, 4, 6, 7, 8, 10, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[6], q[7], q[8], q[10], q[5];
// UNMAPPED c8x [0, 2, 3, 4, 6, 7, 8, 10, 1]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[6], q[7], q[8], q[10], q[1];
// UNMAPPED c8x [0, 2, 3, 4, 6, 7, 8, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[6], q[7], q[8], q[11], q[12];
// UNMAPPED c8x [0, 2, 3, 4, 6, 7, 8, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[6], q[7], q[8], q[11], q[10];
// UNMAPPED c8x [0, 2, 3, 4, 6, 7, 8, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[6], q[7], q[8], q[11], q[9];
// UNMAPPED c8x [0, 2, 3, 4, 6, 7, 8, 11, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[6], q[7], q[8], q[11], q[5];
// UNMAPPED c8x [0, 2, 3, 4, 6, 7, 8, 11, 1]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[6], q[7], q[8], q[11], q[1];
// UNMAPPED c9x [0, 2, 3, 4, 6, 8, 9, 10, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[2], q[3], q[4], q[6], q[8], q[9], q[10], q[11], q[7];
// UNMAPPED c8x [0, 2, 3, 4, 6, 8, 9, 10, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[6], q[8], q[9], q[10], q[7];
// UNMAPPED c8x [0, 2, 3, 4, 6, 8, 9, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[6], q[8], q[9], q[11], q[7];
// UNMAPPED c7x [0, 2, 3, 4, 6, 8, 9, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[6], q[8], q[9], q[7];
// UNMAPPED c8x [0, 2, 3, 4, 6, 8, 10, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[6], q[8], q[10], q[11], q[7];
// UNMAPPED c7x [0, 2, 3, 4, 6, 8, 10, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[6], q[8], q[10], q[7];
// UNMAPPED c7x [0, 2, 3, 4, 6, 8, 11, 7]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[6], q[8], q[11], q[7];
// UNMAPPED c8x [0, 2, 3, 4, 6, 9, 10, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[6], q[9], q[10], q[11], q[8];
// UNMAPPED c7x [0, 2, 3, 4, 6, 9, 10, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[6], q[9], q[10], q[8];
// UNMAPPED c7x [0, 2, 3, 4, 6, 9, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[6], q[9], q[11], q[8];
// UNMAPPED c6x [0, 2, 3, 4, 6, 9, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[6], q[9], q[8];
// UNMAPPED c7x [0, 2, 3, 4, 6, 10, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[6], q[10], q[11], q[9];
// UNMAPPED c7x [0, 2, 3, 4, 6, 10, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[6], q[10], q[11], q[8];
// UNMAPPED c6x [0, 2, 3, 4, 6, 10, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[6], q[10], q[9];
// UNMAPPED c6x [0, 2, 3, 4, 6, 10, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[6], q[10], q[8];
// UNMAPPED c6x [0, 2, 3, 4, 6, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[6], q[11], q[10];
// UNMAPPED c6x [0, 2, 3, 4, 6, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[6], q[11], q[9];
// UNMAPPED c6x [0, 2, 3, 4, 6, 11, 8]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[2], q[3], q[4], q[6], q[11], q[8];
// UNMAPPED c5x [0, 2, 3, 4, 6, 12]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[4], q[6], q[12];
// UNMAPPED c5x [0, 2, 3, 4, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[4], q[6], q[8];
// UNMAPPED c5x [0, 2, 3, 4, 6, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[4], q[6], q[7];
// UNMAPPED c5x [0, 2, 3, 4, 6, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[4], q[6], q[5];
// UNMAPPED c5x [0, 2, 3, 4, 6, 1]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[2], q[3], q[4], q[6], q[1];
// UNMAPPED c9x [0, 2, 3, 4, 7, 8, 9, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[2], q[3], q[4], q[7], q[8], q[9], q[10], q[11], q[12];
// UNMAPPED c9x [0, 2, 3, 4, 7, 8, 9, 10, 11, 6]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[2], q[3], q[4], q[7], q[8], q[9], q[10], q[11], q[6];
// UNMAPPED c9x [0, 2, 3, 4, 7, 8, 9, 10, 11, 5]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[2], q[3], q[4], q[7], q[8], q[9], q[10], q[11], q[5];
// UNMAPPED c9x [0, 2, 3, 4, 7, 8, 9, 10, 11, 1]  (QASM3 비표준 — opaque)
qpgf_c9x q[0], q[2], q[3], q[4], q[7], q[8], q[9], q[10], q[11], q[1];
// UNMAPPED c8x [0, 2, 3, 4, 7, 8, 9, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[7], q[8], q[9], q[10], q[12];
// UNMAPPED c8x [0, 2, 3, 4, 7, 8, 9, 10, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[7], q[8], q[9], q[10], q[6];
// UNMAPPED c8x [0, 2, 3, 4, 7, 8, 9, 10, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[7], q[8], q[9], q[10], q[5];
// UNMAPPED c8x [0, 2, 3, 4, 7, 8, 9, 10, 1]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[7], q[8], q[9], q[10], q[1];
// UNMAPPED c8x [0, 2, 3, 4, 7, 8, 9, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[7], q[8], q[9], q[11], q[12];
// UNMAPPED c8x [0, 2, 3, 4, 7, 8, 9, 11, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[7], q[8], q[9], q[11], q[6];
// UNMAPPED c8x [0, 2, 3, 4, 7, 8, 9, 11, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[7], q[8], q[9], q[11], q[5];
// UNMAPPED c8x [0, 2, 3, 4, 7, 8, 9, 11, 1]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[7], q[8], q[9], q[11], q[1];
// UNMAPPED c7x [0, 2, 3, 4, 7, 8, 9, 12]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[7], q[8], q[9], q[12];
// UNMAPPED c7x [0, 2, 3, 4, 7, 8, 9, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[7], q[8], q[9], q[6];
// UNMAPPED c7x [0, 2, 3, 4, 7, 8, 9, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[7], q[8], q[9], q[5];
// UNMAPPED c7x [0, 2, 3, 4, 7, 8, 9, 1]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[7], q[8], q[9], q[1];
// UNMAPPED c8x [0, 2, 3, 4, 7, 8, 10, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[7], q[8], q[10], q[11], q[12];
// UNMAPPED c8x [0, 2, 3, 4, 7, 8, 10, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[7], q[8], q[10], q[11], q[9];
// UNMAPPED c8x [0, 2, 3, 4, 7, 8, 10, 11, 6]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[7], q[8], q[10], q[11], q[6];
// UNMAPPED c8x [0, 2, 3, 4, 7, 8, 10, 11, 5]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[7], q[8], q[10], q[11], q[5];
// UNMAPPED c8x [0, 2, 3, 4, 7, 8, 10, 11, 1]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[7], q[8], q[10], q[11], q[1];
// UNMAPPED c7x [0, 2, 3, 4, 7, 8, 10, 12]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[7], q[8], q[10], q[12];
// UNMAPPED c7x [0, 2, 3, 4, 7, 8, 10, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[7], q[8], q[10], q[9];
// UNMAPPED c7x [0, 2, 3, 4, 7, 8, 10, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[7], q[8], q[10], q[6];
// UNMAPPED c7x [0, 2, 3, 4, 7, 8, 10, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[7], q[8], q[10], q[5];
// UNMAPPED c7x [0, 2, 3, 4, 7, 8, 10, 1]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[7], q[8], q[10], q[1];
// UNMAPPED c7x [0, 2, 3, 4, 7, 8, 11, 12]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[7], q[8], q[11], q[12];
// UNMAPPED c7x [0, 2, 3, 4, 7, 8, 11, 10]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[7], q[8], q[11], q[10];
// UNMAPPED c7x [0, 2, 3, 4, 7, 8, 11, 9]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[7], q[8], q[11], q[9];
// UNMAPPED c7x [0, 2, 3, 4, 7, 8, 11, 6]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[7], q[8], q[11], q[6];
// UNMAPPED c7x [0, 2, 3, 4, 7, 8, 11, 5]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[7], q[8], q[11], q[5];
// UNMAPPED c7x [0, 2, 3, 4, 7, 8, 11, 1]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[2], q[3], q[4], q[7], q[8], q[11], q[1];
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
ccx q[0], q[7], q[6];
ccx q[0], q[6], q[7];
ccx q[0], q[8], q[7];
ccx q[0], q[7], q[8];
ccx q[0], q[9], q[8];
ccx q[0], q[8], q[9];
ccx q[0], q[10], q[9];
ccx q[0], q[9], q[10];
ccx q[0], q[11], q[10];
ccx q[0], q[10], q[11];
ccx q[0], q[12], q[11];
ccx q[0], q[11], q[12];
