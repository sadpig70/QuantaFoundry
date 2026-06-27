"""Generate Round 4 app-bloq circuits."""
import json, os

submissions = []

# --- 1. iqft2 (n=2): Inverse QFT on 2 qubits ---
# Forward raw QFT2: swap(0,1); H(1); cs(1,0); H(0)
# iQFT2 = reverse+dagger: H(0); cs_dag(1,0); H(1); swap(0,1)
# Alternative (own design): swap first, then H on MSB, CS_dag MSB->LSB, H on LSB
submissions.append({
    "id": "iqft2", "n_sys": 2,
    "circuit": [
        {"gate": "swap", "targets": [0,1]},
        {"gate": "h",    "targets": [0]},
        {"gate": "cs_dag", "targets": [0,1]},
        {"gate": "h",    "targets": [1]}
    ],
    "construction_method": "Forward raw QFT2 = swap + H(LSB) + cs(LSB->MSB) + H(MSB). iQFT2 = reverse each gate and dagger: H(MSB) + cs_dag(MSB->LSB) + H(LSB) + swap. Wire 0=MSB.",
    "self_check": "swap fixes bit-reversal; H+cs_dag+H is standard IQFT core. 4x4 unitary expected."
})

# --- 2. iqft3 (n=3): Inverse QFT on 3 qubits ---
# Forward raw QFT3: H(0); cs(0,1); ct(0,2); H(1); cs(1,2); H(2); swap(0,2)
# iQFT3 = reverse+dagger: swap(0,2); H(2); cs_dag(1,2); H(1); ct_dag(0,2); cs_dag(0,1); H(0)
# ct_dag = cr3_dag (controlled-T-dagger)
submissions.append({
    "id": "iqft3", "n_sys": 3,
    "circuit": [
        {"gate": "swap", "targets": [0,2]},
        {"gate": "h",    "targets": [2]},
        {"gate": "cs_dag", "targets": [1,2]},
        {"gate": "h",    "targets": [1]},
        {"gate": "cr3_dag", "targets": [0,2]},
        {"gate": "cs_dag", "targets": [0,1]},
        {"gate": "h",    "targets": [0]}
    ],
    "construction_method": "Forward raw QFT3 = H(MSB) + cs(0,1) + ct(0,2) + H + cs(1,2) + H(LSB) + swap(0,2). iQFT3 = reverse+dagger. ct_dag = cr3_dag.",
    "self_check": "Standard IQFT3 decomposition: swap for bit-reversal fix, H gates, cs_dag/cr3_dag for controlled rotation daggers. 8x8 unitary."
})

# --- 3. cmul2_mod15 (n=5): Controlled multiply-by-2 mod 15 ---
# q0=control, q1..q4=work (q1=MSB of work)
# y -> (2y mod 15) = cyclic left rotate 4 bits = [q1,q2,q3,q4] -> [q2,q3,q4,q1]
# Using 3 fredkin (controlled-SWAP) gates: fredkin(ctrl, a, b) swaps a,b when ctrl=1
# swap(1,2), swap(2,3), swap(3,4) = cyclic left by 1
submissions.append({
    "id": "cmul2_mod15", "n_sys": 5,
    "circuit": [
        {"gate": "fredkin", "targets": [0, 1, 2]},
        {"gate": "fredkin", "targets": [0, 2, 3]},
        {"gate": "fredkin", "targets": [0, 3, 4]}
    ],
    "construction_method": "Cyclic left-rotate [q1,q2,q3,q4] via 3 controlled swaps. fredkin(0,1,2) swaps 1-2, then (0,2,3) swaps 2-3, then (0,3,4) swaps 3-4. When ctrl=1: [a,b,c,d]->[b,c,d,a]. y=0 and y=15 are fixed points (all bits equal).",
    "self_check": "3 fredkin gates. y=0: all-zero unchanged. y=15: all-one unchanged. y in 1..14: cyclic left rotate. 32x32 unitary."
})

# --- 4. cmul4_mod15 (n=5): Controlled multiply-by-4 mod 15 ---
# y -> (4y mod 15) = cyclic left rotate by 2 = cmul2 applied twice
# Shortcut: swap(1,3) and swap(2,4) controlled
submissions.append({
    "id": "cmul4_mod15", "n_sys": 5,
    "circuit": [
        {"gate": "fredkin", "targets": [0, 1, 3]},
        {"gate": "fredkin", "targets": [0, 2, 4]}
    ],
    "construction_method": "Cyclic left-rotate by 2 positions: [a,b,c,d]->[c,d,a,b]. Two controlled swaps: fredkin(0,1,3) swaps q1<->q3, then fredkin(0,2,4) swaps q2<->q4. Equivalent to cmul2 applied twice but shorter.",
    "self_check": "2 fredkin gates. y=0 and y=15 fixed points. y in 1..14: cyclic left by 2. 32x32 unitary."
})

# --- 5. qpe_s (n=3): QPE of S gate, 2 counting qubits ---
# q0,q1=counting(q0=MSB), q2=target. U=S.
# Sequence: H on counting, CZ(q0,q2)=U^2, CS(q1,q2)=U^1, iQFT2 on {q0,q1}
# iQFT2 design: swap(0,1), H(0), cs_dag(0,1), H(1)
submissions.append({
    "id": "qpe_s", "n_sys": 3,
    "circuit": [
        {"gate": "h",  "targets": [0]},
        {"gate": "h",  "targets": [1]},
        {"gate": "cz", "targets": [0, 2]},
        {"gate": "cs", "targets": [1, 2]},
        {"gate": "swap", "targets": [0, 1]},
        {"gate": "h",    "targets": [0]},
        {"gate": "cs_dag", "targets": [0, 1]},
        {"gate": "h",    "targets": [1]}
    ],
    "construction_method": "Standard QPE circuit: H on counting qubits, controlled-U powers (U^2=CZ on |101>,|111>; U^1=CS on |011>,|111>), then iQFT2 on counting register. iQFT2 = swap + H(MSB) + cs_dag(MSB->LSB) + H(LSB).",
    "self_check": "QPE of S: T=diag(1,i), U^2=Z, U^1=S. iQFT2 produces phase estimate. 8x8 unitary."
})

# --- 6. qpe_t (n=4): QPE of T gate, 3 counting qubits ---
# q0,q1,q2=counting(q0=MSB), q3=target. U=T.
# Sequence: H on counting, CZ(q0,q3)=U^4, CS(q1,q3)=U^2, CT(q2,q3)=U^1, iQFT3
# iQFT3 design: swap(0,2), H(2), cs_dag(1,2), H(1), cr3_dag(0,2), cs_dag(0,1), H(0)
submissions.append({
    "id": "qpe_t", "n_sys": 4,
    "circuit": [
        {"gate": "h",  "targets": [0]},
        {"gate": "h",  "targets": [1]},
        {"gate": "h",  "targets": [2]},
        {"gate": "cz", "targets": [0, 3]},
        {"gate": "cs", "targets": [1, 3]},
        {"gate": "ct", "targets": [2, 3]},
        {"gate": "swap", "targets": [0, 2]},
        {"gate": "h",    "targets": [2]},
        {"gate": "cs_dag", "targets": [1, 2]},
        {"gate": "h",    "targets": [1]},
        {"gate": "cr3_dag", "targets": [0, 2]},
        {"gate": "cs_dag", "targets": [0, 1]},
        {"gate": "h",    "targets": [0]}
    ],
    "construction_method": "QPE of T: U^4=Z, U^2=S, U^1=T. H on 3 counting qubits, controlled powers to target, then iQFT3 on counting register (swap + H + cs_dag/cr3_dag).",
    "self_check": "QPE of T=diag(1,e^(i*pi/4)). Controlled rotations CZ,CS,CT to q3. iQFT3 resolves phase. 16x16 unitary."
})

# --- 7. shor15_a2 (n=7): Shor period-finding for N=15, a=2 ---
# q0,q1,q2=counting(q0=MSB), q3..q6=work(q3=MSB)
# U = multiply-by-2 mod 15. U^4 = I (period r=4).
# Sequence: H on counting, CU^2(q1), CU^1(q2), iQFT3
# CU^4(q0) = I (skip)
# CU^2 = cyclic left by 2: fredkin(q1,3,5), fredkin(q1,4,6)
# CU^1 = cyclic left by 1: fredkin(q2,3,4), fredkin(q2,4,5), fredkin(q2,5,6)
# iQFT3: swap(0,2), H(2), cs_dag(1,2), H(1), cr3_dag(0,2), cs_dag(0,1), H(0)
submissions.append({
    "id": "shor15_a2", "n_sys": 7,
    "circuit": [
        {"gate": "h",  "targets": [0]},
        {"gate": "h",  "targets": [1]},
        {"gate": "h",  "targets": [2]},
        {"gate": "fredkin", "targets": [1, 3, 5]},
        {"gate": "fredkin", "targets": [1, 4, 6]},
        {"gate": "fredkin", "targets": [2, 3, 4]},
        {"gate": "fredkin", "targets": [2, 4, 5]},
        {"gate": "fredkin", "targets": [2, 5, 6]},
        {"gate": "swap", "targets": [0, 2]},
        {"gate": "h",    "targets": [2]},
        {"gate": "cs_dag", "targets": [1, 2]},
        {"gate": "h",    "targets": [1]},
        {"gate": "cr3_dag", "targets": [0, 2]},
        {"gate": "cs_dag", "targets": [0, 1]},
        {"gate": "h",    "targets": [0]}
    ],
    "construction_method": "Shor order-finding for N=15, a=2 (period r=4). H on 3 counting qubits. CU^4(q0)=I skipped. CU^2(q1): 2 fredkin for cyclic left-by-2 on work register. CU^1(q2): 3 fredkin for cyclic left-by-1. iQFT3 on counting register resolves period into |++...> states with period r=4 encoded.",
    "self_check": "Standard Shor circuit: CU^k implement modular exponentiation a^(2^k) mod 15 via bit rotation. iQFT3 extracts period. 128x128 unitary."
})

# Build output
output = {
    "runtime": "deepseek",
    "weights_id": "deepseek-v4-pro",
    "convention_ack": True,
    "submissions": submissions
}

outdir = r"D:\QuantaFoundry\_workspace\crossmodel\apps2\submissions_bloq"
os.makedirs(outdir, exist_ok=True)
outpath = os.path.join(outdir, "deepseek.bloq.json")
with open(outpath, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2)
print(f"Saved: {outpath}")
print(f"Intents: {len(submissions)}")
for s in submissions:
    print(f"  {s['id']:16s} n={s['n_sys']}  gates={len(s['circuit'])}")
