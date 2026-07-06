OPENQASM 3.0;
include "stdgates.inc";
qubit[2] q;

gate qpgf_iswap q0, q1 { }  // opaque: iswap (2q), golden in registry/modules/iswap.sealed.json

z q[0];
z q[1];
// UNMAPPED iswap [0, 1]  (QASM3 비표준 — opaque)
qpgf_iswap q[0], q[1];
cx q[0], q[1];
t q[1];
cx q[0], q[1];
