# v0.5 런타임 붙여넣기용 프롬프트 (각 6런타임에 그대로 전달)

> 정욱님: 아래 `=== PROMPT START ===` ~ `=== PROMPT END ===` 사이 전체를 각 런타임에 **그대로** 붙여넣으세요.
> 6런타임 전부 동일 프롬프트입니다(공정성). 받은 JSON 응답을 `submissions/<runtime>.app.json` 으로 저장하고,
> 파일 안의 `runtime`/`weights_id` 두 필드를 아래 표대로 채워주세요(모델이 잘못 적었으면 정정).
>
> | 저장 파일명 | runtime | weights_id |
> |---|---|---|
> | `gpt-5.app.json` | `gpt-5` | `openai-gpt-5` |
> | `gemini.app.json` | `gemini` | `google-gemini-3.5-flash-high` |
> | `grok.app.json` | `grok` | `xai-grok` |
> | `kimi.app.json` | `kimi` | `moonshot-kimi` |
> | `qwen.app.json` | `qwen` | `alibaba-qwen` |
> | `deepseek.app.json` | `deepseek` | `deepseek-v4-pro` |

---

```
=== PROMPT START ===
You are one independent runtime in a cross-model quantum-gate consensus experiment. Do NOT search the web,
do NOT coordinate with any other model, do NOT ask clarifying questions. Answer entirely on your own.

TASK: For each of the 6 intents below, return the complex unitary matrix U it denotes, as JSON.

MATRIX CONVENTION:
- U[out, in] = <out| U |in>, dtype complex, shape (2^n_sys, 2^n_sys).
- Big-endian: qubit 0 is the most-significant register.
- Global phase is free (a verifier normalizes it). NOTE: the "convention split" intents below are chosen to
  be phase-INequivalent, so your choice genuinely matters.

THE 6 INTENTS:

1. id="sanity_cz" (n_sys=2): The controlled-Z gate CZ = diag(1,1,1,-1). Fully specified.
   declared_reading = {"kind":"fixed"}

2. id="free_cphase" (n_sys=2): A controlled-phase gate diag(1,1,1,exp(i*phi)). The angle phi is YOUR FREE
   CHOICE in the open interval (0, 2*pi) with phi != pi. Do NOT fall back to a canonical value (pi / CZ);
   pick a phi you personally find interesting and COMMIT to it. There is intentionally no unique correct answer.
   declared_reading = {"phi": <your chosen radians>}

3. id="free_rz" (n_sys=1): A single-qubit Z-rotation Rz(theta) = diag(exp(-i*theta/2), exp(+i*theta/2)).
   theta is YOUR FREE CHOICE in (0, 2*pi), theta not in {0, pi}. No unique correct answer — commit to your own theta.
   declared_reading = {"theta": <your chosen radians>}

4. id="split_rz_sign" (n_sys=1): Rz at the FIXED angle theta0 = pi/2, but the SIGN CONVENTION of the
   generator is intentionally unspecified.
     reading "-":  exp(-i*theta0*Z/2) = diag(exp(-i*pi/4), exp(+i*pi/4))
     reading "+":  exp(+i*theta0*Z/2) = diag(exp(+i*pi/4), exp(-i*pi/4))
   These are NOT global-phase equivalent. Use the sign convention YOU consider standard.
   declared_reading = {"sign": "-"}  or  {"sign": "+"}

5. id="split_ry_dir" (n_sys=1): Ry at the FIXED angle theta0 = pi/2, rotation DIRECTION/sign unspecified.
     reading "-":  exp(-i*theta0*Y/2) = [[c,-s],[s,c]]
     reading "+":  exp(+i*theta0*Y/2) = [[c,s],[-s,c]]    with c=cos(pi/4), s=sin(pi/4)
   Use your standard convention.
   declared_reading = {"sign": "-"}  or  {"sign": "+"}

6. id="split_csqrtz_sign" (n_sys=2): The "controlled square-root-of-Z" gate diag(1,1,1, s*i) where
   s=+1 (controlled-S) or s=-1 (controlled-S-dagger). Which root is "the" canonical one is unspecified.
   diag(1,1,1,i) and diag(1,1,1,-i) are NOT global-phase equivalent. Pick one.
   declared_reading = {"sign": "+"}  (controlled-S)  or  {"sign": "-"}  (controlled-S-dagger)

OUTPUT — return ONE JSON object, nothing else, in exactly this shape:
{
  "runtime": "<leave as your model short name>",
  "weights_id": "<leave as your model weights id>",
  "convention_ack": true,
  "submissions": [
    {
      "id": "<intent id>",
      "n_sys": <1 or 2>,
      "app_golden_real": [[...]],          // real part, 2^n x 2^n nested lists
      "app_golden_imag": [[...]],          // imag part, same shape
      "app_golden_code": "import numpy as np\n...\ngolden = <the same 2^n x 2^n ndarray>",
      "declared_reading": { ... },         // EXACTLY per the schema above for this intent
      "construction_method": "one line: your reading; for free_* state your chosen value; for split_* state your sign",
      "self_check": "unitary, shape ok"
    }
    // ... one entry for EACH of the 6 intents, in order
  ]
}

HARD RULES:
- Answer ALL 6 intents. No coordination, no web, no clarifying questions.
- In app_golden_code use ONLY numpy/math/cmath; the final statement must assign a variable named `golden`.
- app_golden_real / app_golden_imag are primary and MUST equal the matrix your app_golden_code produces.
- declared_reading MUST honestly match the matrix you actually submit (declaring one reading but submitting
  another is auto-detected and flagged).
- For free_cphase / free_rz: COMMIT to a genuine free pick. Do not default to a "safe" canonical value;
  the experiment is observing that your free pick differs from other models'.
- Output JSON only. No prose before or after.
=== PROMPT END ===
```
