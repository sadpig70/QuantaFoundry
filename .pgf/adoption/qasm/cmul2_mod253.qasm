OPENQASM 3.0;
include "stdgates.inc";
qubit[9] q;

gate qpgf_c3x q0, q1, q2, q3 { }  // opaque: c3x (4q), golden in registry/modules/c3x.sealed.json
gate qpgf_c4x q0, q1, q2, q3, q4 { }  // opaque: c4x (5q), golden in registry/modules/c4x.sealed.json
gate qpgf_c5x q0, q1, q2, q3, q4, q5 { }  // opaque: c5x (6q), golden in registry/modules/c5x.sealed.json
gate qpgf_c6x q0, q1, q2, q3, q4, q5, q6 { }  // opaque: c6x (7q), golden in registry/modules/c6x.sealed.json
gate qpgf_c7x q0, q1, q2, q3, q4, q5, q6, q7 { }  // opaque: c7x (8q), golden in registry/modules/c7x.sealed.json
gate qpgf_c8x q0, q1, q2, q3, q4, q5, q6, q7, q8 { }  // opaque: c8x (9q), golden in registry/modules/c8x.sealed.json

// UNMAPPED c8x [0, 1, 2, 3, 4, 5, 6, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8];
// UNMAPPED c8x [0, 1, 3, 4, 5, 6, 7, 8, 2]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[1], q[3], q[4], q[5], q[6], q[7], q[8], q[2];
// UNMAPPED c7x [0, 1, 4, 5, 6, 7, 8, 3]  (QASM3 비표준 — opaque)
qpgf_c7x q[0], q[1], q[4], q[5], q[6], q[7], q[8], q[3];
// UNMAPPED c6x [0, 1, 5, 6, 7, 8, 4]  (QASM3 비표준 — opaque)
qpgf_c6x q[0], q[1], q[5], q[6], q[7], q[8], q[4];
// UNMAPPED c5x [0, 1, 6, 7, 8, 5]  (QASM3 비표준 — opaque)
qpgf_c5x q[0], q[1], q[6], q[7], q[8], q[5];
// UNMAPPED c4x [0, 1, 7, 8, 6]  (QASM3 비표준 — opaque)
qpgf_c4x q[0], q[1], q[7], q[8], q[6];
// UNMAPPED c3x [0, 1, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[8], q[7];
ccx q[0], q[1], q[7];
ccx q[0], q[1], q[6];
ccx q[0], q[1], q[5];
ccx q[0], q[1], q[4];
ccx q[0], q[1], q[3];
ccx q[0], q[1], q[2];
// UNMAPPED c8x [0, 2, 3, 4, 5, 6, 7, 8, 1]  (QASM3 비표준 — opaque)
qpgf_c8x q[0], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[1];
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
