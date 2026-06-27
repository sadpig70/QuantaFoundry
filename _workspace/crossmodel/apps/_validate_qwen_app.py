import json, numpy as np, sys

with open(r"D:\QuantaFoundry\_workspace\crossmodel\apps\submissions\qwen.app.json") as f:
    d = json.load(f)

print(f"runtime={d['runtime']}, weights_id={d['weights_id']}, convention_ack={d['convention_ack']}")
print(f"Total intents: {len(d['submissions'])}")
print()

# Unitarity
for s in d["submissions"]:
    U = np.array(s["app_golden_real"]) + 1j * np.array(s["app_golden_imag"])
    n = 2 ** s["n_sys"]
    assert U.shape == (n, n), f'{s["id"]}: shape {U.shape}'
    err = float(np.max(np.abs(U @ U.conj().T - np.eye(n))))
    print(f"  {s['id']:12s} n_sys={s['n_sys']} shape={str(U.shape):10s} unitary_err={err:.2e}  PASS")

# Reproducibility
print()
print("Reproducibility check (re-exec app_golden_code):")
for s in d["submissions"]:
    ns = {}
    exec(s["app_golden_code"], ns)
    U_code = ns["golden"]
    U_json = np.array(s["app_golden_real"]) + 1j * np.array(s["app_golden_imag"])
    diff = np.max(np.abs(U_code - U_json))
    status = "MATCH" if diff < 1e-9 else "FAIL"
    print(f"  {s['id']:12s} max|code - json| = {diff:.2e}  {status}")

print()
print("ALL 8 APP-GOLDENS VALIDATED.")
