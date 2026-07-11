# DESIGN — QFVerifyParallel (qf_verify 병렬 실행)

> **모드**: PGF full-cycle. **목표**: reproduce_all 벽시계 시간 단축(독립 read-only 검증 스텝 병렬화).
> **동기(정량)**: full 시간의 89%가 상위 10 heavy Python 스텝. 그중 8개(ring/resource/convention/
> discovery/hierarchy/cuc/perm_subspace/approx ≈ 507s)가 witness 그룹의 **독립 read-only 검증기**.
> **핵심 원칙**: 결정론 root 불변. 병렬은 *실행 순서*만 바꾸고 *출력(seal/sidecar)·결과 조립 순서*는 불변.

## 0. 구조 분석 (실측)

```text
profile = [core, witness, behavior]  (verification/profiles/{full,changed}.json)
  core     : forge_apps → frontier_block → registry_build → second_oracle   (4 special, 순서·변경 백본)
  witness  : column_verify · approx_certify · witness_batch(101 argv)         (103 argv, 독립 read-only)
  behavior : behavior                                                          (1 special)
분류 규칙: "special" 키 有 = 변경/순서 백본(순차). "argv" = 독립 검증기(병렬 가능).
독립성 근거: argv 스텝은 봉인물을 *읽고* 각자 고유 sidecar 를 *쓴다*(RING-COLUMN·*.column_proof·
  *-OBSERVE 등 서로 다른 파일). registry_build(선행 special)가 REGISTRY-MANIFEST 를 먼저 확정하므로
  doc_counts/structure_lint 등도 안전. 스텝 간 read-after-write 의존 없음.
```

## 1. Gantree

```text
QFVerifyParallel // 독립 스텝 병렬 실행 (designing)
    P1_SegmentedExecutor // runner 를 special-barrier 세그먼트 실행으로 (atomic)
        # 연속 argv = 병렬 세그먼트, special = 순차 싱글턴. 결과는 원래 index 로 조립.
    P2_ThreadPool // 병렬 세그먼트를 ThreadPoolExecutor(jobs)로 (atomic) @dep:P1
        # 스텝=subprocess(cx.run) → thread 안전. max_workers=min(jobs, len(batch)).
    P3_CliJobs // reproduce_all.py --jobs N (기본 1=순차 불변) (atomic) @dep:P2
    P4_Gate // 병렬 root == 순차 root == 0a6fbab0, REPRODUCED, pass-set 동치 (atomic) @dep:P3
```

## 2. PPR

```python
def run_profile(profile_id, echo=print, jobs=1):
    steps, changed_only = load_profile(profile_id)
    results = [None]*len(steps)                 # 원래 순서 슬롯
    i=0
    while i < len(steps):
        if jobs>1 and "special" not in steps[i]:
            batch = [k for k in range(i, len(steps)) if consecutive_argv(k)]  # 연속 argv run
            with ThreadPoolExecutor(min(jobs, len(batch))) as pool:
                for k in batch: results[k] = pool.submit(execute_step, steps[k], changed_only)
            i = end_of_batch
        else:                                    # special = 순차(변경 백본 순서 보존)
            results[i] = execute_step(steps[i], changed_only); i+=1
    # ★조립은 항상 원래 순서: result["steps"] 키 순서·evidence 순서 = manifest 순서(INV-RA2)
    result = {"bundle":"UNKNOWN","steps":{}}; result["mode"]=...
    for idx, st in enumerate(steps):
        frag, meta = results[idx]; result["steps"].update(frag); evidence.append(...)
    # acceptance_criteria:
    #   - jobs=1 → 기존 순차와 완전 동일(백워드 호환)
    #   - special 스텝은 항상 순차·원순서(forge→frontier→registry→2oracle→…→behavior)
    #   - result["steps"] 키/필드/순서 = 순차와 byte 동치(duration_ms 제외=휘발)
    #   - 병렬 실행이 seal/sidecar/root 를 바꾸지 않음(root 0a6fbab0 불변)
```

## 3. POLICY / 정직 경계

```text
non_destructive: 검증 로직·oracle·seal 무수정. runner 실행모델만 확장.
determinism:     root = sorted(id:u_hash) → 실행순서 무관. 결과 조립은 원순서 고정. jobs=1=기존불변.
safety:          special(변경 스텝) 절대 병렬화 금지. argv(독립 read-only)만 병렬. thread=subprocess-bound.
default:         jobs=1(순차, 기존 동작 보존). --jobs N 은 opt-in 고속 경로. 권위 게이트는 순차 유지 가능.
gate:            병렬 REPRODUCED · root 0a6fbab0 · pass-set == 순차 · steps 키집합 동치 · second_oracle 83/83.
```
