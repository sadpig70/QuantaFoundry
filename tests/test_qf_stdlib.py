import copy
import unittest

from qf_stdlib import attest, build_with_proof, load_canon, lookup, validate_canon
from qf_stdlib.adapters import canonical_hash_with_adapter
from qf_stdlib.errors import UnsupportedAdapter
from qf_stdlib.registry import load_snapshot


class QFStdlibTests(unittest.TestCase):
    def test_canon_validates_against_live_registry(self):
        snapshot = load_snapshot()
        canon = load_canon()
        report = validate_canon(canon, snapshot)
        self.assertTrue(report.ok, report.errors)
        self.assertGreaterEqual(report.entries, 20)
        self.assertEqual(canon["_generated_from"]["registry_root_hash"], snapshot.registry_root_hash)

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


if __name__ == "__main__":
    unittest.main()

