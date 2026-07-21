#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""atomic_io — 원자적 텍스트 쓰기 유틸 (Windows AV 간헐 잠금 견고).

배경(DocCountsAtomicWrite, 2026-07-21): 야간 배치 라운드 커밋 하나에서 COUNT-ONTOLOGY.json
쓰기가 실패해 stale(구값) 커밋 → CI doc_counts red(다음 라운드 self-heal·tip green). 원인은
`open(path,"w").write(text)` 직접 truncate-write 가 Windows AV(Defender) 파일 스캔 중
간헐 잠금에 취약했던 것 — 부분쓰기/PermissionError 가 stale 을 남긴다.

해법(두 기존 패턴 결합):
  - 원자성: 같은 디렉토리 임시파일에 쓴 뒤 `os.replace`(원자적 rename) — 부분쓰기 노출 없음
    (compositional_verify 의 tmp→os.replace 패턴).
  - 견고성: AV 잠금 시 `os.replace`/write 를 결정론 재시도 (qasm_export 의 재시도 패턴).

★결정론 불변: 최종 파일 **내용**은 입력 text 와 byte-identical(재시도 여부는 산출물에 무영향).
  임시파일명에 os.getpid() 를 쓰나 이는 즉시 rename 되는 임시경로일 뿐 — 산출물 아님.
  time.sleep 은 재시도 대기용(내용 무관). Date/random 미사용.

사용:
  from qf_witness.core.atomic_io import atomic_write_text
  atomic_write_text(path, text)                 # newline="\n" 기본(LF 고정)
  atomic_write_text(path, text, newline="")     # 개행 변환 없음(문서 마커 보존용)
"""
from __future__ import annotations
import os
import time


def atomic_write_text(path: str, text: str, *, encoding: str = "utf-8",
                      newline: str = "\n", attempts: int = 5) -> None:
    """text 를 path 에 원자적으로 쓴다(임시파일→os.replace). AV 잠금 시 결정론 재시도.

    최종 내용은 text 와 byte-identical. 실패가 attempts 회 지속되면 마지막 예외를 재전파."""
    d = os.path.dirname(path) or "."
    os.makedirs(d, exist_ok=True)
    tmp = os.path.join(d, f".{os.path.basename(path)}.tmp{os.getpid()}")
    last_exc: OSError | None = None
    for attempt in range(1, attempts + 1):
        try:
            with open(tmp, "w", encoding=encoding, newline=newline) as f:
                f.write(text)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp, path)                 # 원자적 — 성공 시 tmp 소멸
            return
        except OSError as e:                       # AV 잠금(PermissionError 포함) 간헐 실패
            last_exc = e
            if attempt == attempts:
                break
            time.sleep(0.25 * attempt)            # 결정론 백오프(내용 무관)
    # 최종 실패: 임시파일 정리 후 재전파
    try:
        if os.path.exists(tmp):
            os.remove(tmp)
    except OSError:
        pass
    raise last_exc if last_exc is not None else OSError(f"atomic_write_text failed: {path}")
