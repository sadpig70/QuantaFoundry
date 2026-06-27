"""crossmodel_adapter.py — cross-model 출처 어댑터 (외부 의존 골격).

KeyFreeConsensus 의 unkeyed regime 은 *물리적으로 다른 weights* 출처가 ≥2 수렴해야 MULTIMODEL
등급에 도달한다(E5' B4: 같은-weights 합의는 독립단위 1로 거부됨). 현 워크스페이스는 단일 모델
환경이라 실제 cross-model 호출은 **외부 의존**이다 — 이 파일은 실배포 시 연결할 인터페이스/stub.

실배포: endpoint(다른 모델 API)를 주입하면 generate()가 formal spec 으로 golden 을 생성하고
u_hash 를 돌려준다. weights_id 가 서로 달라야 independence_unit 이 분리된다(같은 모델 = 같은 단위).
"""


class CrossModelSource:
    def __init__(self, model_id: str, weights_id: str, endpoint=None):
        self.model_id = model_id
        self.weights_id = weights_id      # independence 단위 키 — 모델별로 반드시 달라야 함
        self.endpoint = endpoint          # 실배포 시 다른 모델 호출 핸들 (None = 미연결)

    def available(self) -> bool:
        return self.endpoint is not None

    def generate(self, intent_id: str, formal_spec: dict) -> str:
        """formal spec → 다른 모델 golden 산출 → u_hash. 미연결이면 외부 의존 명시."""
        if not self.available():
            raise NotImplementedError(
                f"cross-model '{self.model_id}' not wired (external dependency: needs a distinct-weights "
                f"model runtime). Inject `endpoint` at deployment.")
        # 실배포 구현 지점:
        #   golden = self.endpoint.author_golden(intent_id, formal_spec)
        #   return uhash(golden)
        raise NotImplementedError("endpoint.author_golden not implemented in this environment")

    def as_source(self, intent_id, formal_spec, Source, uhash):
        return Source(f"{intent_id}_{self.model_id}", "model", self.weights_id,
                      self.generate(intent_id, formal_spec))


def available_panel(adapters):
    """연결된 cross-model 출처만 반환 (미연결은 합의에서 자동 제외)."""
    return [a for a in adapters if a.available()]
