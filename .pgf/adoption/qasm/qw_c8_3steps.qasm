OPENQASM 3.0;
include "stdgates.inc";
qubit[4] q;

gate qpgf_c3x q0, q1, q2, q3 { }  // opaque: c3x (4q), golden in registry/modules/c3x.sealed.json

h q[0];
x q[0];
// UNMAPPED c3x [0, 2, 3, 1]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[2], q[3], q[1];
ccx q[0], q[3], q[2];
cx q[0], q[3];
x q[0];
cx q[0], q[3];
ccx q[0], q[3], q[2];
// UNMAPPED c3x [0, 2, 3, 1]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[2], q[3], q[1];
h q[0];
x q[0];
// UNMAPPED c3x [0, 2, 3, 1]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[2], q[3], q[1];
ccx q[0], q[3], q[2];
cx q[0], q[3];
x q[0];
cx q[0], q[3];
ccx q[0], q[3], q[2];
// UNMAPPED c3x [0, 2, 3, 1]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[2], q[3], q[1];
h q[0];
x q[0];
// UNMAPPED c3x [0, 2, 3, 1]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[2], q[3], q[1];
ccx q[0], q[3], q[2];
cx q[0], q[3];
x q[0];
cx q[0], q[3];
ccx q[0], q[3], q[2];
// UNMAPPED c3x [0, 2, 3, 1]  (QASM3 비표준 — opaque)
qpgf_c3x q[0], q[2], q[3], q[1];
