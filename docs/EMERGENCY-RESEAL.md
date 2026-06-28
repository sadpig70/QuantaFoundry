# Emergency Re-seal & Oracle Revocation Protocol (Stage 5 W5.2)

> fingerprint 2파일(verify_seal.py·contracts.py) 변경 시 전 봉인 sig 무효화 대응 절차.

## 배경

모든 `sealed.json` 의 `sig` 는 `oracle_code_hash`(=sha256(verify_seal.py)) + `contracts_code_hash`(=sha256(contracts.py)) 를 포함해 산출된다. 이 2파일이 1바이트라도 바뀌면 전 봉인의 sig 가 깨진다(설계된 결합 — 오라클 무결성 보증).

## 무결성 점검

```
python scripts/oracle_rollback_protocol.py
```
현 sha256 == 전 sealed 의 기록값이면 `ALL INTACT`. 하나라도 불일치 = fingerprint 변경 감지.

## 변경 감지 시 절차

1. **검토** — `git diff` 로 fingerprint 2파일 변경이 의도(업그레이드)인지 버그인지 판정.

2. **버그면 rollback** — `git revert`/`git checkout` 으로 2파일 복원 → 재봉인 불필요(sig 복원).

3. **정당한 업그레이드면 재봉인**:
   - 영향 sealed 를 `registry/REGISTRY-MANIFEST.json` 의 `revocation_list` 에 등재.
   - `python scripts/reproduce_all.py` 로 전 모듈·앱 재봉인(새 oracle_code_hash 기록).
   - 새 `registry_root_hash` 확인 → `python scripts/citation_gen.py` 로 CITATION 갱신.
   - 재봉인 완료 후 `revocation_list` 비움(전 봉인이 새 fingerprint 로 유효).

## revocation_list 규약

- 빈배열 = 전 봉인이 현 fingerprint 로 유효(정상). 본 점검이 ALL INTACT 일 때만 정당.

- 비어있지 않음 = 재봉인 진행 중 또는 폐기된 봉인 존재. blast-radius 는 `python scripts/registry_tools.py dependents <id>` 로 계산.

## 불변 제약

- fingerprint 2파일은 **절대 임의 수정 금지**. 변경은 오직 의도된 오라클 업그레이드에서만, 위 재봉인 절차를 전수 수행할 때.
