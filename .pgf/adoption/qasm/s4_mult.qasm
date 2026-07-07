OPENQASM 3.0;
include "stdgates.inc";
qubit[10] q;

gate qpgf_c3x q0, q1, q2, q3 { }  // opaque: c3x (4q), golden in registry/modules/c3x.sealed.json

cx q[4], q[9];
cswap q[4], q[7], q[8];
x q[2];
x q[7];
// UNMAPPED c3x [2, 3, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[2], q[3], q[7], q[8];
x q[7];
x q[8];
// UNMAPPED c3x [2, 3, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c3x q[2], q[3], q[8], q[7];
x q[8];
x q[2];
x q[3];
x q[8];
// UNMAPPED c3x [2, 3, 8, 7]  (QASM3 비표준 — opaque)
qpgf_c3x q[2], q[3], q[8], q[7];
x q[8];
x q[7];
// UNMAPPED c3x [2, 3, 7, 8]  (QASM3 비표준 — opaque)
qpgf_c3x q[2], q[3], q[7], q[8];
x q[7];
x q[3];
cswap q[4], q[5], q[6];
x q[2];
// UNMAPPED c3x [2, 3, 5, 6]  (QASM3 비표준 — opaque)
qpgf_c3x q[2], q[3], q[5], q[6];
// UNMAPPED c3x [2, 3, 6, 5]  (QASM3 비표준 — opaque)
qpgf_c3x q[2], q[3], q[6], q[5];
// UNMAPPED c3x [2, 3, 5, 6]  (QASM3 비표준 — opaque)
qpgf_c3x q[2], q[3], q[5], q[6];
// UNMAPPED c3x [2, 3, 6, 5]  (QASM3 비표준 — opaque)
qpgf_c3x q[2], q[3], q[6], q[5];
x q[2];
x q[3];
// UNMAPPED c3x [2, 3, 6, 5]  (QASM3 비표준 — opaque)
qpgf_c3x q[2], q[3], q[6], q[5];
// UNMAPPED c3x [2, 3, 5, 6]  (QASM3 비표준 — opaque)
qpgf_c3x q[2], q[3], q[5], q[6];
// UNMAPPED c3x [2, 3, 6, 5]  (QASM3 비표준 — opaque)
qpgf_c3x q[2], q[3], q[6], q[5];
// UNMAPPED c3x [2, 3, 5, 6]  (QASM3 비표준 — opaque)
qpgf_c3x q[2], q[3], q[5], q[6];
x q[3];
cx q[0], q[5];
cx q[1], q[6];
