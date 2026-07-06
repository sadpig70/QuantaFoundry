OPENQASM 3.0;
include "stdgates.inc";
qubit[4] q;

gate qpgf_c3x q0, q1, q2, q3 { }  // opaque: c3x (4q), golden in registry/modules/c3x.sealed.json

x q[0];
x q[2];
// UNMAPPED c3x [0, 1, 2, 3]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[2], q[3];
x q[2];
x q[3];
// UNMAPPED c3x [0, 1, 3, 2]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[3], q[2];
x q[3];
x q[0];
x q[1];
x q[2];
// UNMAPPED c3x [0, 1, 2, 3]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[2], q[3];
x q[2];
x q[3];
// UNMAPPED c3x [0, 1, 3, 2]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[3], q[2];
x q[3];
x q[1];
x q[1];
x q[2];
// UNMAPPED c3x [0, 1, 2, 3]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[2], q[3];
x q[2];
x q[3];
// UNMAPPED c3x [0, 1, 3, 2]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[1], q[3], q[2];
x q[3];
x q[1];
