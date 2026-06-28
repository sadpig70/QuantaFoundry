OPENQASM 3.0;
include "stdgates.inc";
qubit[12] q;

gate qpgf_c3x q0, q1, q2, q3 { }  // opaque: c3x (4q), golden in registry/modules/c3x.sealed.json
gate qpgf_c4x q0, q1, q2, q3, q4 { }  // opaque: c4x (5q), golden in registry/modules/c4x.sealed.json
gate qpgf_c5x q0, q1, q2, q3, q4, q5 { }  // opaque: c5x (6q), golden in registry/modules/c5x.sealed.json

h q[0];
h q[1];
h q[2];
h q[3];
h q[4];
h q[5];
h q[6];
ccx q[11], q[0], q[10];
ccx q[11], q[0], q[8];
ccx q[10], q[0], q[11];
ccx q[10], q[0], q[8];
// UNMAPPED c3x [9, 8, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[0], q[11];
// UNMAPPED c4x [11, 9, 8, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[8], q[0], q[10];
// UNMAPPED c3x [11, 10, 0, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[10], q[0], q[9];
// UNMAPPED c3x [11, 10, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[10], q[0], q[8];
ccx q[9], q[0], q[11];
ccx q[9], q[0], q[10];
// UNMAPPED c4x [10, 9, 8, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[0], q[11];
// UNMAPPED c3x [11, 9, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[9], q[0], q[10];
// UNMAPPED c3x [11, 9, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[9], q[0], q[8];
// UNMAPPED c3x [11, 8, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[0], q[10];
// UNMAPPED c4x [11, 10, 8, 0, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[0], q[9];
// UNMAPPED c3x [10, 9, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[9], q[0], q[11];
// UNMAPPED c3x [10, 9, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[9], q[0], q[8];
// UNMAPPED c3x [11, 8, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[0], q[10];
// UNMAPPED c4x [11, 10, 8, 0, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[0], q[9];
// UNMAPPED c4x [11, 10, 9, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[9], q[0], q[8];
ccx q[8], q[0], q[11];
// UNMAPPED c3x [9, 8, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[0], q[11];
// UNMAPPED c3x [11, 8, 0, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[0], q[9];
ccx q[7], q[0], q[11];
// UNMAPPED c3x [11, 7, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[0], q[10];
// UNMAPPED c4x [11, 10, 7, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[0], q[8];
// UNMAPPED c4x [11, 10, 8, 0, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[0], q[7];
// UNMAPPED c3x [9, 8, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[0], q[10];
// UNMAPPED c3x [11, 7, 0, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[0], q[9];
// UNMAPPED c4x [11, 9, 7, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[7], q[0], q[8];
// UNMAPPED c4x [11, 9, 8, 0, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[8], q[0], q[7];
// UNMAPPED c5x [11, 10, 9, 7, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[7], q[0], q[8];
// UNMAPPED c4x [10, 9, 8, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[0], q[11];
// UNMAPPED c4x [10, 9, 8, 0, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[0], q[7];
// UNMAPPED c5x [11, 9, 8, 7, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[0], q[10];
// UNMAPPED c5x [11, 10, 9, 8, 0, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[8], q[0], q[7];
ccx q[7], q[0], q[11];
ccx q[7], q[0], q[10];
ccx q[7], q[0], q[9];
// UNMAPPED c4x [10, 9, 7, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[0], q[11];
// UNMAPPED c3x [11, 7, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[0], q[10];
// UNMAPPED c3x [11, 7, 0, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[0], q[9];
// UNMAPPED c4x [11, 8, 7, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[0], q[10];
// UNMAPPED c3x [10, 7, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[7], q[0], q[11];
// UNMAPPED c3x [10, 7, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[7], q[0], q[8];
// UNMAPPED c5x [11, 9, 8, 7, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[0], q[10];
// UNMAPPED c4x [11, 10, 7, 0, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[0], q[9];
// UNMAPPED c4x [11, 10, 7, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[0], q[8];
// UNMAPPED c3x [9, 7, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[0], q[11];
// UNMAPPED c3x [9, 7, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[0], q[10];
// UNMAPPED c3x [9, 7, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[0], q[8];
// UNMAPPED c4x [9, 8, 7, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[0], q[11];
// UNMAPPED c4x [11, 9, 7, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[7], q[0], q[8];
// UNMAPPED c4x [10, 9, 7, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[0], q[11];
// UNMAPPED c4x [10, 9, 7, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[0], q[8];
// UNMAPPED c4x [11, 8, 7, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[0], q[10];
// UNMAPPED c5x [11, 10, 8, 7, 0, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[8], q[7], q[0], q[9];
// UNMAPPED c5x [11, 10, 9, 7, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[7], q[0], q[8];
// UNMAPPED c4x [9, 8, 7, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[0], q[11];
// UNMAPPED c4x [11, 8, 7, 0, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[0], q[9];
// UNMAPPED c4x [10, 8, 7, 0, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[8], q[7], q[0], q[9];
// UNMAPPED c4x [9, 8, 7, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[0], q[11];
// UNMAPPED c5x [11, 9, 8, 7, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[0], q[10];
// UNMAPPED c5x [11, 10, 8, 7, 0, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[8], q[7], q[0], q[9];
// UNMAPPED c4x [9, 8, 7, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[0], q[11];
// UNMAPPED c5x [11, 9, 8, 7, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[0], q[10];
ccx q[11], q[0], q[10];
ccx q[11], q[0], q[8];
ccx q[10], q[0], q[11];
ccx q[10], q[0], q[8];
// UNMAPPED c3x [9, 8, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[0], q[11];
// UNMAPPED c4x [11, 9, 8, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[8], q[0], q[10];
// UNMAPPED c3x [11, 10, 0, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[10], q[0], q[9];
// UNMAPPED c3x [11, 10, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[10], q[0], q[8];
ccx q[9], q[0], q[11];
ccx q[9], q[0], q[10];
// UNMAPPED c4x [10, 9, 8, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[0], q[11];
// UNMAPPED c3x [11, 9, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[9], q[0], q[10];
// UNMAPPED c3x [11, 9, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[9], q[0], q[8];
// UNMAPPED c3x [11, 8, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[0], q[10];
// UNMAPPED c4x [11, 10, 8, 0, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[0], q[9];
// UNMAPPED c3x [10, 9, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[9], q[0], q[11];
// UNMAPPED c3x [10, 9, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[9], q[0], q[8];
// UNMAPPED c3x [11, 8, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[0], q[10];
// UNMAPPED c4x [11, 10, 8, 0, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[0], q[9];
// UNMAPPED c4x [11, 10, 9, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[9], q[0], q[8];
ccx q[8], q[0], q[11];
// UNMAPPED c3x [9, 8, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[0], q[11];
// UNMAPPED c3x [11, 8, 0, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[0], q[9];
ccx q[7], q[0], q[11];
// UNMAPPED c3x [11, 7, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[0], q[10];
// UNMAPPED c4x [11, 10, 7, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[0], q[8];
// UNMAPPED c4x [11, 10, 8, 0, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[0], q[7];
// UNMAPPED c3x [9, 8, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[0], q[10];
// UNMAPPED c3x [11, 7, 0, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[0], q[9];
// UNMAPPED c4x [11, 9, 7, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[7], q[0], q[8];
// UNMAPPED c4x [11, 9, 8, 0, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[8], q[0], q[7];
// UNMAPPED c5x [11, 10, 9, 7, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[7], q[0], q[8];
// UNMAPPED c4x [10, 9, 8, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[0], q[11];
// UNMAPPED c4x [10, 9, 8, 0, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[0], q[7];
// UNMAPPED c5x [11, 9, 8, 7, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[0], q[10];
// UNMAPPED c5x [11, 10, 9, 8, 0, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[8], q[0], q[7];
ccx q[7], q[0], q[11];
ccx q[7], q[0], q[10];
ccx q[7], q[0], q[9];
// UNMAPPED c4x [10, 9, 7, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[0], q[11];
// UNMAPPED c3x [11, 7, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[0], q[10];
// UNMAPPED c3x [11, 7, 0, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[0], q[9];
// UNMAPPED c4x [11, 8, 7, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[0], q[10];
// UNMAPPED c3x [10, 7, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[7], q[0], q[11];
// UNMAPPED c3x [10, 7, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[7], q[0], q[8];
// UNMAPPED c5x [11, 9, 8, 7, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[0], q[10];
// UNMAPPED c4x [11, 10, 7, 0, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[0], q[9];
// UNMAPPED c4x [11, 10, 7, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[0], q[8];
// UNMAPPED c3x [9, 7, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[0], q[11];
// UNMAPPED c3x [9, 7, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[0], q[10];
// UNMAPPED c3x [9, 7, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[0], q[8];
// UNMAPPED c4x [9, 8, 7, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[0], q[11];
// UNMAPPED c4x [11, 9, 7, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[7], q[0], q[8];
// UNMAPPED c4x [10, 9, 7, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[0], q[11];
// UNMAPPED c4x [10, 9, 7, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[0], q[8];
// UNMAPPED c4x [11, 8, 7, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[0], q[10];
// UNMAPPED c5x [11, 10, 8, 7, 0, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[8], q[7], q[0], q[9];
// UNMAPPED c5x [11, 10, 9, 7, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[7], q[0], q[8];
// UNMAPPED c4x [9, 8, 7, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[0], q[11];
// UNMAPPED c4x [11, 8, 7, 0, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[0], q[9];
// UNMAPPED c4x [10, 8, 7, 0, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[8], q[7], q[0], q[9];
// UNMAPPED c4x [9, 8, 7, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[0], q[11];
// UNMAPPED c5x [11, 9, 8, 7, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[0], q[10];
// UNMAPPED c5x [11, 10, 8, 7, 0, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[8], q[7], q[0], q[9];
// UNMAPPED c4x [9, 8, 7, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[0], q[11];
// UNMAPPED c5x [11, 9, 8, 7, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[0], q[10];
ccx q[11], q[0], q[10];
ccx q[11], q[0], q[8];
ccx q[10], q[0], q[11];
ccx q[10], q[0], q[8];
// UNMAPPED c3x [9, 8, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[0], q[11];
// UNMAPPED c4x [11, 9, 8, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[8], q[0], q[10];
// UNMAPPED c3x [11, 10, 0, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[10], q[0], q[9];
// UNMAPPED c3x [11, 10, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[10], q[0], q[8];
ccx q[9], q[0], q[11];
ccx q[9], q[0], q[10];
// UNMAPPED c4x [10, 9, 8, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[0], q[11];
// UNMAPPED c3x [11, 9, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[9], q[0], q[10];
// UNMAPPED c3x [11, 9, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[9], q[0], q[8];
// UNMAPPED c3x [11, 8, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[0], q[10];
// UNMAPPED c4x [11, 10, 8, 0, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[0], q[9];
// UNMAPPED c3x [10, 9, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[9], q[0], q[11];
// UNMAPPED c3x [10, 9, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[9], q[0], q[8];
// UNMAPPED c3x [11, 8, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[0], q[10];
// UNMAPPED c4x [11, 10, 8, 0, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[0], q[9];
// UNMAPPED c4x [11, 10, 9, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[9], q[0], q[8];
ccx q[8], q[0], q[11];
// UNMAPPED c3x [9, 8, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[0], q[11];
// UNMAPPED c3x [11, 8, 0, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[0], q[9];
ccx q[7], q[0], q[11];
// UNMAPPED c3x [11, 7, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[0], q[10];
// UNMAPPED c4x [11, 10, 7, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[0], q[8];
// UNMAPPED c4x [11, 10, 8, 0, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[0], q[7];
// UNMAPPED c3x [9, 8, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[0], q[10];
// UNMAPPED c3x [11, 7, 0, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[0], q[9];
// UNMAPPED c4x [11, 9, 7, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[7], q[0], q[8];
// UNMAPPED c4x [11, 9, 8, 0, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[8], q[0], q[7];
// UNMAPPED c5x [11, 10, 9, 7, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[7], q[0], q[8];
// UNMAPPED c4x [10, 9, 8, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[0], q[11];
// UNMAPPED c4x [10, 9, 8, 0, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[0], q[7];
// UNMAPPED c5x [11, 9, 8, 7, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[0], q[10];
// UNMAPPED c5x [11, 10, 9, 8, 0, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[8], q[0], q[7];
ccx q[7], q[0], q[11];
ccx q[7], q[0], q[10];
ccx q[7], q[0], q[9];
// UNMAPPED c4x [10, 9, 7, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[0], q[11];
// UNMAPPED c3x [11, 7, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[0], q[10];
// UNMAPPED c3x [11, 7, 0, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[0], q[9];
// UNMAPPED c4x [11, 8, 7, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[0], q[10];
// UNMAPPED c3x [10, 7, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[7], q[0], q[11];
// UNMAPPED c3x [10, 7, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[7], q[0], q[8];
// UNMAPPED c5x [11, 9, 8, 7, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[0], q[10];
// UNMAPPED c4x [11, 10, 7, 0, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[0], q[9];
// UNMAPPED c4x [11, 10, 7, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[0], q[8];
// UNMAPPED c3x [9, 7, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[0], q[11];
// UNMAPPED c3x [9, 7, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[0], q[10];
// UNMAPPED c3x [9, 7, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[0], q[8];
// UNMAPPED c4x [9, 8, 7, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[0], q[11];
// UNMAPPED c4x [11, 9, 7, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[7], q[0], q[8];
// UNMAPPED c4x [10, 9, 7, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[0], q[11];
// UNMAPPED c4x [10, 9, 7, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[0], q[8];
// UNMAPPED c4x [11, 8, 7, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[0], q[10];
// UNMAPPED c5x [11, 10, 8, 7, 0, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[8], q[7], q[0], q[9];
// UNMAPPED c5x [11, 10, 9, 7, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[7], q[0], q[8];
// UNMAPPED c4x [9, 8, 7, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[0], q[11];
// UNMAPPED c4x [11, 8, 7, 0, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[0], q[9];
// UNMAPPED c4x [10, 8, 7, 0, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[8], q[7], q[0], q[9];
// UNMAPPED c4x [9, 8, 7, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[0], q[11];
// UNMAPPED c5x [11, 9, 8, 7, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[0], q[10];
// UNMAPPED c5x [11, 10, 8, 7, 0, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[8], q[7], q[0], q[9];
// UNMAPPED c4x [9, 8, 7, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[0], q[11];
// UNMAPPED c5x [11, 9, 8, 7, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[0], q[10];
ccx q[11], q[0], q[10];
ccx q[11], q[0], q[8];
ccx q[10], q[0], q[11];
ccx q[10], q[0], q[8];
// UNMAPPED c3x [9, 8, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[0], q[11];
// UNMAPPED c4x [11, 9, 8, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[8], q[0], q[10];
// UNMAPPED c3x [11, 10, 0, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[10], q[0], q[9];
// UNMAPPED c3x [11, 10, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[10], q[0], q[8];
ccx q[9], q[0], q[11];
ccx q[9], q[0], q[10];
// UNMAPPED c4x [10, 9, 8, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[0], q[11];
// UNMAPPED c3x [11, 9, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[9], q[0], q[10];
// UNMAPPED c3x [11, 9, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[9], q[0], q[8];
// UNMAPPED c3x [11, 8, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[0], q[10];
// UNMAPPED c4x [11, 10, 8, 0, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[0], q[9];
// UNMAPPED c3x [10, 9, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[9], q[0], q[11];
// UNMAPPED c3x [10, 9, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[9], q[0], q[8];
// UNMAPPED c3x [11, 8, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[0], q[10];
// UNMAPPED c4x [11, 10, 8, 0, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[0], q[9];
// UNMAPPED c4x [11, 10, 9, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[9], q[0], q[8];
ccx q[8], q[0], q[11];
// UNMAPPED c3x [9, 8, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[0], q[11];
// UNMAPPED c3x [11, 8, 0, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[0], q[9];
ccx q[7], q[0], q[11];
// UNMAPPED c3x [11, 7, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[0], q[10];
// UNMAPPED c4x [11, 10, 7, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[0], q[8];
// UNMAPPED c4x [11, 10, 8, 0, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[0], q[7];
// UNMAPPED c3x [9, 8, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[0], q[10];
// UNMAPPED c3x [11, 7, 0, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[0], q[9];
// UNMAPPED c4x [11, 9, 7, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[7], q[0], q[8];
// UNMAPPED c4x [11, 9, 8, 0, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[8], q[0], q[7];
// UNMAPPED c5x [11, 10, 9, 7, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[7], q[0], q[8];
// UNMAPPED c4x [10, 9, 8, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[0], q[11];
// UNMAPPED c4x [10, 9, 8, 0, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[0], q[7];
// UNMAPPED c5x [11, 9, 8, 7, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[0], q[10];
// UNMAPPED c5x [11, 10, 9, 8, 0, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[8], q[0], q[7];
ccx q[7], q[0], q[11];
ccx q[7], q[0], q[10];
ccx q[7], q[0], q[9];
// UNMAPPED c4x [10, 9, 7, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[0], q[11];
// UNMAPPED c3x [11, 7, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[0], q[10];
// UNMAPPED c3x [11, 7, 0, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[0], q[9];
// UNMAPPED c4x [11, 8, 7, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[0], q[10];
// UNMAPPED c3x [10, 7, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[7], q[0], q[11];
// UNMAPPED c3x [10, 7, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[7], q[0], q[8];
// UNMAPPED c5x [11, 9, 8, 7, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[0], q[10];
// UNMAPPED c4x [11, 10, 7, 0, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[0], q[9];
// UNMAPPED c4x [11, 10, 7, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[0], q[8];
// UNMAPPED c3x [9, 7, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[0], q[11];
// UNMAPPED c3x [9, 7, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[0], q[10];
// UNMAPPED c3x [9, 7, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[0], q[8];
// UNMAPPED c4x [9, 8, 7, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[0], q[11];
// UNMAPPED c4x [11, 9, 7, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[7], q[0], q[8];
// UNMAPPED c4x [10, 9, 7, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[0], q[11];
// UNMAPPED c4x [10, 9, 7, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[0], q[8];
// UNMAPPED c4x [11, 8, 7, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[0], q[10];
// UNMAPPED c5x [11, 10, 8, 7, 0, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[8], q[7], q[0], q[9];
// UNMAPPED c5x [11, 10, 9, 7, 0, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[7], q[0], q[8];
// UNMAPPED c4x [9, 8, 7, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[0], q[11];
// UNMAPPED c4x [11, 8, 7, 0, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[0], q[9];
// UNMAPPED c4x [10, 8, 7, 0, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[8], q[7], q[0], q[9];
// UNMAPPED c4x [9, 8, 7, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[0], q[11];
// UNMAPPED c5x [11, 9, 8, 7, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[0], q[10];
// UNMAPPED c5x [11, 10, 8, 7, 0, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[8], q[7], q[0], q[9];
// UNMAPPED c4x [9, 8, 7, 0, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[0], q[11];
// UNMAPPED c5x [11, 9, 8, 7, 0, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[0], q[10];
ccx q[11], q[1], q[10];
ccx q[11], q[1], q[8];
ccx q[10], q[1], q[11];
ccx q[10], q[1], q[8];
// UNMAPPED c3x [9, 8, 1, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[1], q[11];
// UNMAPPED c4x [11, 9, 8, 1, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[8], q[1], q[10];
// UNMAPPED c3x [11, 10, 1, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[10], q[1], q[9];
// UNMAPPED c3x [11, 10, 1, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[10], q[1], q[8];
ccx q[9], q[1], q[11];
ccx q[9], q[1], q[10];
// UNMAPPED c4x [10, 9, 8, 1, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[1], q[11];
// UNMAPPED c3x [11, 9, 1, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[9], q[1], q[10];
// UNMAPPED c3x [11, 9, 1, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[9], q[1], q[8];
// UNMAPPED c3x [11, 8, 1, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[1], q[10];
// UNMAPPED c4x [11, 10, 8, 1, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[1], q[9];
// UNMAPPED c3x [10, 9, 1, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[9], q[1], q[11];
// UNMAPPED c3x [10, 9, 1, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[9], q[1], q[8];
// UNMAPPED c3x [11, 8, 1, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[1], q[10];
// UNMAPPED c4x [11, 10, 8, 1, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[1], q[9];
// UNMAPPED c4x [11, 10, 9, 1, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[9], q[1], q[8];
ccx q[8], q[1], q[11];
// UNMAPPED c3x [9, 8, 1, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[1], q[11];
// UNMAPPED c3x [11, 8, 1, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[1], q[9];
ccx q[7], q[1], q[11];
// UNMAPPED c3x [11, 7, 1, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[1], q[10];
// UNMAPPED c4x [11, 10, 7, 1, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[1], q[8];
// UNMAPPED c4x [11, 10, 8, 1, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[1], q[7];
// UNMAPPED c3x [9, 8, 1, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[1], q[10];
// UNMAPPED c3x [11, 7, 1, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[1], q[9];
// UNMAPPED c4x [11, 9, 7, 1, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[7], q[1], q[8];
// UNMAPPED c4x [11, 9, 8, 1, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[8], q[1], q[7];
// UNMAPPED c5x [11, 10, 9, 7, 1, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[7], q[1], q[8];
// UNMAPPED c4x [10, 9, 8, 1, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[1], q[11];
// UNMAPPED c4x [10, 9, 8, 1, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[1], q[7];
// UNMAPPED c5x [11, 9, 8, 7, 1, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[1], q[10];
// UNMAPPED c5x [11, 10, 9, 8, 1, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[8], q[1], q[7];
ccx q[7], q[1], q[11];
ccx q[7], q[1], q[10];
ccx q[7], q[1], q[9];
// UNMAPPED c4x [10, 9, 7, 1, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[1], q[11];
// UNMAPPED c3x [11, 7, 1, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[1], q[10];
// UNMAPPED c3x [11, 7, 1, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[1], q[9];
// UNMAPPED c4x [11, 8, 7, 1, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[1], q[10];
// UNMAPPED c3x [10, 7, 1, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[7], q[1], q[11];
// UNMAPPED c3x [10, 7, 1, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[7], q[1], q[8];
// UNMAPPED c5x [11, 9, 8, 7, 1, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[1], q[10];
// UNMAPPED c4x [11, 10, 7, 1, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[1], q[9];
// UNMAPPED c4x [11, 10, 7, 1, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[1], q[8];
// UNMAPPED c3x [9, 7, 1, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[1], q[11];
// UNMAPPED c3x [9, 7, 1, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[1], q[10];
// UNMAPPED c3x [9, 7, 1, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[1], q[8];
// UNMAPPED c4x [9, 8, 7, 1, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[1], q[11];
// UNMAPPED c4x [11, 9, 7, 1, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[7], q[1], q[8];
// UNMAPPED c4x [10, 9, 7, 1, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[1], q[11];
// UNMAPPED c4x [10, 9, 7, 1, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[1], q[8];
// UNMAPPED c4x [11, 8, 7, 1, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[1], q[10];
// UNMAPPED c5x [11, 10, 8, 7, 1, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[8], q[7], q[1], q[9];
// UNMAPPED c5x [11, 10, 9, 7, 1, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[7], q[1], q[8];
// UNMAPPED c4x [9, 8, 7, 1, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[1], q[11];
// UNMAPPED c4x [11, 8, 7, 1, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[1], q[9];
// UNMAPPED c4x [10, 8, 7, 1, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[8], q[7], q[1], q[9];
// UNMAPPED c4x [9, 8, 7, 1, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[1], q[11];
// UNMAPPED c5x [11, 9, 8, 7, 1, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[1], q[10];
// UNMAPPED c5x [11, 10, 8, 7, 1, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[8], q[7], q[1], q[9];
// UNMAPPED c4x [9, 8, 7, 1, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[1], q[11];
// UNMAPPED c5x [11, 9, 8, 7, 1, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[1], q[10];
ccx q[11], q[1], q[10];
ccx q[11], q[1], q[8];
ccx q[10], q[1], q[11];
ccx q[10], q[1], q[8];
// UNMAPPED c3x [9, 8, 1, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[1], q[11];
// UNMAPPED c4x [11, 9, 8, 1, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[8], q[1], q[10];
// UNMAPPED c3x [11, 10, 1, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[10], q[1], q[9];
// UNMAPPED c3x [11, 10, 1, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[10], q[1], q[8];
ccx q[9], q[1], q[11];
ccx q[9], q[1], q[10];
// UNMAPPED c4x [10, 9, 8, 1, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[1], q[11];
// UNMAPPED c3x [11, 9, 1, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[9], q[1], q[10];
// UNMAPPED c3x [11, 9, 1, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[9], q[1], q[8];
// UNMAPPED c3x [11, 8, 1, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[1], q[10];
// UNMAPPED c4x [11, 10, 8, 1, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[1], q[9];
// UNMAPPED c3x [10, 9, 1, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[9], q[1], q[11];
// UNMAPPED c3x [10, 9, 1, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[9], q[1], q[8];
// UNMAPPED c3x [11, 8, 1, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[1], q[10];
// UNMAPPED c4x [11, 10, 8, 1, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[1], q[9];
// UNMAPPED c4x [11, 10, 9, 1, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[9], q[1], q[8];
ccx q[8], q[1], q[11];
// UNMAPPED c3x [9, 8, 1, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[1], q[11];
// UNMAPPED c3x [11, 8, 1, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[1], q[9];
ccx q[7], q[1], q[11];
// UNMAPPED c3x [11, 7, 1, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[1], q[10];
// UNMAPPED c4x [11, 10, 7, 1, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[1], q[8];
// UNMAPPED c4x [11, 10, 8, 1, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[1], q[7];
// UNMAPPED c3x [9, 8, 1, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[1], q[10];
// UNMAPPED c3x [11, 7, 1, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[1], q[9];
// UNMAPPED c4x [11, 9, 7, 1, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[7], q[1], q[8];
// UNMAPPED c4x [11, 9, 8, 1, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[8], q[1], q[7];
// UNMAPPED c5x [11, 10, 9, 7, 1, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[7], q[1], q[8];
// UNMAPPED c4x [10, 9, 8, 1, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[1], q[11];
// UNMAPPED c4x [10, 9, 8, 1, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[1], q[7];
// UNMAPPED c5x [11, 9, 8, 7, 1, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[1], q[10];
// UNMAPPED c5x [11, 10, 9, 8, 1, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[8], q[1], q[7];
ccx q[7], q[1], q[11];
ccx q[7], q[1], q[10];
ccx q[7], q[1], q[9];
// UNMAPPED c4x [10, 9, 7, 1, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[1], q[11];
// UNMAPPED c3x [11, 7, 1, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[1], q[10];
// UNMAPPED c3x [11, 7, 1, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[1], q[9];
// UNMAPPED c4x [11, 8, 7, 1, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[1], q[10];
// UNMAPPED c3x [10, 7, 1, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[7], q[1], q[11];
// UNMAPPED c3x [10, 7, 1, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[7], q[1], q[8];
// UNMAPPED c5x [11, 9, 8, 7, 1, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[1], q[10];
// UNMAPPED c4x [11, 10, 7, 1, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[1], q[9];
// UNMAPPED c4x [11, 10, 7, 1, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[1], q[8];
// UNMAPPED c3x [9, 7, 1, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[1], q[11];
// UNMAPPED c3x [9, 7, 1, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[1], q[10];
// UNMAPPED c3x [9, 7, 1, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[1], q[8];
// UNMAPPED c4x [9, 8, 7, 1, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[1], q[11];
// UNMAPPED c4x [11, 9, 7, 1, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[7], q[1], q[8];
// UNMAPPED c4x [10, 9, 7, 1, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[1], q[11];
// UNMAPPED c4x [10, 9, 7, 1, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[1], q[8];
// UNMAPPED c4x [11, 8, 7, 1, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[1], q[10];
// UNMAPPED c5x [11, 10, 8, 7, 1, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[8], q[7], q[1], q[9];
// UNMAPPED c5x [11, 10, 9, 7, 1, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[7], q[1], q[8];
// UNMAPPED c4x [9, 8, 7, 1, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[1], q[11];
// UNMAPPED c4x [11, 8, 7, 1, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[1], q[9];
// UNMAPPED c4x [10, 8, 7, 1, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[8], q[7], q[1], q[9];
// UNMAPPED c4x [9, 8, 7, 1, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[1], q[11];
// UNMAPPED c5x [11, 9, 8, 7, 1, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[1], q[10];
// UNMAPPED c5x [11, 10, 8, 7, 1, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[8], q[7], q[1], q[9];
// UNMAPPED c4x [9, 8, 7, 1, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[1], q[11];
// UNMAPPED c5x [11, 9, 8, 7, 1, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[1], q[10];
ccx q[11], q[2], q[10];
ccx q[11], q[2], q[8];
ccx q[10], q[2], q[11];
ccx q[10], q[2], q[8];
// UNMAPPED c3x [9, 8, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[2], q[11];
// UNMAPPED c4x [11, 9, 8, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[8], q[2], q[10];
// UNMAPPED c3x [11, 10, 2, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[10], q[2], q[9];
// UNMAPPED c3x [11, 10, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[10], q[2], q[8];
ccx q[9], q[2], q[11];
ccx q[9], q[2], q[10];
// UNMAPPED c4x [10, 9, 8, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[2], q[11];
// UNMAPPED c3x [11, 9, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[9], q[2], q[10];
// UNMAPPED c3x [11, 9, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[9], q[2], q[8];
// UNMAPPED c3x [11, 8, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[2], q[10];
// UNMAPPED c4x [11, 10, 8, 2, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[2], q[9];
// UNMAPPED c3x [10, 9, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[9], q[2], q[11];
// UNMAPPED c3x [10, 9, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[9], q[2], q[8];
// UNMAPPED c3x [11, 8, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[2], q[10];
// UNMAPPED c4x [11, 10, 8, 2, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[2], q[9];
// UNMAPPED c4x [11, 10, 9, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[9], q[2], q[8];
ccx q[8], q[2], q[11];
// UNMAPPED c3x [9, 8, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[2], q[11];
// UNMAPPED c3x [11, 8, 2, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[2], q[9];
ccx q[7], q[2], q[11];
// UNMAPPED c3x [11, 7, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[2], q[10];
// UNMAPPED c4x [11, 10, 7, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[2], q[8];
// UNMAPPED c4x [11, 10, 8, 2, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[2], q[7];
// UNMAPPED c3x [9, 8, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[2], q[10];
// UNMAPPED c3x [11, 7, 2, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[2], q[9];
// UNMAPPED c4x [11, 9, 7, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[7], q[2], q[8];
// UNMAPPED c4x [11, 9, 8, 2, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[8], q[2], q[7];
// UNMAPPED c5x [11, 10, 9, 7, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[7], q[2], q[8];
// UNMAPPED c4x [10, 9, 8, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[2], q[11];
// UNMAPPED c4x [10, 9, 8, 2, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[2], q[7];
// UNMAPPED c5x [11, 9, 8, 7, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[2], q[10];
// UNMAPPED c5x [11, 10, 9, 8, 2, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[8], q[2], q[7];
ccx q[7], q[2], q[11];
ccx q[7], q[2], q[10];
ccx q[7], q[2], q[9];
// UNMAPPED c4x [10, 9, 7, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[2], q[11];
// UNMAPPED c3x [11, 7, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[2], q[10];
// UNMAPPED c3x [11, 7, 2, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[2], q[9];
// UNMAPPED c4x [11, 8, 7, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[2], q[10];
// UNMAPPED c3x [10, 7, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[7], q[2], q[11];
// UNMAPPED c3x [10, 7, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[7], q[2], q[8];
// UNMAPPED c5x [11, 9, 8, 7, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[2], q[10];
// UNMAPPED c4x [11, 10, 7, 2, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[2], q[9];
// UNMAPPED c4x [11, 10, 7, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[2], q[8];
// UNMAPPED c3x [9, 7, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[2], q[11];
// UNMAPPED c3x [9, 7, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[2], q[10];
// UNMAPPED c3x [9, 7, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[2], q[8];
// UNMAPPED c4x [9, 8, 7, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[2], q[11];
// UNMAPPED c4x [11, 9, 7, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[7], q[2], q[8];
// UNMAPPED c4x [10, 9, 7, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[2], q[11];
// UNMAPPED c4x [10, 9, 7, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[2], q[8];
// UNMAPPED c4x [11, 8, 7, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[2], q[10];
// UNMAPPED c5x [11, 10, 8, 7, 2, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[8], q[7], q[2], q[9];
// UNMAPPED c5x [11, 10, 9, 7, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[7], q[2], q[8];
// UNMAPPED c4x [9, 8, 7, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[2], q[11];
// UNMAPPED c4x [11, 8, 7, 2, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[2], q[9];
// UNMAPPED c4x [10, 8, 7, 2, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[8], q[7], q[2], q[9];
// UNMAPPED c4x [9, 8, 7, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[2], q[11];
// UNMAPPED c5x [11, 9, 8, 7, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[2], q[10];
// UNMAPPED c5x [11, 10, 8, 7, 2, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[8], q[7], q[2], q[9];
// UNMAPPED c4x [9, 8, 7, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[2], q[11];
// UNMAPPED c5x [11, 9, 8, 7, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[2], q[10];
ccx q[11], q[2], q[10];
ccx q[11], q[2], q[8];
ccx q[10], q[2], q[11];
ccx q[10], q[2], q[8];
// UNMAPPED c3x [9, 8, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[2], q[11];
// UNMAPPED c4x [11, 9, 8, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[8], q[2], q[10];
// UNMAPPED c3x [11, 10, 2, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[10], q[2], q[9];
// UNMAPPED c3x [11, 10, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[10], q[2], q[8];
ccx q[9], q[2], q[11];
ccx q[9], q[2], q[10];
// UNMAPPED c4x [10, 9, 8, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[2], q[11];
// UNMAPPED c3x [11, 9, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[9], q[2], q[10];
// UNMAPPED c3x [11, 9, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[9], q[2], q[8];
// UNMAPPED c3x [11, 8, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[2], q[10];
// UNMAPPED c4x [11, 10, 8, 2, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[2], q[9];
// UNMAPPED c3x [10, 9, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[9], q[2], q[11];
// UNMAPPED c3x [10, 9, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[9], q[2], q[8];
// UNMAPPED c3x [11, 8, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[2], q[10];
// UNMAPPED c4x [11, 10, 8, 2, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[2], q[9];
// UNMAPPED c4x [11, 10, 9, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[9], q[2], q[8];
ccx q[8], q[2], q[11];
// UNMAPPED c3x [9, 8, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[2], q[11];
// UNMAPPED c3x [11, 8, 2, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[2], q[9];
ccx q[7], q[2], q[11];
// UNMAPPED c3x [11, 7, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[2], q[10];
// UNMAPPED c4x [11, 10, 7, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[2], q[8];
// UNMAPPED c4x [11, 10, 8, 2, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[2], q[7];
// UNMAPPED c3x [9, 8, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[2], q[10];
// UNMAPPED c3x [11, 7, 2, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[2], q[9];
// UNMAPPED c4x [11, 9, 7, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[7], q[2], q[8];
// UNMAPPED c4x [11, 9, 8, 2, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[8], q[2], q[7];
// UNMAPPED c5x [11, 10, 9, 7, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[7], q[2], q[8];
// UNMAPPED c4x [10, 9, 8, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[2], q[11];
// UNMAPPED c4x [10, 9, 8, 2, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[2], q[7];
// UNMAPPED c5x [11, 9, 8, 7, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[2], q[10];
// UNMAPPED c5x [11, 10, 9, 8, 2, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[8], q[2], q[7];
ccx q[7], q[2], q[11];
ccx q[7], q[2], q[10];
ccx q[7], q[2], q[9];
// UNMAPPED c4x [10, 9, 7, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[2], q[11];
// UNMAPPED c3x [11, 7, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[2], q[10];
// UNMAPPED c3x [11, 7, 2, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[2], q[9];
// UNMAPPED c4x [11, 8, 7, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[2], q[10];
// UNMAPPED c3x [10, 7, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[7], q[2], q[11];
// UNMAPPED c3x [10, 7, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[7], q[2], q[8];
// UNMAPPED c5x [11, 9, 8, 7, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[2], q[10];
// UNMAPPED c4x [11, 10, 7, 2, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[2], q[9];
// UNMAPPED c4x [11, 10, 7, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[2], q[8];
// UNMAPPED c3x [9, 7, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[2], q[11];
// UNMAPPED c3x [9, 7, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[2], q[10];
// UNMAPPED c3x [9, 7, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[2], q[8];
// UNMAPPED c4x [9, 8, 7, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[2], q[11];
// UNMAPPED c4x [11, 9, 7, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[7], q[2], q[8];
// UNMAPPED c4x [10, 9, 7, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[2], q[11];
// UNMAPPED c4x [10, 9, 7, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[2], q[8];
// UNMAPPED c4x [11, 8, 7, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[2], q[10];
// UNMAPPED c5x [11, 10, 8, 7, 2, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[8], q[7], q[2], q[9];
// UNMAPPED c5x [11, 10, 9, 7, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[7], q[2], q[8];
// UNMAPPED c4x [9, 8, 7, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[2], q[11];
// UNMAPPED c4x [11, 8, 7, 2, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[2], q[9];
// UNMAPPED c4x [10, 8, 7, 2, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[8], q[7], q[2], q[9];
// UNMAPPED c4x [9, 8, 7, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[2], q[11];
// UNMAPPED c5x [11, 9, 8, 7, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[2], q[10];
// UNMAPPED c5x [11, 10, 8, 7, 2, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[8], q[7], q[2], q[9];
// UNMAPPED c4x [9, 8, 7, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[2], q[11];
// UNMAPPED c5x [11, 9, 8, 7, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[2], q[10];
ccx q[11], q[2], q[10];
ccx q[11], q[2], q[8];
ccx q[10], q[2], q[11];
ccx q[10], q[2], q[8];
// UNMAPPED c3x [9, 8, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[2], q[11];
// UNMAPPED c4x [11, 9, 8, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[8], q[2], q[10];
// UNMAPPED c3x [11, 10, 2, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[10], q[2], q[9];
// UNMAPPED c3x [11, 10, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[10], q[2], q[8];
ccx q[9], q[2], q[11];
ccx q[9], q[2], q[10];
// UNMAPPED c4x [10, 9, 8, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[2], q[11];
// UNMAPPED c3x [11, 9, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[9], q[2], q[10];
// UNMAPPED c3x [11, 9, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[9], q[2], q[8];
// UNMAPPED c3x [11, 8, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[2], q[10];
// UNMAPPED c4x [11, 10, 8, 2, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[2], q[9];
// UNMAPPED c3x [10, 9, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[9], q[2], q[11];
// UNMAPPED c3x [10, 9, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[9], q[2], q[8];
// UNMAPPED c3x [11, 8, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[2], q[10];
// UNMAPPED c4x [11, 10, 8, 2, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[2], q[9];
// UNMAPPED c4x [11, 10, 9, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[9], q[2], q[8];
ccx q[8], q[2], q[11];
// UNMAPPED c3x [9, 8, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[2], q[11];
// UNMAPPED c3x [11, 8, 2, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[2], q[9];
ccx q[7], q[2], q[11];
// UNMAPPED c3x [11, 7, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[2], q[10];
// UNMAPPED c4x [11, 10, 7, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[2], q[8];
// UNMAPPED c4x [11, 10, 8, 2, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[2], q[7];
// UNMAPPED c3x [9, 8, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[2], q[10];
// UNMAPPED c3x [11, 7, 2, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[2], q[9];
// UNMAPPED c4x [11, 9, 7, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[7], q[2], q[8];
// UNMAPPED c4x [11, 9, 8, 2, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[8], q[2], q[7];
// UNMAPPED c5x [11, 10, 9, 7, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[7], q[2], q[8];
// UNMAPPED c4x [10, 9, 8, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[2], q[11];
// UNMAPPED c4x [10, 9, 8, 2, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[2], q[7];
// UNMAPPED c5x [11, 9, 8, 7, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[2], q[10];
// UNMAPPED c5x [11, 10, 9, 8, 2, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[8], q[2], q[7];
ccx q[7], q[2], q[11];
ccx q[7], q[2], q[10];
ccx q[7], q[2], q[9];
// UNMAPPED c4x [10, 9, 7, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[2], q[11];
// UNMAPPED c3x [11, 7, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[2], q[10];
// UNMAPPED c3x [11, 7, 2, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[2], q[9];
// UNMAPPED c4x [11, 8, 7, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[2], q[10];
// UNMAPPED c3x [10, 7, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[7], q[2], q[11];
// UNMAPPED c3x [10, 7, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[7], q[2], q[8];
// UNMAPPED c5x [11, 9, 8, 7, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[2], q[10];
// UNMAPPED c4x [11, 10, 7, 2, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[2], q[9];
// UNMAPPED c4x [11, 10, 7, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[2], q[8];
// UNMAPPED c3x [9, 7, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[2], q[11];
// UNMAPPED c3x [9, 7, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[2], q[10];
// UNMAPPED c3x [9, 7, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[2], q[8];
// UNMAPPED c4x [9, 8, 7, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[2], q[11];
// UNMAPPED c4x [11, 9, 7, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[7], q[2], q[8];
// UNMAPPED c4x [10, 9, 7, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[2], q[11];
// UNMAPPED c4x [10, 9, 7, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[2], q[8];
// UNMAPPED c4x [11, 8, 7, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[2], q[10];
// UNMAPPED c5x [11, 10, 8, 7, 2, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[8], q[7], q[2], q[9];
// UNMAPPED c5x [11, 10, 9, 7, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[7], q[2], q[8];
// UNMAPPED c4x [9, 8, 7, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[2], q[11];
// UNMAPPED c4x [11, 8, 7, 2, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[2], q[9];
// UNMAPPED c4x [10, 8, 7, 2, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[8], q[7], q[2], q[9];
// UNMAPPED c4x [9, 8, 7, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[2], q[11];
// UNMAPPED c5x [11, 9, 8, 7, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[2], q[10];
// UNMAPPED c5x [11, 10, 8, 7, 2, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[8], q[7], q[2], q[9];
// UNMAPPED c4x [9, 8, 7, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[2], q[11];
// UNMAPPED c5x [11, 9, 8, 7, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[2], q[10];
ccx q[11], q[2], q[10];
ccx q[11], q[2], q[8];
ccx q[10], q[2], q[11];
ccx q[10], q[2], q[8];
// UNMAPPED c3x [9, 8, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[2], q[11];
// UNMAPPED c4x [11, 9, 8, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[8], q[2], q[10];
// UNMAPPED c3x [11, 10, 2, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[10], q[2], q[9];
// UNMAPPED c3x [11, 10, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[10], q[2], q[8];
ccx q[9], q[2], q[11];
ccx q[9], q[2], q[10];
// UNMAPPED c4x [10, 9, 8, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[2], q[11];
// UNMAPPED c3x [11, 9, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[9], q[2], q[10];
// UNMAPPED c3x [11, 9, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[9], q[2], q[8];
// UNMAPPED c3x [11, 8, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[2], q[10];
// UNMAPPED c4x [11, 10, 8, 2, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[2], q[9];
// UNMAPPED c3x [10, 9, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[9], q[2], q[11];
// UNMAPPED c3x [10, 9, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[9], q[2], q[8];
// UNMAPPED c3x [11, 8, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[2], q[10];
// UNMAPPED c4x [11, 10, 8, 2, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[2], q[9];
// UNMAPPED c4x [11, 10, 9, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[9], q[2], q[8];
ccx q[8], q[2], q[11];
// UNMAPPED c3x [9, 8, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[2], q[11];
// UNMAPPED c3x [11, 8, 2, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[2], q[9];
ccx q[7], q[2], q[11];
// UNMAPPED c3x [11, 7, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[2], q[10];
// UNMAPPED c4x [11, 10, 7, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[2], q[8];
// UNMAPPED c4x [11, 10, 8, 2, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[2], q[7];
// UNMAPPED c3x [9, 8, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[2], q[10];
// UNMAPPED c3x [11, 7, 2, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[2], q[9];
// UNMAPPED c4x [11, 9, 7, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[7], q[2], q[8];
// UNMAPPED c4x [11, 9, 8, 2, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[8], q[2], q[7];
// UNMAPPED c5x [11, 10, 9, 7, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[7], q[2], q[8];
// UNMAPPED c4x [10, 9, 8, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[2], q[11];
// UNMAPPED c4x [10, 9, 8, 2, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[2], q[7];
// UNMAPPED c5x [11, 9, 8, 7, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[2], q[10];
// UNMAPPED c5x [11, 10, 9, 8, 2, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[8], q[2], q[7];
ccx q[7], q[2], q[11];
ccx q[7], q[2], q[10];
ccx q[7], q[2], q[9];
// UNMAPPED c4x [10, 9, 7, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[2], q[11];
// UNMAPPED c3x [11, 7, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[2], q[10];
// UNMAPPED c3x [11, 7, 2, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[2], q[9];
// UNMAPPED c4x [11, 8, 7, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[2], q[10];
// UNMAPPED c3x [10, 7, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[7], q[2], q[11];
// UNMAPPED c3x [10, 7, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[7], q[2], q[8];
// UNMAPPED c5x [11, 9, 8, 7, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[2], q[10];
// UNMAPPED c4x [11, 10, 7, 2, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[2], q[9];
// UNMAPPED c4x [11, 10, 7, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[2], q[8];
// UNMAPPED c3x [9, 7, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[2], q[11];
// UNMAPPED c3x [9, 7, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[2], q[10];
// UNMAPPED c3x [9, 7, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[2], q[8];
// UNMAPPED c4x [9, 8, 7, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[2], q[11];
// UNMAPPED c4x [11, 9, 7, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[7], q[2], q[8];
// UNMAPPED c4x [10, 9, 7, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[2], q[11];
// UNMAPPED c4x [10, 9, 7, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[2], q[8];
// UNMAPPED c4x [11, 8, 7, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[2], q[10];
// UNMAPPED c5x [11, 10, 8, 7, 2, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[8], q[7], q[2], q[9];
// UNMAPPED c5x [11, 10, 9, 7, 2, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[7], q[2], q[8];
// UNMAPPED c4x [9, 8, 7, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[2], q[11];
// UNMAPPED c4x [11, 8, 7, 2, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[2], q[9];
// UNMAPPED c4x [10, 8, 7, 2, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[8], q[7], q[2], q[9];
// UNMAPPED c4x [9, 8, 7, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[2], q[11];
// UNMAPPED c5x [11, 9, 8, 7, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[2], q[10];
// UNMAPPED c5x [11, 10, 8, 7, 2, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[8], q[7], q[2], q[9];
// UNMAPPED c4x [9, 8, 7, 2, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[2], q[11];
// UNMAPPED c5x [11, 9, 8, 7, 2, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[2], q[10];
ccx q[11], q[3], q[10];
ccx q[11], q[3], q[8];
ccx q[10], q[3], q[11];
ccx q[10], q[3], q[8];
// UNMAPPED c3x [9, 8, 3, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[3], q[11];
// UNMAPPED c4x [11, 9, 8, 3, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[8], q[3], q[10];
// UNMAPPED c3x [11, 10, 3, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[10], q[3], q[9];
// UNMAPPED c3x [11, 10, 3, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[10], q[3], q[8];
ccx q[9], q[3], q[11];
ccx q[9], q[3], q[10];
// UNMAPPED c4x [10, 9, 8, 3, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[3], q[11];
// UNMAPPED c3x [11, 9, 3, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[9], q[3], q[10];
// UNMAPPED c3x [11, 9, 3, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[9], q[3], q[8];
// UNMAPPED c3x [11, 8, 3, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[3], q[10];
// UNMAPPED c4x [11, 10, 8, 3, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[3], q[9];
// UNMAPPED c3x [10, 9, 3, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[9], q[3], q[11];
// UNMAPPED c3x [10, 9, 3, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[9], q[3], q[8];
// UNMAPPED c3x [11, 8, 3, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[3], q[10];
// UNMAPPED c4x [11, 10, 8, 3, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[3], q[9];
// UNMAPPED c4x [11, 10, 9, 3, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[9], q[3], q[8];
ccx q[8], q[3], q[11];
// UNMAPPED c3x [9, 8, 3, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[3], q[11];
// UNMAPPED c3x [11, 8, 3, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[3], q[9];
ccx q[7], q[3], q[11];
// UNMAPPED c3x [11, 7, 3, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[3], q[10];
// UNMAPPED c4x [11, 10, 7, 3, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[3], q[8];
// UNMAPPED c4x [11, 10, 8, 3, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[3], q[7];
// UNMAPPED c3x [9, 8, 3, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[3], q[10];
// UNMAPPED c3x [11, 7, 3, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[3], q[9];
// UNMAPPED c4x [11, 9, 7, 3, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[7], q[3], q[8];
// UNMAPPED c4x [11, 9, 8, 3, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[8], q[3], q[7];
// UNMAPPED c5x [11, 10, 9, 7, 3, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[7], q[3], q[8];
// UNMAPPED c4x [10, 9, 8, 3, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[3], q[11];
// UNMAPPED c4x [10, 9, 8, 3, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[3], q[7];
// UNMAPPED c5x [11, 9, 8, 7, 3, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[3], q[10];
// UNMAPPED c5x [11, 10, 9, 8, 3, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[8], q[3], q[7];
ccx q[7], q[3], q[11];
ccx q[7], q[3], q[10];
ccx q[7], q[3], q[9];
// UNMAPPED c4x [10, 9, 7, 3, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[3], q[11];
// UNMAPPED c3x [11, 7, 3, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[3], q[10];
// UNMAPPED c3x [11, 7, 3, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[3], q[9];
// UNMAPPED c4x [11, 8, 7, 3, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[3], q[10];
// UNMAPPED c3x [10, 7, 3, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[7], q[3], q[11];
// UNMAPPED c3x [10, 7, 3, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[7], q[3], q[8];
// UNMAPPED c5x [11, 9, 8, 7, 3, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[3], q[10];
// UNMAPPED c4x [11, 10, 7, 3, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[3], q[9];
// UNMAPPED c4x [11, 10, 7, 3, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[3], q[8];
// UNMAPPED c3x [9, 7, 3, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[3], q[11];
// UNMAPPED c3x [9, 7, 3, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[3], q[10];
// UNMAPPED c3x [9, 7, 3, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[3], q[8];
// UNMAPPED c4x [9, 8, 7, 3, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[3], q[11];
// UNMAPPED c4x [11, 9, 7, 3, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[7], q[3], q[8];
// UNMAPPED c4x [10, 9, 7, 3, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[3], q[11];
// UNMAPPED c4x [10, 9, 7, 3, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[3], q[8];
// UNMAPPED c4x [11, 8, 7, 3, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[3], q[10];
// UNMAPPED c5x [11, 10, 8, 7, 3, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[8], q[7], q[3], q[9];
// UNMAPPED c5x [11, 10, 9, 7, 3, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[7], q[3], q[8];
// UNMAPPED c4x [9, 8, 7, 3, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[3], q[11];
// UNMAPPED c4x [11, 8, 7, 3, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[3], q[9];
// UNMAPPED c4x [10, 8, 7, 3, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[8], q[7], q[3], q[9];
// UNMAPPED c4x [9, 8, 7, 3, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[3], q[11];
// UNMAPPED c5x [11, 9, 8, 7, 3, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[3], q[10];
// UNMAPPED c5x [11, 10, 8, 7, 3, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[8], q[7], q[3], q[9];
// UNMAPPED c4x [9, 8, 7, 3, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[3], q[11];
// UNMAPPED c5x [11, 9, 8, 7, 3, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[3], q[10];
ccx q[11], q[3], q[10];
ccx q[11], q[3], q[8];
ccx q[10], q[3], q[11];
ccx q[10], q[3], q[8];
// UNMAPPED c3x [9, 8, 3, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[3], q[11];
// UNMAPPED c4x [11, 9, 8, 3, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[8], q[3], q[10];
// UNMAPPED c3x [11, 10, 3, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[10], q[3], q[9];
// UNMAPPED c3x [11, 10, 3, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[10], q[3], q[8];
ccx q[9], q[3], q[11];
ccx q[9], q[3], q[10];
// UNMAPPED c4x [10, 9, 8, 3, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[3], q[11];
// UNMAPPED c3x [11, 9, 3, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[9], q[3], q[10];
// UNMAPPED c3x [11, 9, 3, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[9], q[3], q[8];
// UNMAPPED c3x [11, 8, 3, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[3], q[10];
// UNMAPPED c4x [11, 10, 8, 3, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[3], q[9];
// UNMAPPED c3x [10, 9, 3, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[9], q[3], q[11];
// UNMAPPED c3x [10, 9, 3, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[9], q[3], q[8];
// UNMAPPED c3x [11, 8, 3, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[3], q[10];
// UNMAPPED c4x [11, 10, 8, 3, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[3], q[9];
// UNMAPPED c4x [11, 10, 9, 3, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[9], q[3], q[8];
ccx q[8], q[3], q[11];
// UNMAPPED c3x [9, 8, 3, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[3], q[11];
// UNMAPPED c3x [11, 8, 3, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[3], q[9];
ccx q[7], q[3], q[11];
// UNMAPPED c3x [11, 7, 3, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[3], q[10];
// UNMAPPED c4x [11, 10, 7, 3, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[3], q[8];
// UNMAPPED c4x [11, 10, 8, 3, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[3], q[7];
// UNMAPPED c3x [9, 8, 3, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[3], q[10];
// UNMAPPED c3x [11, 7, 3, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[3], q[9];
// UNMAPPED c4x [11, 9, 7, 3, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[7], q[3], q[8];
// UNMAPPED c4x [11, 9, 8, 3, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[8], q[3], q[7];
// UNMAPPED c5x [11, 10, 9, 7, 3, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[7], q[3], q[8];
// UNMAPPED c4x [10, 9, 8, 3, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[3], q[11];
// UNMAPPED c4x [10, 9, 8, 3, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[3], q[7];
// UNMAPPED c5x [11, 9, 8, 7, 3, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[3], q[10];
// UNMAPPED c5x [11, 10, 9, 8, 3, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[8], q[3], q[7];
ccx q[7], q[3], q[11];
ccx q[7], q[3], q[10];
ccx q[7], q[3], q[9];
// UNMAPPED c4x [10, 9, 7, 3, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[3], q[11];
// UNMAPPED c3x [11, 7, 3, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[3], q[10];
// UNMAPPED c3x [11, 7, 3, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[3], q[9];
// UNMAPPED c4x [11, 8, 7, 3, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[3], q[10];
// UNMAPPED c3x [10, 7, 3, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[7], q[3], q[11];
// UNMAPPED c3x [10, 7, 3, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[7], q[3], q[8];
// UNMAPPED c5x [11, 9, 8, 7, 3, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[3], q[10];
// UNMAPPED c4x [11, 10, 7, 3, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[3], q[9];
// UNMAPPED c4x [11, 10, 7, 3, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[3], q[8];
// UNMAPPED c3x [9, 7, 3, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[3], q[11];
// UNMAPPED c3x [9, 7, 3, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[3], q[10];
// UNMAPPED c3x [9, 7, 3, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[3], q[8];
// UNMAPPED c4x [9, 8, 7, 3, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[3], q[11];
// UNMAPPED c4x [11, 9, 7, 3, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[7], q[3], q[8];
// UNMAPPED c4x [10, 9, 7, 3, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[3], q[11];
// UNMAPPED c4x [10, 9, 7, 3, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[3], q[8];
// UNMAPPED c4x [11, 8, 7, 3, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[3], q[10];
// UNMAPPED c5x [11, 10, 8, 7, 3, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[8], q[7], q[3], q[9];
// UNMAPPED c5x [11, 10, 9, 7, 3, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[7], q[3], q[8];
// UNMAPPED c4x [9, 8, 7, 3, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[3], q[11];
// UNMAPPED c4x [11, 8, 7, 3, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[3], q[9];
// UNMAPPED c4x [10, 8, 7, 3, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[8], q[7], q[3], q[9];
// UNMAPPED c4x [9, 8, 7, 3, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[3], q[11];
// UNMAPPED c5x [11, 9, 8, 7, 3, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[3], q[10];
// UNMAPPED c5x [11, 10, 8, 7, 3, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[8], q[7], q[3], q[9];
// UNMAPPED c4x [9, 8, 7, 3, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[3], q[11];
// UNMAPPED c5x [11, 9, 8, 7, 3, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[3], q[10];
ccx q[11], q[4], q[10];
ccx q[11], q[4], q[8];
ccx q[10], q[4], q[11];
ccx q[10], q[4], q[8];
// UNMAPPED c3x [9, 8, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[4], q[11];
// UNMAPPED c4x [11, 9, 8, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[8], q[4], q[10];
// UNMAPPED c3x [11, 10, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[10], q[4], q[9];
// UNMAPPED c3x [11, 10, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[10], q[4], q[8];
ccx q[9], q[4], q[11];
ccx q[9], q[4], q[10];
// UNMAPPED c4x [10, 9, 8, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[4], q[11];
// UNMAPPED c3x [11, 9, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[9], q[4], q[10];
// UNMAPPED c3x [11, 9, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[9], q[4], q[8];
// UNMAPPED c3x [11, 8, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[4], q[10];
// UNMAPPED c4x [11, 10, 8, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[4], q[9];
// UNMAPPED c3x [10, 9, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[9], q[4], q[11];
// UNMAPPED c3x [10, 9, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[9], q[4], q[8];
// UNMAPPED c3x [11, 8, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[4], q[10];
// UNMAPPED c4x [11, 10, 8, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[4], q[9];
// UNMAPPED c4x [11, 10, 9, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[9], q[4], q[8];
ccx q[8], q[4], q[11];
// UNMAPPED c3x [9, 8, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[4], q[11];
// UNMAPPED c3x [11, 8, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[4], q[9];
ccx q[7], q[4], q[11];
// UNMAPPED c3x [11, 7, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[4], q[10];
// UNMAPPED c4x [11, 10, 7, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[4], q[8];
// UNMAPPED c4x [11, 10, 8, 4, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[4], q[7];
// UNMAPPED c3x [9, 8, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[4], q[10];
// UNMAPPED c3x [11, 7, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[4], q[9];
// UNMAPPED c4x [11, 9, 7, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[7], q[4], q[8];
// UNMAPPED c4x [11, 9, 8, 4, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[8], q[4], q[7];
// UNMAPPED c5x [11, 10, 9, 7, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[7], q[4], q[8];
// UNMAPPED c4x [10, 9, 8, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[4], q[11];
// UNMAPPED c4x [10, 9, 8, 4, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[4], q[7];
// UNMAPPED c5x [11, 9, 8, 7, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[4], q[10];
// UNMAPPED c5x [11, 10, 9, 8, 4, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[8], q[4], q[7];
ccx q[7], q[4], q[11];
ccx q[7], q[4], q[10];
ccx q[7], q[4], q[9];
// UNMAPPED c4x [10, 9, 7, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[4], q[11];
// UNMAPPED c3x [11, 7, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[4], q[10];
// UNMAPPED c3x [11, 7, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[4], q[9];
// UNMAPPED c4x [11, 8, 7, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[4], q[10];
// UNMAPPED c3x [10, 7, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[7], q[4], q[11];
// UNMAPPED c3x [10, 7, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[7], q[4], q[8];
// UNMAPPED c5x [11, 9, 8, 7, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[4], q[10];
// UNMAPPED c4x [11, 10, 7, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[4], q[9];
// UNMAPPED c4x [11, 10, 7, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[4], q[8];
// UNMAPPED c3x [9, 7, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[4], q[11];
// UNMAPPED c3x [9, 7, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[4], q[10];
// UNMAPPED c3x [9, 7, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[4], q[8];
// UNMAPPED c4x [9, 8, 7, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[4], q[11];
// UNMAPPED c4x [11, 9, 7, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[7], q[4], q[8];
// UNMAPPED c4x [10, 9, 7, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[4], q[11];
// UNMAPPED c4x [10, 9, 7, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[4], q[8];
// UNMAPPED c4x [11, 8, 7, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[4], q[10];
// UNMAPPED c5x [11, 10, 8, 7, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[8], q[7], q[4], q[9];
// UNMAPPED c5x [11, 10, 9, 7, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[7], q[4], q[8];
// UNMAPPED c4x [9, 8, 7, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[4], q[11];
// UNMAPPED c4x [11, 8, 7, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[4], q[9];
// UNMAPPED c4x [10, 8, 7, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[8], q[7], q[4], q[9];
// UNMAPPED c4x [9, 8, 7, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[4], q[11];
// UNMAPPED c5x [11, 9, 8, 7, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[4], q[10];
// UNMAPPED c5x [11, 10, 8, 7, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[8], q[7], q[4], q[9];
// UNMAPPED c4x [9, 8, 7, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[4], q[11];
// UNMAPPED c5x [11, 9, 8, 7, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[4], q[10];
ccx q[11], q[4], q[10];
ccx q[11], q[4], q[8];
ccx q[10], q[4], q[11];
ccx q[10], q[4], q[8];
// UNMAPPED c3x [9, 8, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[4], q[11];
// UNMAPPED c4x [11, 9, 8, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[8], q[4], q[10];
// UNMAPPED c3x [11, 10, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[10], q[4], q[9];
// UNMAPPED c3x [11, 10, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[10], q[4], q[8];
ccx q[9], q[4], q[11];
ccx q[9], q[4], q[10];
// UNMAPPED c4x [10, 9, 8, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[4], q[11];
// UNMAPPED c3x [11, 9, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[9], q[4], q[10];
// UNMAPPED c3x [11, 9, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[9], q[4], q[8];
// UNMAPPED c3x [11, 8, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[4], q[10];
// UNMAPPED c4x [11, 10, 8, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[4], q[9];
// UNMAPPED c3x [10, 9, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[9], q[4], q[11];
// UNMAPPED c3x [10, 9, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[9], q[4], q[8];
// UNMAPPED c3x [11, 8, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[4], q[10];
// UNMAPPED c4x [11, 10, 8, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[4], q[9];
// UNMAPPED c4x [11, 10, 9, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[9], q[4], q[8];
ccx q[8], q[4], q[11];
// UNMAPPED c3x [9, 8, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[4], q[11];
// UNMAPPED c3x [11, 8, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[4], q[9];
ccx q[7], q[4], q[11];
// UNMAPPED c3x [11, 7, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[4], q[10];
// UNMAPPED c4x [11, 10, 7, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[4], q[8];
// UNMAPPED c4x [11, 10, 8, 4, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[4], q[7];
// UNMAPPED c3x [9, 8, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[4], q[10];
// UNMAPPED c3x [11, 7, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[4], q[9];
// UNMAPPED c4x [11, 9, 7, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[7], q[4], q[8];
// UNMAPPED c4x [11, 9, 8, 4, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[8], q[4], q[7];
// UNMAPPED c5x [11, 10, 9, 7, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[7], q[4], q[8];
// UNMAPPED c4x [10, 9, 8, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[4], q[11];
// UNMAPPED c4x [10, 9, 8, 4, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[4], q[7];
// UNMAPPED c5x [11, 9, 8, 7, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[4], q[10];
// UNMAPPED c5x [11, 10, 9, 8, 4, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[8], q[4], q[7];
ccx q[7], q[4], q[11];
ccx q[7], q[4], q[10];
ccx q[7], q[4], q[9];
// UNMAPPED c4x [10, 9, 7, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[4], q[11];
// UNMAPPED c3x [11, 7, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[4], q[10];
// UNMAPPED c3x [11, 7, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[4], q[9];
// UNMAPPED c4x [11, 8, 7, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[4], q[10];
// UNMAPPED c3x [10, 7, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[7], q[4], q[11];
// UNMAPPED c3x [10, 7, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[7], q[4], q[8];
// UNMAPPED c5x [11, 9, 8, 7, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[4], q[10];
// UNMAPPED c4x [11, 10, 7, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[4], q[9];
// UNMAPPED c4x [11, 10, 7, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[4], q[8];
// UNMAPPED c3x [9, 7, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[4], q[11];
// UNMAPPED c3x [9, 7, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[4], q[10];
// UNMAPPED c3x [9, 7, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[4], q[8];
// UNMAPPED c4x [9, 8, 7, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[4], q[11];
// UNMAPPED c4x [11, 9, 7, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[7], q[4], q[8];
// UNMAPPED c4x [10, 9, 7, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[4], q[11];
// UNMAPPED c4x [10, 9, 7, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[4], q[8];
// UNMAPPED c4x [11, 8, 7, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[4], q[10];
// UNMAPPED c5x [11, 10, 8, 7, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[8], q[7], q[4], q[9];
// UNMAPPED c5x [11, 10, 9, 7, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[7], q[4], q[8];
// UNMAPPED c4x [9, 8, 7, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[4], q[11];
// UNMAPPED c4x [11, 8, 7, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[4], q[9];
// UNMAPPED c4x [10, 8, 7, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[8], q[7], q[4], q[9];
// UNMAPPED c4x [9, 8, 7, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[4], q[11];
// UNMAPPED c5x [11, 9, 8, 7, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[4], q[10];
// UNMAPPED c5x [11, 10, 8, 7, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[8], q[7], q[4], q[9];
// UNMAPPED c4x [9, 8, 7, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[4], q[11];
// UNMAPPED c5x [11, 9, 8, 7, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[4], q[10];
ccx q[11], q[4], q[10];
ccx q[11], q[4], q[8];
ccx q[10], q[4], q[11];
ccx q[10], q[4], q[8];
// UNMAPPED c3x [9, 8, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[4], q[11];
// UNMAPPED c4x [11, 9, 8, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[8], q[4], q[10];
// UNMAPPED c3x [11, 10, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[10], q[4], q[9];
// UNMAPPED c3x [11, 10, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[10], q[4], q[8];
ccx q[9], q[4], q[11];
ccx q[9], q[4], q[10];
// UNMAPPED c4x [10, 9, 8, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[4], q[11];
// UNMAPPED c3x [11, 9, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[9], q[4], q[10];
// UNMAPPED c3x [11, 9, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[9], q[4], q[8];
// UNMAPPED c3x [11, 8, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[4], q[10];
// UNMAPPED c4x [11, 10, 8, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[4], q[9];
// UNMAPPED c3x [10, 9, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[9], q[4], q[11];
// UNMAPPED c3x [10, 9, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[9], q[4], q[8];
// UNMAPPED c3x [11, 8, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[4], q[10];
// UNMAPPED c4x [11, 10, 8, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[4], q[9];
// UNMAPPED c4x [11, 10, 9, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[9], q[4], q[8];
ccx q[8], q[4], q[11];
// UNMAPPED c3x [9, 8, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[4], q[11];
// UNMAPPED c3x [11, 8, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[4], q[9];
ccx q[7], q[4], q[11];
// UNMAPPED c3x [11, 7, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[4], q[10];
// UNMAPPED c4x [11, 10, 7, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[4], q[8];
// UNMAPPED c4x [11, 10, 8, 4, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[4], q[7];
// UNMAPPED c3x [9, 8, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[4], q[10];
// UNMAPPED c3x [11, 7, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[4], q[9];
// UNMAPPED c4x [11, 9, 7, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[7], q[4], q[8];
// UNMAPPED c4x [11, 9, 8, 4, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[8], q[4], q[7];
// UNMAPPED c5x [11, 10, 9, 7, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[7], q[4], q[8];
// UNMAPPED c4x [10, 9, 8, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[4], q[11];
// UNMAPPED c4x [10, 9, 8, 4, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[4], q[7];
// UNMAPPED c5x [11, 9, 8, 7, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[4], q[10];
// UNMAPPED c5x [11, 10, 9, 8, 4, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[8], q[4], q[7];
ccx q[7], q[4], q[11];
ccx q[7], q[4], q[10];
ccx q[7], q[4], q[9];
// UNMAPPED c4x [10, 9, 7, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[4], q[11];
// UNMAPPED c3x [11, 7, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[4], q[10];
// UNMAPPED c3x [11, 7, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[4], q[9];
// UNMAPPED c4x [11, 8, 7, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[4], q[10];
// UNMAPPED c3x [10, 7, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[7], q[4], q[11];
// UNMAPPED c3x [10, 7, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[7], q[4], q[8];
// UNMAPPED c5x [11, 9, 8, 7, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[4], q[10];
// UNMAPPED c4x [11, 10, 7, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[4], q[9];
// UNMAPPED c4x [11, 10, 7, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[4], q[8];
// UNMAPPED c3x [9, 7, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[4], q[11];
// UNMAPPED c3x [9, 7, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[4], q[10];
// UNMAPPED c3x [9, 7, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[4], q[8];
// UNMAPPED c4x [9, 8, 7, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[4], q[11];
// UNMAPPED c4x [11, 9, 7, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[7], q[4], q[8];
// UNMAPPED c4x [10, 9, 7, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[4], q[11];
// UNMAPPED c4x [10, 9, 7, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[4], q[8];
// UNMAPPED c4x [11, 8, 7, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[4], q[10];
// UNMAPPED c5x [11, 10, 8, 7, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[8], q[7], q[4], q[9];
// UNMAPPED c5x [11, 10, 9, 7, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[7], q[4], q[8];
// UNMAPPED c4x [9, 8, 7, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[4], q[11];
// UNMAPPED c4x [11, 8, 7, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[4], q[9];
// UNMAPPED c4x [10, 8, 7, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[8], q[7], q[4], q[9];
// UNMAPPED c4x [9, 8, 7, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[4], q[11];
// UNMAPPED c5x [11, 9, 8, 7, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[4], q[10];
// UNMAPPED c5x [11, 10, 8, 7, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[8], q[7], q[4], q[9];
// UNMAPPED c4x [9, 8, 7, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[4], q[11];
// UNMAPPED c5x [11, 9, 8, 7, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[4], q[10];
ccx q[11], q[4], q[10];
ccx q[11], q[4], q[8];
ccx q[10], q[4], q[11];
ccx q[10], q[4], q[8];
// UNMAPPED c3x [9, 8, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[4], q[11];
// UNMAPPED c4x [11, 9, 8, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[8], q[4], q[10];
// UNMAPPED c3x [11, 10, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[10], q[4], q[9];
// UNMAPPED c3x [11, 10, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[10], q[4], q[8];
ccx q[9], q[4], q[11];
ccx q[9], q[4], q[10];
// UNMAPPED c4x [10, 9, 8, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[4], q[11];
// UNMAPPED c3x [11, 9, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[9], q[4], q[10];
// UNMAPPED c3x [11, 9, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[9], q[4], q[8];
// UNMAPPED c3x [11, 8, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[4], q[10];
// UNMAPPED c4x [11, 10, 8, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[4], q[9];
// UNMAPPED c3x [10, 9, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[9], q[4], q[11];
// UNMAPPED c3x [10, 9, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[9], q[4], q[8];
// UNMAPPED c3x [11, 8, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[4], q[10];
// UNMAPPED c4x [11, 10, 8, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[4], q[9];
// UNMAPPED c4x [11, 10, 9, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[9], q[4], q[8];
ccx q[8], q[4], q[11];
// UNMAPPED c3x [9, 8, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[4], q[11];
// UNMAPPED c3x [11, 8, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[4], q[9];
ccx q[7], q[4], q[11];
// UNMAPPED c3x [11, 7, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[4], q[10];
// UNMAPPED c4x [11, 10, 7, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[4], q[8];
// UNMAPPED c4x [11, 10, 8, 4, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[4], q[7];
// UNMAPPED c3x [9, 8, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[4], q[10];
// UNMAPPED c3x [11, 7, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[4], q[9];
// UNMAPPED c4x [11, 9, 7, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[7], q[4], q[8];
// UNMAPPED c4x [11, 9, 8, 4, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[8], q[4], q[7];
// UNMAPPED c5x [11, 10, 9, 7, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[7], q[4], q[8];
// UNMAPPED c4x [10, 9, 8, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[4], q[11];
// UNMAPPED c4x [10, 9, 8, 4, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[4], q[7];
// UNMAPPED c5x [11, 9, 8, 7, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[4], q[10];
// UNMAPPED c5x [11, 10, 9, 8, 4, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[8], q[4], q[7];
ccx q[7], q[4], q[11];
ccx q[7], q[4], q[10];
ccx q[7], q[4], q[9];
// UNMAPPED c4x [10, 9, 7, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[4], q[11];
// UNMAPPED c3x [11, 7, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[4], q[10];
// UNMAPPED c3x [11, 7, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[4], q[9];
// UNMAPPED c4x [11, 8, 7, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[4], q[10];
// UNMAPPED c3x [10, 7, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[7], q[4], q[11];
// UNMAPPED c3x [10, 7, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[7], q[4], q[8];
// UNMAPPED c5x [11, 9, 8, 7, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[4], q[10];
// UNMAPPED c4x [11, 10, 7, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[4], q[9];
// UNMAPPED c4x [11, 10, 7, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[4], q[8];
// UNMAPPED c3x [9, 7, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[4], q[11];
// UNMAPPED c3x [9, 7, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[4], q[10];
// UNMAPPED c3x [9, 7, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[4], q[8];
// UNMAPPED c4x [9, 8, 7, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[4], q[11];
// UNMAPPED c4x [11, 9, 7, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[7], q[4], q[8];
// UNMAPPED c4x [10, 9, 7, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[4], q[11];
// UNMAPPED c4x [10, 9, 7, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[4], q[8];
// UNMAPPED c4x [11, 8, 7, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[4], q[10];
// UNMAPPED c5x [11, 10, 8, 7, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[8], q[7], q[4], q[9];
// UNMAPPED c5x [11, 10, 9, 7, 4, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[7], q[4], q[8];
// UNMAPPED c4x [9, 8, 7, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[4], q[11];
// UNMAPPED c4x [11, 8, 7, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[4], q[9];
// UNMAPPED c4x [10, 8, 7, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[8], q[7], q[4], q[9];
// UNMAPPED c4x [9, 8, 7, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[4], q[11];
// UNMAPPED c5x [11, 9, 8, 7, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[4], q[10];
// UNMAPPED c5x [11, 10, 8, 7, 4, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[8], q[7], q[4], q[9];
// UNMAPPED c4x [9, 8, 7, 4, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[4], q[11];
// UNMAPPED c5x [11, 9, 8, 7, 4, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[4], q[10];
ccx q[11], q[5], q[10];
ccx q[11], q[5], q[8];
ccx q[10], q[5], q[11];
ccx q[10], q[5], q[8];
// UNMAPPED c3x [9, 8, 5, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[5], q[11];
// UNMAPPED c4x [11, 9, 8, 5, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[8], q[5], q[10];
// UNMAPPED c3x [11, 10, 5, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[10], q[5], q[9];
// UNMAPPED c3x [11, 10, 5, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[10], q[5], q[8];
ccx q[9], q[5], q[11];
ccx q[9], q[5], q[10];
// UNMAPPED c4x [10, 9, 8, 5, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[5], q[11];
// UNMAPPED c3x [11, 9, 5, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[9], q[5], q[10];
// UNMAPPED c3x [11, 9, 5, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[9], q[5], q[8];
// UNMAPPED c3x [11, 8, 5, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[5], q[10];
// UNMAPPED c4x [11, 10, 8, 5, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[5], q[9];
// UNMAPPED c3x [10, 9, 5, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[9], q[5], q[11];
// UNMAPPED c3x [10, 9, 5, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[9], q[5], q[8];
// UNMAPPED c3x [11, 8, 5, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[5], q[10];
// UNMAPPED c4x [11, 10, 8, 5, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[5], q[9];
// UNMAPPED c4x [11, 10, 9, 5, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[9], q[5], q[8];
ccx q[8], q[5], q[11];
// UNMAPPED c3x [9, 8, 5, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[5], q[11];
// UNMAPPED c3x [11, 8, 5, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[5], q[9];
ccx q[7], q[5], q[11];
// UNMAPPED c3x [11, 7, 5, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[5], q[10];
// UNMAPPED c4x [11, 10, 7, 5, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[5], q[8];
// UNMAPPED c4x [11, 10, 8, 5, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[5], q[7];
// UNMAPPED c3x [9, 8, 5, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[5], q[10];
// UNMAPPED c3x [11, 7, 5, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[5], q[9];
// UNMAPPED c4x [11, 9, 7, 5, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[7], q[5], q[8];
// UNMAPPED c4x [11, 9, 8, 5, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[8], q[5], q[7];
// UNMAPPED c5x [11, 10, 9, 7, 5, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[7], q[5], q[8];
// UNMAPPED c4x [10, 9, 8, 5, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[5], q[11];
// UNMAPPED c4x [10, 9, 8, 5, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[5], q[7];
// UNMAPPED c5x [11, 9, 8, 7, 5, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[5], q[10];
// UNMAPPED c5x [11, 10, 9, 8, 5, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[8], q[5], q[7];
ccx q[7], q[5], q[11];
ccx q[7], q[5], q[10];
ccx q[7], q[5], q[9];
// UNMAPPED c4x [10, 9, 7, 5, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[5], q[11];
// UNMAPPED c3x [11, 7, 5, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[5], q[10];
// UNMAPPED c3x [11, 7, 5, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[5], q[9];
// UNMAPPED c4x [11, 8, 7, 5, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[5], q[10];
// UNMAPPED c3x [10, 7, 5, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[7], q[5], q[11];
// UNMAPPED c3x [10, 7, 5, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[7], q[5], q[8];
// UNMAPPED c5x [11, 9, 8, 7, 5, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[5], q[10];
// UNMAPPED c4x [11, 10, 7, 5, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[5], q[9];
// UNMAPPED c4x [11, 10, 7, 5, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[5], q[8];
// UNMAPPED c3x [9, 7, 5, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[5], q[11];
// UNMAPPED c3x [9, 7, 5, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[5], q[10];
// UNMAPPED c3x [9, 7, 5, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[5], q[8];
// UNMAPPED c4x [9, 8, 7, 5, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[5], q[11];
// UNMAPPED c4x [11, 9, 7, 5, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[7], q[5], q[8];
// UNMAPPED c4x [10, 9, 7, 5, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[5], q[11];
// UNMAPPED c4x [10, 9, 7, 5, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[5], q[8];
// UNMAPPED c4x [11, 8, 7, 5, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[5], q[10];
// UNMAPPED c5x [11, 10, 8, 7, 5, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[8], q[7], q[5], q[9];
// UNMAPPED c5x [11, 10, 9, 7, 5, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[7], q[5], q[8];
// UNMAPPED c4x [9, 8, 7, 5, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[5], q[11];
// UNMAPPED c4x [11, 8, 7, 5, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[5], q[9];
// UNMAPPED c4x [10, 8, 7, 5, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[8], q[7], q[5], q[9];
// UNMAPPED c4x [9, 8, 7, 5, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[5], q[11];
// UNMAPPED c5x [11, 9, 8, 7, 5, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[5], q[10];
// UNMAPPED c5x [11, 10, 8, 7, 5, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[8], q[7], q[5], q[9];
// UNMAPPED c4x [9, 8, 7, 5, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[5], q[11];
// UNMAPPED c5x [11, 9, 8, 7, 5, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[5], q[10];
ccx q[11], q[5], q[10];
ccx q[11], q[5], q[8];
ccx q[10], q[5], q[11];
ccx q[10], q[5], q[8];
// UNMAPPED c3x [9, 8, 5, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[5], q[11];
// UNMAPPED c4x [11, 9, 8, 5, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[8], q[5], q[10];
// UNMAPPED c3x [11, 10, 5, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[10], q[5], q[9];
// UNMAPPED c3x [11, 10, 5, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[10], q[5], q[8];
ccx q[9], q[5], q[11];
ccx q[9], q[5], q[10];
// UNMAPPED c4x [10, 9, 8, 5, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[5], q[11];
// UNMAPPED c3x [11, 9, 5, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[9], q[5], q[10];
// UNMAPPED c3x [11, 9, 5, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[9], q[5], q[8];
// UNMAPPED c3x [11, 8, 5, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[5], q[10];
// UNMAPPED c4x [11, 10, 8, 5, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[5], q[9];
// UNMAPPED c3x [10, 9, 5, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[9], q[5], q[11];
// UNMAPPED c3x [10, 9, 5, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[9], q[5], q[8];
// UNMAPPED c3x [11, 8, 5, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[5], q[10];
// UNMAPPED c4x [11, 10, 8, 5, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[5], q[9];
// UNMAPPED c4x [11, 10, 9, 5, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[9], q[5], q[8];
ccx q[8], q[5], q[11];
// UNMAPPED c3x [9, 8, 5, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[5], q[11];
// UNMAPPED c3x [11, 8, 5, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[5], q[9];
ccx q[7], q[5], q[11];
// UNMAPPED c3x [11, 7, 5, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[5], q[10];
// UNMAPPED c4x [11, 10, 7, 5, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[5], q[8];
// UNMAPPED c4x [11, 10, 8, 5, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[5], q[7];
// UNMAPPED c3x [9, 8, 5, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[5], q[10];
// UNMAPPED c3x [11, 7, 5, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[5], q[9];
// UNMAPPED c4x [11, 9, 7, 5, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[7], q[5], q[8];
// UNMAPPED c4x [11, 9, 8, 5, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[8], q[5], q[7];
// UNMAPPED c5x [11, 10, 9, 7, 5, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[7], q[5], q[8];
// UNMAPPED c4x [10, 9, 8, 5, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[5], q[11];
// UNMAPPED c4x [10, 9, 8, 5, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[5], q[7];
// UNMAPPED c5x [11, 9, 8, 7, 5, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[5], q[10];
// UNMAPPED c5x [11, 10, 9, 8, 5, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[8], q[5], q[7];
ccx q[7], q[5], q[11];
ccx q[7], q[5], q[10];
ccx q[7], q[5], q[9];
// UNMAPPED c4x [10, 9, 7, 5, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[5], q[11];
// UNMAPPED c3x [11, 7, 5, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[5], q[10];
// UNMAPPED c3x [11, 7, 5, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[5], q[9];
// UNMAPPED c4x [11, 8, 7, 5, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[5], q[10];
// UNMAPPED c3x [10, 7, 5, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[7], q[5], q[11];
// UNMAPPED c3x [10, 7, 5, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[7], q[5], q[8];
// UNMAPPED c5x [11, 9, 8, 7, 5, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[5], q[10];
// UNMAPPED c4x [11, 10, 7, 5, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[5], q[9];
// UNMAPPED c4x [11, 10, 7, 5, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[5], q[8];
// UNMAPPED c3x [9, 7, 5, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[5], q[11];
// UNMAPPED c3x [9, 7, 5, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[5], q[10];
// UNMAPPED c3x [9, 7, 5, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[5], q[8];
// UNMAPPED c4x [9, 8, 7, 5, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[5], q[11];
// UNMAPPED c4x [11, 9, 7, 5, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[7], q[5], q[8];
// UNMAPPED c4x [10, 9, 7, 5, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[5], q[11];
// UNMAPPED c4x [10, 9, 7, 5, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[5], q[8];
// UNMAPPED c4x [11, 8, 7, 5, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[5], q[10];
// UNMAPPED c5x [11, 10, 8, 7, 5, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[8], q[7], q[5], q[9];
// UNMAPPED c5x [11, 10, 9, 7, 5, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[7], q[5], q[8];
// UNMAPPED c4x [9, 8, 7, 5, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[5], q[11];
// UNMAPPED c4x [11, 8, 7, 5, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[5], q[9];
// UNMAPPED c4x [10, 8, 7, 5, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[8], q[7], q[5], q[9];
// UNMAPPED c4x [9, 8, 7, 5, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[5], q[11];
// UNMAPPED c5x [11, 9, 8, 7, 5, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[5], q[10];
// UNMAPPED c5x [11, 10, 8, 7, 5, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[8], q[7], q[5], q[9];
// UNMAPPED c4x [9, 8, 7, 5, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[5], q[11];
// UNMAPPED c5x [11, 9, 8, 7, 5, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[5], q[10];
ccx q[11], q[6], q[10];
ccx q[11], q[6], q[8];
ccx q[10], q[6], q[11];
ccx q[10], q[6], q[8];
// UNMAPPED c3x [9, 8, 6, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[6], q[11];
// UNMAPPED c4x [11, 9, 8, 6, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[8], q[6], q[10];
// UNMAPPED c3x [11, 10, 6, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[10], q[6], q[9];
// UNMAPPED c3x [11, 10, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[10], q[6], q[8];
ccx q[9], q[6], q[11];
ccx q[9], q[6], q[10];
// UNMAPPED c4x [10, 9, 8, 6, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[6], q[11];
// UNMAPPED c3x [11, 9, 6, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[9], q[6], q[10];
// UNMAPPED c3x [11, 9, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[9], q[6], q[8];
// UNMAPPED c3x [11, 8, 6, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[6], q[10];
// UNMAPPED c4x [11, 10, 8, 6, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[6], q[9];
// UNMAPPED c3x [10, 9, 6, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[9], q[6], q[11];
// UNMAPPED c3x [10, 9, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[9], q[6], q[8];
// UNMAPPED c3x [11, 8, 6, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[6], q[10];
// UNMAPPED c4x [11, 10, 8, 6, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[6], q[9];
// UNMAPPED c4x [11, 10, 9, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[9], q[6], q[8];
ccx q[8], q[6], q[11];
// UNMAPPED c3x [9, 8, 6, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[6], q[11];
// UNMAPPED c3x [11, 8, 6, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[8], q[6], q[9];
ccx q[7], q[6], q[11];
// UNMAPPED c3x [11, 7, 6, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[6], q[10];
// UNMAPPED c4x [11, 10, 7, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[6], q[8];
// UNMAPPED c4x [11, 10, 8, 6, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[8], q[6], q[7];
// UNMAPPED c3x [9, 8, 6, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[8], q[6], q[10];
// UNMAPPED c3x [11, 7, 6, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[6], q[9];
// UNMAPPED c4x [11, 9, 7, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[7], q[6], q[8];
// UNMAPPED c4x [11, 9, 8, 6, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[8], q[6], q[7];
// UNMAPPED c5x [11, 10, 9, 7, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[7], q[6], q[8];
// UNMAPPED c4x [10, 9, 8, 6, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[6], q[11];
// UNMAPPED c4x [10, 9, 8, 6, 7]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[8], q[6], q[7];
// UNMAPPED c5x [11, 9, 8, 7, 6, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[6], q[10];
// UNMAPPED c5x [11, 10, 9, 8, 6, 7]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[8], q[6], q[7];
ccx q[7], q[6], q[11];
ccx q[7], q[6], q[10];
ccx q[7], q[6], q[9];
// UNMAPPED c4x [10, 9, 7, 6, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[6], q[11];
// UNMAPPED c3x [11, 7, 6, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[6], q[10];
// UNMAPPED c3x [11, 7, 6, 9]  (QASM3 비표준 — opaque)
qpgf_c3x q[11], q[7], q[6], q[9];
// UNMAPPED c4x [11, 8, 7, 6, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[6], q[10];
// UNMAPPED c3x [10, 7, 6, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[7], q[6], q[11];
// UNMAPPED c3x [10, 7, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[10], q[7], q[6], q[8];
// UNMAPPED c5x [11, 9, 8, 7, 6, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[6], q[10];
// UNMAPPED c4x [11, 10, 7, 6, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[6], q[9];
// UNMAPPED c4x [11, 10, 7, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[10], q[7], q[6], q[8];
// UNMAPPED c3x [9, 7, 6, 11]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[6], q[11];
// UNMAPPED c3x [9, 7, 6, 10]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[6], q[10];
// UNMAPPED c3x [9, 7, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[9], q[7], q[6], q[8];
// UNMAPPED c4x [9, 8, 7, 6, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[6], q[11];
// UNMAPPED c4x [11, 9, 7, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[9], q[7], q[6], q[8];
// UNMAPPED c4x [10, 9, 7, 6, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[6], q[11];
// UNMAPPED c4x [10, 9, 7, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[9], q[7], q[6], q[8];
// UNMAPPED c4x [11, 8, 7, 6, 10]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[6], q[10];
// UNMAPPED c5x [11, 10, 8, 7, 6, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[8], q[7], q[6], q[9];
// UNMAPPED c5x [11, 10, 9, 7, 6, 8]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[9], q[7], q[6], q[8];
// UNMAPPED c4x [9, 8, 7, 6, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[6], q[11];
// UNMAPPED c4x [11, 8, 7, 6, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[11], q[8], q[7], q[6], q[9];
// UNMAPPED c4x [10, 8, 7, 6, 9]  (QASM3 비표준 — opaque)
qpgf_c4x q[10], q[8], q[7], q[6], q[9];
// UNMAPPED c4x [9, 8, 7, 6, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[6], q[11];
// UNMAPPED c5x [11, 9, 8, 7, 6, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[6], q[10];
// UNMAPPED c5x [11, 10, 8, 7, 6, 9]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[10], q[8], q[7], q[6], q[9];
// UNMAPPED c4x [9, 8, 7, 6, 11]  (QASM3 비표준 — opaque)
qpgf_c4x q[9], q[8], q[7], q[6], q[11];
// UNMAPPED c5x [11, 9, 8, 7, 6, 10]  (QASM3 비표준 — opaque)
qpgf_c5x q[11], q[9], q[8], q[7], q[6], q[10];
swap q[0], q[6];
swap q[1], q[5];
swap q[2], q[4];
h q[6];
cp(-1.57079632679) q[6], q[5];
h q[5];
cp(-0.785398163397) q[6], q[4];
cp(-1.57079632679) q[5], q[4];
h q[4];
cp(-0.392699081699) q[6], q[3];
cp(-0.785398163397) q[5], q[3];
cp(-1.57079632679) q[4], q[3];
h q[3];
cp(-0.196349540849) q[6], q[2];
cp(-0.392699081699) q[5], q[2];
cp(-0.785398163397) q[4], q[2];
cp(-1.57079632679) q[3], q[2];
h q[2];
cp(-0.0981747704247) q[6], q[1];
cp(-0.196349540849) q[5], q[1];
cp(-0.392699081699) q[4], q[1];
cp(-0.785398163397) q[3], q[1];
cp(-1.57079632679) q[2], q[1];
h q[1];
cp(-0.0490873852123) q[6], q[0];
cp(-0.0981747704247) q[5], q[0];
cp(-0.196349540849) q[4], q[0];
cp(-0.392699081699) q[3], q[0];
cp(-0.785398163397) q[2], q[0];
cp(-1.57079632679) q[1], q[0];
h q[0];
