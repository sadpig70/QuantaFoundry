OPENQASM 3.0;
include "stdgates.inc";
qubit[3] q;

gate qpgf_rx_negpi4 q0 { }  // opaque: rx_negpi4 (1q), golden in registry/modules/rx_negpi4.sealed.json
gate qpgf_rz_negpi8 q0 { }  // opaque: rz_negpi8 (1q), golden in registry/modules/rz_negpi8.sealed.json

cx q[0], q[1];
// UNMAPPED rz_negpi8 [1]  (QASM3 비표준 — opaque)
qpgf_rz_negpi8 q[1];
cx q[0], q[1];
cx q[1], q[2];
// UNMAPPED rz_negpi8 [2]  (QASM3 비표준 — opaque)
qpgf_rz_negpi8 q[2];
cx q[1], q[2];
// UNMAPPED rx_negpi4 [0]  (QASM3 비표준 — opaque)
qpgf_rx_negpi4 q[0];
// UNMAPPED rx_negpi4 [1]  (QASM3 비표준 — opaque)
qpgf_rx_negpi4 q[1];
// UNMAPPED rx_negpi4 [2]  (QASM3 비표준 — opaque)
qpgf_rx_negpi4 q[2];
cx q[0], q[1];
// UNMAPPED rz_negpi8 [1]  (QASM3 비표준 — opaque)
qpgf_rz_negpi8 q[1];
cx q[0], q[1];
cx q[1], q[2];
// UNMAPPED rz_negpi8 [2]  (QASM3 비표준 — opaque)
qpgf_rz_negpi8 q[2];
cx q[1], q[2];
