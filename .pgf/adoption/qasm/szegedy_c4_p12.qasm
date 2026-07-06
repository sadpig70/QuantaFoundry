OPENQASM 3.0;
include "stdgates.inc";
qubit[4] q;

gate qpgf_qft2 q0, q1 { }  // opaque: qft2 (2q), golden in registry/modules/qft2.sealed.json

x q[0];
x q[1];
// UNMAPPED qft2 [2, 3]  (QASM3 비표준 — opaque)
qpgf_qft2 q[2], q[3];
cp(1.57079632679) q[1], q[3];
cz q[1], q[2];
cz q[0], q[3];
swap q[2], q[3];
h q[3];
cp(-1.57079632679) q[3], q[2];
h q[2];
cx q[3], q[2];
x q[3];
x q[0];
x q[1];
x q[3];
h q[2];
x q[2];
x q[3];
cz q[2], q[3];
x q[2];
x q[3];
h q[2];
x q[3];
// UNMAPPED qft2 [2, 3]  (QASM3 비표준 — opaque)
qpgf_qft2 q[2], q[3];
cp(1.57079632679) q[1], q[3];
cz q[1], q[2];
cz q[0], q[3];
swap q[2], q[3];
h q[3];
cp(-1.57079632679) q[3], q[2];
h q[2];
swap q[0], q[2];
swap q[1], q[3];
x q[0];
x q[1];
// UNMAPPED qft2 [2, 3]  (QASM3 비표준 — opaque)
qpgf_qft2 q[2], q[3];
cp(1.57079632679) q[1], q[3];
cz q[1], q[2];
cz q[0], q[3];
swap q[2], q[3];
h q[3];
cp(-1.57079632679) q[3], q[2];
h q[2];
cx q[3], q[2];
x q[3];
x q[0];
x q[1];
x q[3];
h q[2];
x q[2];
x q[3];
cz q[2], q[3];
x q[2];
x q[3];
h q[2];
x q[3];
// UNMAPPED qft2 [2, 3]  (QASM3 비표준 — opaque)
qpgf_qft2 q[2], q[3];
cp(1.57079632679) q[1], q[3];
cz q[1], q[2];
cz q[0], q[3];
swap q[2], q[3];
h q[3];
cp(-1.57079632679) q[3], q[2];
h q[2];
swap q[0], q[2];
swap q[1], q[3];
