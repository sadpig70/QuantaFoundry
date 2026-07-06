OPENQASM 3.0;
include "stdgates.inc";
qubit[1] q;

gate qpgf_ry_fib q0 { }  // opaque: ry_fib (1q), golden in registry/modules/ry_fib.sealed.json

z q[0];
// UNMAPPED ry_fib [0]  (QASM3 비표준 — opaque)
qpgf_ry_fib q[0];
