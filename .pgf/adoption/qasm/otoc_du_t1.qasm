OPENQASM 3.0;
include "stdgates.inc";
qubit[6] q;

gate qpgf_iswap q0, q1 { }  // opaque: iswap (2q), golden in registry/modules/iswap.sealed.json
gate qpgf_sdg_gate q0 { }  // opaque: sdg_gate (1q), golden in registry/modules/sdg_gate.sealed.json

x q[0];
z q[0];
z q[1];
// UNMAPPED iswap [0, 1]  (QASM3 비표준 — opaque)
qpgf_iswap q[0], q[1];
cx q[0], q[1];
t q[1];
cx q[0], q[1];
z q[2];
z q[3];
// UNMAPPED iswap [2, 3]  (QASM3 비표준 — opaque)
qpgf_iswap q[2], q[3];
cx q[2], q[3];
t q[3];
cx q[2], q[3];
z q[4];
z q[5];
// UNMAPPED iswap [4, 5]  (QASM3 비표준 — opaque)
qpgf_iswap q[4], q[5];
cx q[4], q[5];
t q[5];
cx q[4], q[5];
z q[1];
z q[2];
// UNMAPPED iswap [1, 2]  (QASM3 비표준 — opaque)
qpgf_iswap q[1], q[2];
cx q[1], q[2];
t q[2];
cx q[1], q[2];
z q[3];
z q[4];
// UNMAPPED iswap [3, 4]  (QASM3 비표준 — opaque)
qpgf_iswap q[3], q[4];
cx q[3], q[4];
t q[4];
cx q[3], q[4];
z q[5];
z q[0];
// UNMAPPED iswap [5, 0]  (QASM3 비표준 — opaque)
qpgf_iswap q[5], q[0];
cx q[5], q[0];
t q[0];
cx q[5], q[0];
x q[1];
cx q[5], q[0];
t q[0];
// UNMAPPED sdg_gate [0]  (QASM3 비표준 — opaque)
qpgf_sdg_gate q[0];
cx q[5], q[0];
// UNMAPPED iswap [5, 0]  (QASM3 비표준 — opaque)
qpgf_iswap q[5], q[0];
// UNMAPPED iswap [5, 0]  (QASM3 비표준 — opaque)
qpgf_iswap q[5], q[0];
// UNMAPPED iswap [5, 0]  (QASM3 비표준 — opaque)
qpgf_iswap q[5], q[0];
z q[5];
z q[0];
cx q[3], q[4];
t q[4];
// UNMAPPED sdg_gate [4]  (QASM3 비표준 — opaque)
qpgf_sdg_gate q[4];
cx q[3], q[4];
// UNMAPPED iswap [3, 4]  (QASM3 비표준 — opaque)
qpgf_iswap q[3], q[4];
// UNMAPPED iswap [3, 4]  (QASM3 비표준 — opaque)
qpgf_iswap q[3], q[4];
// UNMAPPED iswap [3, 4]  (QASM3 비표준 — opaque)
qpgf_iswap q[3], q[4];
z q[3];
z q[4];
cx q[1], q[2];
t q[2];
// UNMAPPED sdg_gate [2]  (QASM3 비표준 — opaque)
qpgf_sdg_gate q[2];
cx q[1], q[2];
// UNMAPPED iswap [1, 2]  (QASM3 비표준 — opaque)
qpgf_iswap q[1], q[2];
// UNMAPPED iswap [1, 2]  (QASM3 비표준 — opaque)
qpgf_iswap q[1], q[2];
// UNMAPPED iswap [1, 2]  (QASM3 비표준 — opaque)
qpgf_iswap q[1], q[2];
z q[1];
z q[2];
cx q[4], q[5];
t q[5];
// UNMAPPED sdg_gate [5]  (QASM3 비표준 — opaque)
qpgf_sdg_gate q[5];
cx q[4], q[5];
// UNMAPPED iswap [4, 5]  (QASM3 비표준 — opaque)
qpgf_iswap q[4], q[5];
// UNMAPPED iswap [4, 5]  (QASM3 비표준 — opaque)
qpgf_iswap q[4], q[5];
// UNMAPPED iswap [4, 5]  (QASM3 비표준 — opaque)
qpgf_iswap q[4], q[5];
z q[4];
z q[5];
cx q[2], q[3];
t q[3];
// UNMAPPED sdg_gate [3]  (QASM3 비표준 — opaque)
qpgf_sdg_gate q[3];
cx q[2], q[3];
// UNMAPPED iswap [2, 3]  (QASM3 비표준 — opaque)
qpgf_iswap q[2], q[3];
// UNMAPPED iswap [2, 3]  (QASM3 비표준 — opaque)
qpgf_iswap q[2], q[3];
// UNMAPPED iswap [2, 3]  (QASM3 비표준 — opaque)
qpgf_iswap q[2], q[3];
z q[2];
z q[3];
cx q[0], q[1];
t q[1];
// UNMAPPED sdg_gate [1]  (QASM3 비표준 — opaque)
qpgf_sdg_gate q[1];
cx q[0], q[1];
// UNMAPPED iswap [0, 1]  (QASM3 비표준 — opaque)
qpgf_iswap q[0], q[1];
// UNMAPPED iswap [0, 1]  (QASM3 비표준 — opaque)
qpgf_iswap q[0], q[1];
// UNMAPPED iswap [0, 1]  (QASM3 비표준 — opaque)
qpgf_iswap q[0], q[1];
z q[0];
z q[1];
x q[0];
z q[0];
z q[1];
// UNMAPPED iswap [0, 1]  (QASM3 비표준 — opaque)
qpgf_iswap q[0], q[1];
cx q[0], q[1];
t q[1];
cx q[0], q[1];
z q[2];
z q[3];
// UNMAPPED iswap [2, 3]  (QASM3 비표준 — opaque)
qpgf_iswap q[2], q[3];
cx q[2], q[3];
t q[3];
cx q[2], q[3];
z q[4];
z q[5];
// UNMAPPED iswap [4, 5]  (QASM3 비표준 — opaque)
qpgf_iswap q[4], q[5];
cx q[4], q[5];
t q[5];
cx q[4], q[5];
z q[1];
z q[2];
// UNMAPPED iswap [1, 2]  (QASM3 비표준 — opaque)
qpgf_iswap q[1], q[2];
cx q[1], q[2];
t q[2];
cx q[1], q[2];
z q[3];
z q[4];
// UNMAPPED iswap [3, 4]  (QASM3 비표준 — opaque)
qpgf_iswap q[3], q[4];
cx q[3], q[4];
t q[4];
cx q[3], q[4];
z q[5];
z q[0];
// UNMAPPED iswap [5, 0]  (QASM3 비표준 — opaque)
qpgf_iswap q[5], q[0];
cx q[5], q[0];
t q[0];
cx q[5], q[0];
x q[1];
cx q[5], q[0];
t q[0];
// UNMAPPED sdg_gate [0]  (QASM3 비표준 — opaque)
qpgf_sdg_gate q[0];
cx q[5], q[0];
// UNMAPPED iswap [5, 0]  (QASM3 비표준 — opaque)
qpgf_iswap q[5], q[0];
// UNMAPPED iswap [5, 0]  (QASM3 비표준 — opaque)
qpgf_iswap q[5], q[0];
// UNMAPPED iswap [5, 0]  (QASM3 비표준 — opaque)
qpgf_iswap q[5], q[0];
z q[5];
z q[0];
cx q[3], q[4];
t q[4];
// UNMAPPED sdg_gate [4]  (QASM3 비표준 — opaque)
qpgf_sdg_gate q[4];
cx q[3], q[4];
// UNMAPPED iswap [3, 4]  (QASM3 비표준 — opaque)
qpgf_iswap q[3], q[4];
// UNMAPPED iswap [3, 4]  (QASM3 비표준 — opaque)
qpgf_iswap q[3], q[4];
// UNMAPPED iswap [3, 4]  (QASM3 비표준 — opaque)
qpgf_iswap q[3], q[4];
z q[3];
z q[4];
cx q[1], q[2];
t q[2];
// UNMAPPED sdg_gate [2]  (QASM3 비표준 — opaque)
qpgf_sdg_gate q[2];
cx q[1], q[2];
// UNMAPPED iswap [1, 2]  (QASM3 비표준 — opaque)
qpgf_iswap q[1], q[2];
// UNMAPPED iswap [1, 2]  (QASM3 비표준 — opaque)
qpgf_iswap q[1], q[2];
// UNMAPPED iswap [1, 2]  (QASM3 비표준 — opaque)
qpgf_iswap q[1], q[2];
z q[1];
z q[2];
cx q[4], q[5];
t q[5];
// UNMAPPED sdg_gate [5]  (QASM3 비표준 — opaque)
qpgf_sdg_gate q[5];
cx q[4], q[5];
// UNMAPPED iswap [4, 5]  (QASM3 비표준 — opaque)
qpgf_iswap q[4], q[5];
// UNMAPPED iswap [4, 5]  (QASM3 비표준 — opaque)
qpgf_iswap q[4], q[5];
// UNMAPPED iswap [4, 5]  (QASM3 비표준 — opaque)
qpgf_iswap q[4], q[5];
z q[4];
z q[5];
cx q[2], q[3];
t q[3];
// UNMAPPED sdg_gate [3]  (QASM3 비표준 — opaque)
qpgf_sdg_gate q[3];
cx q[2], q[3];
// UNMAPPED iswap [2, 3]  (QASM3 비표준 — opaque)
qpgf_iswap q[2], q[3];
// UNMAPPED iswap [2, 3]  (QASM3 비표준 — opaque)
qpgf_iswap q[2], q[3];
// UNMAPPED iswap [2, 3]  (QASM3 비표준 — opaque)
qpgf_iswap q[2], q[3];
z q[2];
z q[3];
cx q[0], q[1];
t q[1];
// UNMAPPED sdg_gate [1]  (QASM3 비표준 — opaque)
qpgf_sdg_gate q[1];
cx q[0], q[1];
// UNMAPPED iswap [0, 1]  (QASM3 비표준 — opaque)
qpgf_iswap q[0], q[1];
// UNMAPPED iswap [0, 1]  (QASM3 비표준 — opaque)
qpgf_iswap q[0], q[1];
// UNMAPPED iswap [0, 1]  (QASM3 비표준 — opaque)
qpgf_iswap q[0], q[1];
z q[0];
z q[1];
