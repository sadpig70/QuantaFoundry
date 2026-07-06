OPENQASM 3.0;
include "stdgates.inc";
qubit[3] q;

gate qpgf_rx_y4_p q0 { }  // opaque: rx_y4_p (1q), golden in registry/modules/rx_y4_p.sealed.json
gate qpgf_rx_y4_q q0 { }  // opaque: rx_y4_q (1q), golden in registry/modules/rx_y4_q.sealed.json
gate qpgf_rz_y4_p q0 { }  // opaque: rz_y4_p (1q), golden in registry/modules/rz_y4_p.sealed.json
gate qpgf_rz_y4_q q0 { }  // opaque: rz_y4_q (1q), golden in registry/modules/rz_y4_q.sealed.json

cx q[0], q[1];
// UNMAPPED rz_y4_p [1]  (QASM3 비표준 — opaque)
qpgf_rz_y4_p q[1];
cx q[0], q[1];
cx q[1], q[2];
// UNMAPPED rz_y4_p [2]  (QASM3 비표준 — opaque)
qpgf_rz_y4_p q[2];
cx q[1], q[2];
// UNMAPPED rx_y4_p [0]  (QASM3 비표준 — opaque)
qpgf_rx_y4_p q[0];
// UNMAPPED rx_y4_p [1]  (QASM3 비표준 — opaque)
qpgf_rx_y4_p q[1];
// UNMAPPED rx_y4_p [2]  (QASM3 비표준 — opaque)
qpgf_rx_y4_p q[2];
cx q[0], q[1];
// UNMAPPED rz_y4_p [1]  (QASM3 비표준 — opaque)
qpgf_rz_y4_p q[1];
cx q[0], q[1];
cx q[1], q[2];
// UNMAPPED rz_y4_p [2]  (QASM3 비표준 — opaque)
qpgf_rz_y4_p q[2];
cx q[1], q[2];
cx q[0], q[1];
// UNMAPPED rz_y4_p [1]  (QASM3 비표준 — opaque)
qpgf_rz_y4_p q[1];
cx q[0], q[1];
cx q[1], q[2];
// UNMAPPED rz_y4_p [2]  (QASM3 비표준 — opaque)
qpgf_rz_y4_p q[2];
cx q[1], q[2];
// UNMAPPED rx_y4_p [0]  (QASM3 비표준 — opaque)
qpgf_rx_y4_p q[0];
// UNMAPPED rx_y4_p [1]  (QASM3 비표준 — opaque)
qpgf_rx_y4_p q[1];
// UNMAPPED rx_y4_p [2]  (QASM3 비표준 — opaque)
qpgf_rx_y4_p q[2];
cx q[0], q[1];
// UNMAPPED rz_y4_p [1]  (QASM3 비표준 — opaque)
qpgf_rz_y4_p q[1];
cx q[0], q[1];
cx q[1], q[2];
// UNMAPPED rz_y4_p [2]  (QASM3 비표준 — opaque)
qpgf_rz_y4_p q[2];
cx q[1], q[2];
cx q[0], q[1];
// UNMAPPED rz_y4_q [1]  (QASM3 비표준 — opaque)
qpgf_rz_y4_q q[1];
cx q[0], q[1];
cx q[1], q[2];
// UNMAPPED rz_y4_q [2]  (QASM3 비표준 — opaque)
qpgf_rz_y4_q q[2];
cx q[1], q[2];
// UNMAPPED rx_y4_q [0]  (QASM3 비표준 — opaque)
qpgf_rx_y4_q q[0];
// UNMAPPED rx_y4_q [1]  (QASM3 비표준 — opaque)
qpgf_rx_y4_q q[1];
// UNMAPPED rx_y4_q [2]  (QASM3 비표준 — opaque)
qpgf_rx_y4_q q[2];
cx q[0], q[1];
// UNMAPPED rz_y4_q [1]  (QASM3 비표준 — opaque)
qpgf_rz_y4_q q[1];
cx q[0], q[1];
cx q[1], q[2];
// UNMAPPED rz_y4_q [2]  (QASM3 비표준 — opaque)
qpgf_rz_y4_q q[2];
cx q[1], q[2];
cx q[0], q[1];
// UNMAPPED rz_y4_p [1]  (QASM3 비표준 — opaque)
qpgf_rz_y4_p q[1];
cx q[0], q[1];
cx q[1], q[2];
// UNMAPPED rz_y4_p [2]  (QASM3 비표준 — opaque)
qpgf_rz_y4_p q[2];
cx q[1], q[2];
// UNMAPPED rx_y4_p [0]  (QASM3 비표준 — opaque)
qpgf_rx_y4_p q[0];
// UNMAPPED rx_y4_p [1]  (QASM3 비표준 — opaque)
qpgf_rx_y4_p q[1];
// UNMAPPED rx_y4_p [2]  (QASM3 비표준 — opaque)
qpgf_rx_y4_p q[2];
cx q[0], q[1];
// UNMAPPED rz_y4_p [1]  (QASM3 비표준 — opaque)
qpgf_rz_y4_p q[1];
cx q[0], q[1];
cx q[1], q[2];
// UNMAPPED rz_y4_p [2]  (QASM3 비표준 — opaque)
qpgf_rz_y4_p q[2];
cx q[1], q[2];
cx q[0], q[1];
// UNMAPPED rz_y4_p [1]  (QASM3 비표준 — opaque)
qpgf_rz_y4_p q[1];
cx q[0], q[1];
cx q[1], q[2];
// UNMAPPED rz_y4_p [2]  (QASM3 비표준 — opaque)
qpgf_rz_y4_p q[2];
cx q[1], q[2];
// UNMAPPED rx_y4_p [0]  (QASM3 비표준 — opaque)
qpgf_rx_y4_p q[0];
// UNMAPPED rx_y4_p [1]  (QASM3 비표준 — opaque)
qpgf_rx_y4_p q[1];
// UNMAPPED rx_y4_p [2]  (QASM3 비표준 — opaque)
qpgf_rx_y4_p q[2];
cx q[0], q[1];
// UNMAPPED rz_y4_p [1]  (QASM3 비표준 — opaque)
qpgf_rz_y4_p q[1];
cx q[0], q[1];
cx q[1], q[2];
// UNMAPPED rz_y4_p [2]  (QASM3 비표준 — opaque)
qpgf_rz_y4_p q[2];
cx q[1], q[2];
