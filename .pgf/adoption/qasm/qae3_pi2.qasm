OPENQASM 3.0;
include "stdgates.inc";
qubit[4] q;

gate qpgf_ry_negpi2 q0 { }  // opaque: ry_negpi2 (1q), golden in registry/modules/ry_negpi2.sealed.json
gate qpgf_ry_pi2 q0 { }  // opaque: ry_pi2 (1q), golden in registry/modules/ry_pi2.sealed.json

// UNMAPPED ry_pi2 [3]  (QASM3 비표준 — opaque)
qpgf_ry_pi2 q[3];
h q[0];
h q[1];
h q[2];
z q[1];
cx q[2], q[3];
// UNMAPPED ry_negpi2 [3]  (QASM3 비표준 — opaque)
qpgf_ry_negpi2 q[3];
cx q[2], q[3];
// UNMAPPED ry_pi2 [3]  (QASM3 비표준 — opaque)
qpgf_ry_pi2 q[3];
swap q[0], q[2];
h q[2];
cp(-1.57079632679) q[2], q[1];
h q[1];
cp(-0.785398163397) q[2], q[0];
cp(-1.57079632679) q[1], q[0];
h q[0];
