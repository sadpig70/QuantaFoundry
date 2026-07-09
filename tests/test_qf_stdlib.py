import copy
import unittest

import numpy as np

from qf_stdlib import attest, attest_circuit, build_with_proof, check_root, load_canon, lookup, validate_canon
from qf_stdlib.adapters import adapter_convention, canonical_hash_with_adapter
from qf_stdlib.errors import AdapterConventionError, UnsupportedAdapter
from qf_stdlib.registry import load_snapshot

try:
    import cirq
except Exception:  # pragma: no cover - optional dependency may be absent outside this workspace
    cirq = None


class QFStdlibTests(unittest.TestCase):
    def test_canon_validates_against_live_registry(self):
        snapshot = load_snapshot()
        canon = load_canon()
        report = validate_canon(canon, snapshot)
        self.assertTrue(report.ok, report.errors)
        self.assertGreaterEqual(report.entries, 55)
        self.assertEqual(canon["_generated_from"]["registry_root_hash"], snapshot.registry_root_hash)

    def test_root_check_is_fast_drift_guard(self):
        snapshot = load_snapshot()
        canon = load_canon()
        report = check_root(canon, snapshot)
        self.assertTrue(report.ok, report.errors)
        self.assertEqual(report.entries, len(canon["canon"]))

    def test_root_check_detects_entry_drift(self):
        snapshot = load_snapshot()
        canon = copy.deepcopy(load_canon())
        canon["canon"]["qft/7"]["registry_root"] = "0" * 64
        report = check_root(canon, snapshot)
        self.assertFalse(report.ok)
        self.assertIn("qft/7:root_mismatch", report.errors)

    def test_expanded_palette_entries_exist(self):
        canon = load_canon()
        for key in (
            "qft/7",
            "iqft/2",
            "block-encoding/xz",
            "qsp/d5",
            "qsvt/pauli2/d3",
            "cmul/237/a2",
            "gate/x",
            "gate/h",
            "gate/cnot",
            "gate/toffoli",
            "gate/ccz",
        ):
            self.assertIn(key, canon["canon"])

    def test_base_gate_lookup_by_key_alias_id_and_hash(self):
        canon = load_canon()
        entry = lookup("gate/cnot", canon=canon)
        self.assertIsNotNone(entry)
        self.assertEqual(entry["kind"], "module")
        self.assertEqual(entry["id"], "cnot")
        self.assertEqual(lookup("cx", canon=canon)["key"], "gate/cnot")
        self.assertEqual(lookup("cnot", canon=canon)["key"], "gate/cnot")
        self.assertEqual(lookup(entry["u_hash"], canon=canon)["key"], "gate/cnot")

    def test_base_gate_attestation_preserves_module_scope(self):
        proof = attest("gate/h")
        self.assertIsNotNone(proof)
        self.assertEqual(proof["subject"]["kind"], "module")
        self.assertEqual(proof["subject"]["id"], "h_gate")
        self.assertEqual(proof["claim"]["semantic_guarantee"], "unitary_equiv")

    def test_lookup_by_key_alias_id_and_hash(self):
        canon = load_canon()
        entry = lookup("qft/8", canon=canon)
        self.assertIsNotNone(entry)
        self.assertEqual(entry["id"], "qft8_pipeline")
        self.assertEqual(lookup("qft8", canon=canon)["id"], "qft8_pipeline")
        self.assertEqual(lookup("qft8_pipeline", canon=canon)["key"], "qft/8")
        self.assertEqual(lookup(entry["u_hash"], canon=canon)["key"], "qft/8")
        self.assertIsNone(lookup("not-a-canonical-primitive", canon=canon))

    def test_attestation_is_root_anchored_lookup_not_new_seal(self):
        proof = attest("qsvt/proj/d3")
        self.assertIsNotNone(proof)
        self.assertEqual(proof["schema"], "qf-attestation-v1")
        self.assertEqual(proof["subject"]["id"], "qsvt_proj_d3")
        self.assertEqual(proof["claim"]["semantic_guarantee"], "unitary_equiv")
        self.assertIn("registry_root", proof["anchor"])
        self.assertIn("not a new oracle run", proof["limits"][1])

    @unittest.skipUnless(cirq is not None, "cirq optional dependency is unavailable")
    def test_attest_circuit_returns_root_anchored_proof_for_canon_match(self):
        qubits = cirq.LineQubit.range(3)
        circuit = cirq.Circuit(cirq.qft(*qubits, without_reverse=False))
        proof = attest_circuit(circuit, "cirq", qubit_order=qubits)
        self.assertIsNotNone(proof)
        self.assertEqual(proof["schema"], "qf-attestation-v1")
        self.assertEqual(proof["subject"]["key"], "qft/3")
        self.assertEqual(proof["subject"]["u_hash"], lookup("qft/3")["u_hash"])
        self.assertEqual(proof["proof"]["adapter"]["computed_u_hash"], lookup("qft/3")["u_hash"])
        self.assertEqual(proof["proof"]["adapter"]["convention"]["adapter"], "cirq")

    @unittest.skipUnless(cirq is not None, "cirq optional dependency is unavailable")
    def test_attest_circuit_unknown_hash_fails_closed(self):
        qubits = cirq.LineQubit.range(1)
        circuit = cirq.Circuit(cirq.MatrixGate(np.diag([1, np.exp(0.123j)])).on(qubits[0]))
        self.assertIsNone(attest_circuit(circuit, "cirq", qubit_order=qubits))

    @unittest.skipUnless(cirq is not None, "cirq optional dependency is unavailable")
    def test_attest_circuit_preserves_adapter_convention_errors(self):
        qubits = cirq.LineQubit.range(2)
        circuit = cirq.Circuit(cirq.qft(*qubits, without_reverse=False))
        with self.assertRaises(AdapterConventionError):
            attest_circuit(circuit, "cirq")

    def test_template_certificate_keeps_partial_scope(self):
        cert = build_with_proof("qpe_skeleton")
        self.assertEqual(cert["schema"], "qf-template-cert-v1")
        self.assertEqual(cert["template_id"], "qpe_skeleton")
        self.assertEqual(cert["steps"][0]["attestation"]["subject"]["id"], "iqft8")
        self.assertTrue(any("does not certify the target unitary" in limit for limit in cert["limits"]))

    def test_duplicate_alias_fails_closed(self):
        snapshot = load_snapshot()
        canon = copy.deepcopy(load_canon())
        canon["canon"]["qft/2"]["aliases"].append("qft8")
        report = validate_canon(canon, snapshot)
        self.assertFalse(report.ok)
        self.assertTrue(any("alias_collision" in err for err in report.errors))

    def test_stale_root_fails_closed(self):
        snapshot = load_snapshot()
        canon = copy.deepcopy(load_canon())
        canon["_generated_from"]["registry_root_hash"] = "0" * 64
        report = validate_canon(canon, snapshot)
        self.assertFalse(report.ok)
        self.assertIn("generated_root_mismatch", report.errors)

    def test_cached_leaf_module_cannot_be_unique_app_canon(self):
        snapshot = load_snapshot()
        cached_id = sorted(snapshot.cached_leaf_modules)[0]
        sealed = snapshot.resolve("app", cached_id)
        canon = copy.deepcopy(load_canon())
        canon["canon"]["bad/cached"] = {
            "aliases": ["bad_cached"],
            "convention": sealed.get("convention", "qualtran-raw"),
            "dependencies": [],
            "honesty_scope": "bad cached app exposure",
            "id": cached_id,
            "kind": "app",
            "n_sys": sealed.get("n_sys"),
            "registry_path": f"registry/apps/{cached_id}.sealed.json",
            "registry_root": snapshot.registry_root_hash,
            "resource": sealed.get("resource", {}),
            "selection": {"method": "test", "reason": "negative control"},
            "semantic_guarantee": "unitary_equiv",
            "sig": sealed.get("sig"),
            "tier": 0,
            "u_hash": sealed["u_hash"],
        }
        report = validate_canon(canon, snapshot)
        self.assertFalse(report.ok)
        self.assertTrue(any("cached_leaf_module_exposed_as_app" in err for err in report.errors))

    def test_optional_framework_adapter_is_explicitly_unsupported(self):
        with self.assertRaises(UnsupportedAdapter):
            canonical_hash_with_adapter(object(), "qiskit")

    @unittest.skipUnless(cirq is not None, "cirq optional dependency is unavailable")
    def test_cirq_qft_hash_matches_canon_when_convention_pinned(self):
        qubits = cirq.LineQubit.range(3)
        circuit = cirq.Circuit(cirq.qft(*qubits, without_reverse=False))
        circuit_hash = canonical_hash_with_adapter(circuit, "cirq", qubit_order=qubits)
        self.assertEqual(circuit_hash, lookup("qft/3")["u_hash"])
        self.assertEqual(lookup(circuit_hash)["key"], "qft/3")

    @unittest.skipUnless(cirq is not None, "cirq optional dependency is unavailable")
    def test_cirq_adapter_requires_explicit_qubit_order(self):
        qubits = cirq.LineQubit.range(2)
        circuit = cirq.Circuit(cirq.qft(*qubits, without_reverse=False))
        with self.assertRaises(AdapterConventionError):
            canonical_hash_with_adapter(circuit, "cirq")

    @unittest.skipUnless(cirq is not None, "cirq optional dependency is unavailable")
    def test_cirq_endian_variant_does_not_match_qft_canon(self):
        qubits = cirq.LineQubit.range(3)
        circuit = cirq.Circuit(cirq.qft(*qubits, without_reverse=True))
        circuit_hash = canonical_hash_with_adapter(circuit, "cirq", qubit_order=qubits)
        self.assertNotEqual(circuit_hash, lookup("qft/3")["u_hash"])

    @unittest.skipUnless(cirq is not None, "cirq optional dependency is unavailable")
    def test_cirq_global_phase_matches_canon(self):
        qubits = cirq.LineQubit.range(2)
        size = 1 << len(qubits)
        omega = np.exp(2j * np.pi / size)
        qft = np.array([[omega ** (j * k) for k in range(size)] for j in range(size)], dtype=complex) / np.sqrt(size)
        circuit = cirq.Circuit(cirq.MatrixGate(np.exp(0.321j) * qft).on(*qubits))
        circuit_hash = canonical_hash_with_adapter(circuit, "cirq", qubit_order=qubits)
        self.assertEqual(circuit_hash, lookup("qft/2")["u_hash"])

    @unittest.skipUnless(cirq is not None, "cirq optional dependency is unavailable")
    def test_cirq_measurement_is_rejected(self):
        qubits = cirq.LineQubit.range(1)
        circuit = cirq.Circuit(cirq.measure(qubits[0]))
        with self.assertRaises(AdapterConventionError):
            canonical_hash_with_adapter(circuit, "cirq", qubit_order=qubits)

    def test_adapter_convention_reports_pinned_cirq_contract(self):
        info = adapter_convention("cirq")
        self.assertTrue(info["qubit_order_required"])
        self.assertEqual(info["global_phase"], "normalized by QPGF hash_unitary")


if __name__ == "__main__":
    unittest.main()
