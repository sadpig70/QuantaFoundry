# -*- coding: utf-8 -*-
"""paths — 리포 경로 상수 단일 정본 (final_scripts_refactoring_plan §2-a).

★깊이 함정 해소(§2-b): 구 scripts/ 본체 137개가 `ROOT = dirname(dirname(__file__))` 로
리포 루트를 계산했다 — qf_witness/<cat>/ (깊이 2) 이동 시 전부 틀어지므로, codemod 가
그 정의를 `from qf_witness.core.paths import ROOT` 로 치환한다.

oracle 은 사용만(INV-SR4): ORACLE_DIR 은 qpgf-oracle 스킬의 위치 상수일 뿐 — 사본 금지.
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

ORACLE_DIR = os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts")
REPORTS = os.path.join(ROOT, "reports")
SPECS_APPS = os.path.join(ROOT, "specs", "apps")
SPECS_MODULES = os.path.join(ROOT, "specs", "modules")
REGISTRY = os.path.join(ROOT, "registry")
REGISTRY_APPS = os.path.join(REGISTRY, "apps")
REGISTRY_MODULES = os.path.join(REGISTRY, "modules")
PROOFS = os.path.join(ROOT, ".pgf", "proofs")
