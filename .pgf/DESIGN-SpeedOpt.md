# DESIGN-SpeedOpt — reproduce 파이프라인 속도 최적화 (O1+O2)

> PGF full-cycle · 2026-07-13 · 근거: 실측 프로파일(frontier_block 730s 순차·deep 오라우팅 35×)
> 불변 전제: 오라클 무접촉 · 유니터리 값 동일(hash 불변) · 게이트 판정 로직 무변경 · root 불변

```
SpeedOpt // reproduce 속도 최적화 — 실측 병목 2건 (done — 2026-07-13) @v:1.1
    O2_PermKernelRouting // 순열 커널 전면 라우팅 — deep 오라우팅 수정 + 표준 경로 통일 (in-progress)
        UnifyReassemble // _reassemble 내부를 kernel dispatch 로 교체 (in-progress)
            # input: n, parsed[(gid,tg,k)], drop/swap(teeth 용)
            # process: step 마다 _module_kernel(gid) → perm 이면 _perm_plan 행 gather(in-place),
            #          dense 면 V = apply_left(U,tg,n,V). drop/swap 의미 보존(루프 구조 동일).
            # criteria: fast==sealed 표본 14 전부 일치 · teeth swap → mismatch 불변
        DeepRoutingFix // run_deep 분기 제거 — cost 무관 _reassemble_fast 사용 (in-progress)
            # 현재: cost<CKPT_MIN_COST → 구형 dense 경로(24ms/step). 수정: 항상 fast(ckpt 는
            #   CKPT_INTERVAL 넘는 앱에서만 자연 발동 — 소형앱 오버헤드 0).
            # criteria: deep 재검증 표본 시간 ≥10× 단축 · verified 값 불변
        EquivGate // 등가성 게이트 (needs-verify) @dep:UnifyReassemble,DeepRoutingFix
            # criteria: (1) 표본 14 fast==row==sealed (2) quick run all_ok·teeth·teeth_inline 불변
            #           (3) full sidecar 재생성 == 기존(verified/failed/counts diff 없음)
    O1_FrontierBlockParallel // frontier_block 내부 병렬화 — 730s 순차 → ~200s (in-progress)
        ParallelSubSteps // FRONTIER_STEPS 를 ThreadPool subprocess 병렬 (in-progress)
            # input: FRONTIER_STEPS 13개 — 독립 read-only argv(각자 자기 REPORT sidecar 만 기록)
            # process: ThreadPoolExecutor(min(6, cpu-2)) 로 cx.run 병렬 → 결과 dict 는 원순서 조립
            # criteria: steps dict 키 순서 == 기존(INV-RA2 계열) · 각 스텝 판정값 동일
        FactorySequential // factory --reproduce 는 병렬 뒤 순차 유지 (in-progress)
            # 이유: FACTORY-FRONTIER.json 등 공유 상태 접근 가능성 — 보수적 격리
        ChangedOnlyUntouched // changed-only 분기(coherence 경로)는 무변경 (done — 설계상 제외)
    VerifyGate // 최종 검증 (needs-verify) @dep:O2_PermKernelRouting,O1_FrontierBlockParallel
        # criteria: (1) full reproduce REPRODUCED·root 3c953d32 불변 (2) frontier_block 실측 ≥3× 단축
        #           (3) deep 표본 실측 ≥10× (4) 기존 봉인/frozen byte-identical
```

## 사전 검토 (3관점, plan 진입 게이트)

**[실현성]** O2 = 기실증 커널 재사용(값 동일 논증·등가성 테스트 존재). O1 = `--jobs` 병렬화와 동일
전제(독립 argv subprocess)의 내부 적용 — 이미 검증된 패턴. 둘 다 신규 알고리즘 없음. ✅

**[위험]** ① O2 의 drop/swap(teeth) 의미 보존 — 루프 구조를 유지하고 kernel dispatch 만 바꿔 회피,
EquivGate (2)로 강제. ② O1 의 병렬 쓰기 충돌 — frontier 스크립트는 각자 자기 REPORT 파일만 기록
(교차 없음 확인), factory 는 순차 격리. ③ BLAS 스레드 경합 — 서브프로세스 단위 병렬이라 OS 스케줄링에
위임(기존 --jobs 와 동일 특성, 벽시계 이득 실증됨). ④ 결정론 — 병렬화는 실행 순서만 바꾸고 각 스텝은
독립 결정론(파일 단위), 판정·root 무영향. ✅

**[아키텍처]** 수정 파일 2개(compositional_verify.py 내부 dispatch·special.py frontier_block)로 국소화.
manifest/게이트/오라클 무접촉. 기존 _reassemble_fast·_module_kernel·_perm_plan 재사용(중복 구현 없음). ✅

→ 판정: Critical 0 · High 0 — plan/execute 진행.
```


## 실행 결과 (verify 폐합, 2026-07-13)

- **O2 (done)**: 등가성 14표본·teeth·quick/full 전부 통과. deep 표본 51.7s→1.45s(**36×**),
  compositional full 64s→11-17s. sidecar 값 diff 0(레지스트리 성장분 제외).
- **O1 (done, rework 2회)**: ★설계 위험 ②의 전제 붕괴 실측 — legacy frontier 스크립트는 spec/봉인
  파일을 재기록하며, 상주 AV(ASDSvc)의 일시 파일잠금으로 병렬 쓰기가 간헐 실패.
  rework1=N-가족 직렬 그룹(불충분) → rework2=**2상 분리+실패분 순차 재시도 1회**(결정론 재유도라
  재실행이 byte-identical 수렴 — transient self-heal, 진짜 실패는 재시도서도 실패로 정직 유지).
  안정성 3/3 trial 통과. frontier_block 730s→334-457s(**1.6-2.2×** — 목표 3× 미달, AV 재시도
  오버헤드+oversubscription 이 구조적 floor. 정직 기록).
- **VerifyGate**: full reproduce **REPRODUCED**·root 3c953d32 불변·기존 봉인/frozen byte-identical.
  full 벽시계 1152s→**867s(1.33×)** · 배치 후처리(deep)= **~36×**(30-50분→~2분).
