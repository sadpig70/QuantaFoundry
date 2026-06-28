# -*- coding: utf-8 -*-
"""runtime_identity.py — Stage 5 W5.3 [EXT]: 런타임 신원증명 (Sybil 방어).

blind-spot: gated panel 의 "≥2 distinct weights" 독립성은 *자기신고* 기반이다 — 한 런타임이
다중 weights_id 를 가장(Sybil)하면 가짜 독립합의를 만들 수 있다. 방어: 제출을 ed25519 서명한
bundle 로 받고, **independence_unit 을 runtime_pubkey 로 강화**한다. 같은 pubkey = 같은 물리
런타임 = 1 독립단위 → distinct weights 가장이 1 vote 로 병합돼 Sybil 이 무력화된다.

self-contained(메커니즘): 결정론 합성 keypair 로 (1) 서명/검증 (2) Sybil(같은 pubkey, 다른
weights) → 1 unit 병합 → 합의 붕괴 (3) 진짜 2런타임(다른 pubkey) → 2 unit → ESTABLISHED 를 실증.
[EXT] relay: 실 런타임의 공개키 등록·서명 수급은 패널 배포 필요.

비파괴: 검증/스키마 전용. registry/sealed/frozen 불변. `.pgf/hardening/`·패널패키지 가산.
소비 자산(사용만): consensus(Source/establish_truth) · cryptography(ed25519).

사용:  python scripts/runtime_identity.py
"""
from __future__ import annotations
import os, sys, json, hashlib
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(ROOT, ".pgf", "keyfree"))
import consensus as C                 # noqa: E402  Source/establish_truth 사용만

OUT = os.path.join(ROOT, ".pgf", "hardening")
PKG = os.path.join(ROOT, "_workspace", "crossmodel", "identity_round")


def _keypair(seed_label):
    """결정론 합성 keypair (데모용; 실 런타임은 자체 보관 비밀키)."""
    seed = hashlib.sha256(seed_label.encode()).digest()[:32]
    priv = ed25519.Ed25519PrivateKey.from_private_bytes(seed)
    pub = priv.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw).hex()
    return priv, pub


def make_bundle(priv, pub, weights_id, u_hash, nonce):
    """signed submission bundle = {weights_id, runtime_pubkey, u_hash, nonce, signature}."""
    msg = f"{weights_id}|{u_hash}|{nonce}".encode()
    sig = priv.sign(msg).hex()
    return {"weights_id": weights_id, "runtime_pubkey": pub, "u_hash": u_hash,
            "nonce": nonce, "signature": sig}


def verify_bundle(b):
    msg = f"{b['weights_id']}|{b['u_hash']}|{b['nonce']}".encode()
    try:
        ed25519.Ed25519PublicKey.from_public_bytes(bytes.fromhex(b["runtime_pubkey"])).verify(
            bytes.fromhex(b["signature"]), msg)
        return True
    except Exception:
        return False


def source_from_bundle(b):
    """independence_unit 을 pubkey 로 강화 — 같은 pubkey = 같은 물리 런타임 = 1 단위(Sybil 차단)."""
    return C.Source(b["weights_id"], "model", f"pk:{b['runtime_pubkey'][:16]}", b["u_hash"])


def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(PKG, exist_ok=True)
    print("=" * 84)
    print("RuntimeIdentityProof (W5.3 [EXT]) — ed25519 signed bundle + Sybil 방어")
    print("=" * 84)
    U = "340b5f344fae9b99e..."   # 임의 합의 답(qft3 류) — 데모용 u_hash
    checks = []

    # 1) 서명/검증 무결성 (teeth): 정상 bundle 검증 통과, 위변조(weights_id 바꿈)는 거부
    privA, pubA = _keypair("runtimeA")
    b_ok = make_bundle(privA, pubA, "modelX", U, "n1")
    b_tampered = dict(b_ok, weights_id="modelEVIL")   # 서명 후 내용 변조
    checks.append({"name": "signature_integrity", "valid_accepts": verify_bundle(b_ok),
                   "tampered_rejected": not verify_bundle(b_tampered),
                   "pass": verify_bundle(b_ok) and not verify_bundle(b_tampered)})

    # 2) Sybil teeth: 한 런타임(pubA)이 distinct weights 2개 가장 → 같은 pubkey → 1 unit → 합의 붕괴
    b_sybil1 = make_bundle(privA, pubA, "modelX", U, "n1")
    b_sybil2 = make_bundle(privA, pubA, "modelY", U, "n2")   # 같은 키, 다른 weights_id
    s_sybil = [source_from_bundle(b_sybil1), source_from_bundle(b_sybil2)]
    r_sybil = C.establish_truth("qft3", s_sybil, N=2, rho=0.0)
    checks.append({"name": "sybil_collapses", "status": r_sybil.status, "dist": r_sybil.distribution,
                   "pass": r_sybil.status == "DIVERGENT",
                   "detail": "같은 pubkey 2제출(다른 weights_id 가장) → pubkey-unit 병합 1<2 → DIVERGENT"})

    # 3) 진짜 2런타임(다른 pubkey) → 2 unit → ESTABLISHED (정상 독립은 통과)
    privB, pubB = _keypair("runtimeB")
    b_r1 = make_bundle(privA, pubA, "modelX", U, "n1")
    b_r2 = make_bundle(privB, pubB, "modelX", U, "n2")   # 다른 키
    s_real = [source_from_bundle(b_r1), source_from_bundle(b_r2)]
    r_real = C.establish_truth("qft3", s_real, N=2, rho=0.0)
    checks.append({"name": "genuine_two_runtimes", "status": r_real.status,
                   "pass": r_real.status == "ESTABLISHED",
                   "detail": "다른 pubkey 2런타임 → 2 독립단위 → ESTABLISHED (false-negative 아님)"})

    allok = all(c["pass"] for c in checks)
    for c in checks:
        extra = (f"valid={c.get('valid_accepts')} tampered_rejected={c.get('tampered_rejected')}"
                 if c["name"] == "signature_integrity" else f"→ {c.get('status','')}")
        print(f"  {'✓' if c['pass'] else '✗'} {c['name']:22} {extra}")
        if c.get("detail"):
            print(f"      {c['detail']}")

    out = {"_schema": "runtime-identity-v1", "all_pass": allok, "checks": checks,
           "bundle_schema": {"weights_id": "str", "runtime_pubkey": "ed25519 raw hex",
                             "u_hash": "str", "nonce": "str", "signature": "ed25519 sig hex"},
           "_note": "independence_unit 을 runtime_pubkey 로 강화 → 같은 물리키가 다중 weights 가장(Sybil) "
                    "시 1 단위로 병합돼 가짜 독립합의 붕괴. ed25519 서명으로 제출 무결성. self-contained "
                    "메커니즘 실증 — 실 런타임 공개키 등록/서명 수급은 [EXT] relay. 분석/검증 전용 비파괴."}
    json.dump(out, open(os.path.join(OUT, "RUNTIME-IDENTITY.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    panel = {"_schema": "identity-panel-v1", "round": "identity_round",
             "instruction": "각 런타임은 자체 보관 ed25519 비밀키로 제출을 서명한다. bundle="
                            "{weights_id, runtime_pubkey, u_hash, nonce, signature}. 등록 시 pubkey 공개.",
             "bundle_schema": out["bundle_schema"],
             "scoring": "수거 후 verify_bundle 로 서명검증 → source_from_bundle(pubkey-unit) 으로 "
                        "establish_truth. 같은 pubkey 다중제출은 1 독립단위로 병합(Sybil 차단).",
             "relay": "정욱님 패널 런타임 공개키 등록 + 서명 제출 수급. EXT 의존."}
    json.dump(panel, open(os.path.join(PKG, "IDENTITY-PANEL-SPEC.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    os.makedirs(os.path.join(PKG, "responses"), exist_ok=True)

    print("-" * 84)
    print(f"판정: {'Sybil 방어 메커니즘 LIVE ✅' if allok else 'CHECK FAILED ✗'} · "
          f"→ .pgf/hardening/RUNTIME-IDENTITY.json · 패키지 _workspace/crossmodel/identity_round/ [EXT]")
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())
