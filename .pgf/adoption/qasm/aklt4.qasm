OPENQASM 3.0;
include "stdgates.inc";
qubit[9] q;

gate qpgf_ry_ak13 q0 { }  // opaque: ry_ak13 (1q), golden in registry/modules/ry_ak13.sealed.json
gate qpgf_ry_ak13_dag q0 { }  // opaque: ry_ak13_dag (1q), golden in registry/modules/ry_ak13_dag.sealed.json
gate qpgf_ry_ak41_dag q0 { }  // opaque: ry_ak41_dag (1q), golden in registry/modules/ry_ak41_dag.sealed.json
gate qpgf_ry_ak7 q0 { }  // opaque: ry_ak7 (1q), golden in registry/modules/ry_ak7.sealed.json
gate qpgf_ry_ak7_dag q0 { }  // opaque: ry_ak7_dag (1q), golden in registry/modules/ry_ak7_dag.sealed.json
gate qpgf_ry_negpi2 q0 { }  // opaque: ry_negpi2 (1q), golden in registry/modules/ry_negpi2.sealed.json
gate qpgf_ry_negpi4 q0 { }  // opaque: ry_negpi4 (1q), golden in registry/modules/ry_negpi4.sealed.json
gate qpgf_ry_pi2 q0 { }  // opaque: ry_pi2 (1q), golden in registry/modules/ry_pi2.sealed.json
gate qpgf_ry_pi4 q0 { }  // opaque: ry_pi4 (1q), golden in registry/modules/ry_pi4.sealed.json

z q[8];
x q[8];
z q[8];
x q[8];
// UNMAPPED ry_ak41_dag [1]  (QASM3 비표준 — opaque)
qpgf_ry_ak41_dag q[1];
// UNMAPPED ry_ak41_dag [1]  (QASM3 비표준 — opaque)
qpgf_ry_ak41_dag q[1];
x q[1];
cx q[1], q[8];
x q[1];
cx q[1], q[0];
x q[1];
// UNMAPPED ry_negpi4 [1]  (QASM3 비표준 — opaque)
qpgf_ry_negpi4 q[1];
cz q[0], q[1];
// UNMAPPED ry_pi4 [1]  (QASM3 비표준 — opaque)
qpgf_ry_pi4 q[1];
x q[1];
cx q[1], q[0];
x q[8];
cx q[8], q[3];
// UNMAPPED ry_ak13 [3]  (QASM3 비표준 — opaque)
qpgf_ry_ak13 q[3];
cx q[8], q[3];
// UNMAPPED ry_ak13_dag [3]  (QASM3 비표준 — opaque)
qpgf_ry_ak13_dag q[3];
x q[8];
cx q[8], q[3];
cx q[8], q[2];
// UNMAPPED ry_ak7 [2]  (QASM3 비표준 — opaque)
qpgf_ry_ak7 q[2];
cx q[8], q[2];
// UNMAPPED ry_ak7_dag [2]  (QASM3 비표준 — opaque)
qpgf_ry_ak7_dag q[2];
x q[3];
cx q[3], q[8];
x q[3];
cx q[2], q[8];
cx q[3], q[2];
x q[3];
// UNMAPPED ry_negpi4 [3]  (QASM3 비표준 — opaque)
qpgf_ry_negpi4 q[3];
cz q[2], q[3];
// UNMAPPED ry_pi4 [3]  (QASM3 비표준 — opaque)
qpgf_ry_pi4 q[3];
x q[3];
cx q[3], q[2];
x q[8];
cx q[8], q[5];
ry(-1.10714871779) q[5];
// UNMAPPED ry_pi2 [5]  (QASM3 비표준 — opaque)
qpgf_ry_pi2 q[5];
cx q[8], q[5];
// UNMAPPED ry_negpi2 [5]  (QASM3 비표준 — opaque)
qpgf_ry_negpi2 q[5];
ry(1.10714871779) q[5];
x q[8];
cx q[8], q[5];
cx q[8], q[4];
// UNMAPPED ry_pi4 [4]  (QASM3 비표준 — opaque)
qpgf_ry_pi4 q[4];
cx q[8], q[4];
// UNMAPPED ry_negpi4 [4]  (QASM3 비표준 — opaque)
qpgf_ry_negpi4 q[4];
x q[5];
cx q[5], q[8];
x q[5];
cx q[4], q[8];
cx q[5], q[4];
x q[5];
// UNMAPPED ry_negpi4 [5]  (QASM3 비표준 — opaque)
qpgf_ry_negpi4 q[5];
cz q[4], q[5];
// UNMAPPED ry_pi4 [5]  (QASM3 비표준 — opaque)
qpgf_ry_pi4 q[5];
x q[5];
cx q[5], q[4];
x q[8];
cx q[8], q[7];
x q[8];
cx q[8], q[6];
cx q[8], q[7];
cx q[6], q[8];
cx q[7], q[6];
x q[7];
// UNMAPPED ry_negpi4 [7]  (QASM3 비표준 — opaque)
qpgf_ry_negpi4 q[7];
cz q[6], q[7];
// UNMAPPED ry_pi4 [7]  (QASM3 비표준 — opaque)
qpgf_ry_pi4 q[7];
x q[7];
cx q[7], q[6];
