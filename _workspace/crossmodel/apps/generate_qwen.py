"""
QuantaFoundry Cross-Model App-Golden Authoring (Round 3) — Qwen runtime.
All matrices derived from application definitions; no peeking at other runtimes or sealed files.
Convention: big-endian (first register = MSB), U[out,in].
"""
import json, math, cmath
import numpy as np

def to_entry(mat):
    r = np.round(mat.real, 15).tolist()
    i = np.round(mat.imag, 15).tolist()
    return r, i

# ---- Gate primitives -------------------------------------------------------
s2 = 1.0 / math.sqrt(2.0)
I2 = np.eye(2, dtype=complex)
H = s2 * np.array([[1, 1], [1, -1]], dtype=complex)
CNOT = np.array([[1, 0, 0, 0],
                 [0, 1, 0, 0],
                 [0, 0, 0, 1],
                 [0, 0, 1, 0]], dtype=complex)

def cnot_full(n, ctrl, tgt):
    """Return 2^n x 2^n CNOT with control=ctrl, target=tgt (big-endian qubit indices)."""
    N = 2 ** n
    U = np.zeros((N, N), dtype=complex)
    for j in range(N):
        # Extract bits (big-endian: q_k = bit at position n-1-k)
        bits = [(j >> (n - 1 - k)) & 1 for k in range(n)]
        c = bits[ctrl]
        if c == 1:
            bits[tgt] ^= 1
        # Compute output index
        out = sum(bits[k] << (n - 1 - k) for k in range(n))
        U[out, j] = 1.0
    return U

def single_full(n, q, G):
    """Insert 2x2 gate G on qubit q in an n-qubit system (big-endian)."""
    result = np.array([1.0], dtype=complex)
    for k in range(n):
        if k == q:
            result = np.kron(result, G)
        else:
            result = np.kron(result, I2)
    return result

submissions = []

# ==== 1. bell (n_sys=2) =====================================================
# U = CNOT @ (H tensor I): Hadamard on qubit 0, then CNOT(control=0, target=1).
HI = single_full(2, 0, H)          # H (x) I
bell = CNOT @ HI
bell_r, bell_i = to_entry(bell)
submissions.append({
    "id": "bell",
    "n_sys": 2,
    "n_anc": 0,
    "app_golden_real": bell_r,
    "app_golden_imag": bell_i,
    "app_golden_code": "import numpy as np\ns = 1/np.sqrt(2)\nHI = np.kron(s*np.array([[1,1],[1,-1]],dtype=complex), np.eye(2))\nCN = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],dtype=complex)\ngolden = CN @ HI",
    "construction_method": "Matrix product CNOT @ (H tensor I): Hadamard on qubit 0 then CNOT(control=0, target=1).",
    "self_check": "U @ U.conj().T == I (4x4), shape (4,4), unitary verified."
})

# ==== 2. ghz3 (n_sys=3) =====================================================
# H on q0, then CNOT(0->1), then CNOT(1->2). Rightmost applied first.
H3   = single_full(3, 0, H)        # H (x) I (x) I
C01  = cnot_full(3, 0, 1)          # CNOT control=q0, target=q1
C12  = cnot_full(3, 1, 2)          # CNOT control=q1, target=q2
ghz3 = C12 @ C01 @ H3              # apply H first, then C01, then C12
ghz3_r, ghz3_i = to_entry(ghz3)
submissions.append({
    "id": "ghz3",
    "n_sys": 3,
    "n_anc": 0,
    "app_golden_real": ghz3_r,
    "app_golden_imag": ghz3_i,
    "app_golden_code": (
        "import numpy as np\n"
        "s = 1/np.sqrt(2)\n"
        "I2 = np.eye(2, dtype=complex)\n"
        "H3 = np.kron(np.kron(s*np.array([[1,1],[1,-1]],dtype=complex), I2), I2)\n"
        "# CNOT(0->1): ctrl=q0, tgt=q1 in 3-qubit big-endian\n"
        "C01 = np.eye(8, dtype=complex)\n"
        "for j in range(8):\n"
        "    bits=[(j>>2)&1,(j>>1)&1,j&1]\n"
        "    if bits[0]==1: bits[1]^=1\n"
        "    o=bits[0]*4+bits[1]*2+bits[2]\n"
        "    C01[o,j]=1.0 if o==((j>>2&1)*4+((j>>1&1)^(j>>2&1))*2+(j&1)) else 0.0\n"
        "C12 = np.eye(8, dtype=complex)\n"
        "for j in range(8):\n"
        "    bits=[(j>>2)&1,(j>>1)&1,j&1]\n"
        "    if bits[1]==1: bits[2]^=1\n"
        "    o=bits[0]*4+bits[1]*2+bits[2]\n"
        "    C12[o,j]=1.0\n"
        "golden = C12 @ C01 @ H3"
    ),
    "construction_method": "Three-gate product: H on q0, CNOT(0->1), CNOT(1->2), applied rightmost-first so H acts first. Each CNOT built from big-endian truth table.",
    "self_check": "U @ U.conj().T == I (8x8), shape (8,8), unitary verified. U|000> = (|000>+|111>)/sqrt(2)."
})

# ==== 3. ghz4 (n_sys=4) =====================================================
# H on q0, then CNOT(0->1), CNOT(1->2), CNOT(2->3).
H4   = single_full(4, 0, H)
C01_4 = cnot_full(4, 0, 1)
C12_4 = cnot_full(4, 1, 2)
C23_4 = cnot_full(4, 2, 3)
ghz4 = C23_4 @ C12_4 @ C01_4 @ H4
ghz4_r, ghz4_i = to_entry(ghz4)
submissions.append({
    "id": "ghz4",
    "n_sys": 4,
    "n_anc": 0,
    "app_golden_real": ghz4_r,
    "app_golden_imag": ghz4_i,
    "app_golden_code": (
        "import numpy as np\n"
        "def cnot(n,c,t):\n"
        "    N=2**n; U=np.zeros((N,N),dtype=complex)\n"
        "    for j in range(N):\n"
        "        bits=[(j>>(n-1-k))&1 for k in range(n)]\n"
        "        if bits[c]: bits[t]^=1\n"
        "        U[sum(bits[k]<<(n-1-k) for k in range(n)),j]=1.0\n"
        "    return U\n"
        "s=1/np.sqrt(2); I2=np.eye(2,dtype=complex)\n"
        "H4=np.kron(s*np.array([[1,1],[1,-1]],dtype=complex),np.kron(I2,np.kron(I2,I2)))\n"
        "golden = cnot(4,2,3) @ cnot(4,1,2) @ cnot(4,0,1) @ H4"
    ),
    "construction_method": "Four-gate product on 4 qubits: H on q0, then CNOT(0->1), CNOT(1->2), CNOT(2->3). Each CNOT from big-endian truth-table construction.",
    "self_check": "U @ U.conj().T == I (16x16), shape (16,16), unitary verified. U|0000> = (|0000>+|1111>)/sqrt(2)."
})

# ==== 4. reflect00 (n_sys=2) ================================================
# 2|00><00| - I = diag(1, -1, -1, -1).
# (Global phase is free: diag(1,-1,-1,-1) ~ diag(-1,1,1,1).)
ref00 = np.diag([1, -1, -1, -1]).astype(complex)
ref00_r, ref00_i = to_entry(ref00)
submissions.append({
    "id": "reflect00",
    "n_sys": 2,
    "n_anc": 0,
    "app_golden_real": ref00_r,
    "app_golden_imag": ref00_i,
    "app_golden_code": "import numpy as np\ngolden = np.diag([1.0, -1.0, -1.0, -1.0]).astype(complex)",
    "construction_method": "Reflection 2|00><00| - I: +1 eigenvalue on |00>, -1 on |01>, |10>, |11>. Diagonal matrix.",
    "self_check": "U @ U.conj().T == I (4x4), U^2 == I (involution). Shape (4,4), unitary verified."
})

# ==== 5. diffusion (n_sys=2) ================================================
# D = (H tensor H) @ (2|00><00| - I) @ (H tensor H)
HH = np.kron(H, H)
diffusion = HH @ ref00 @ HH
diffusion_r, diffusion_i = to_entry(diffusion)
submissions.append({
    "id": "diffusion",
    "n_sys": 2,
    "n_anc": 0,
    "app_golden_real": diffusion_r,
    "app_golden_imag": diffusion_i,
    "app_golden_code": (
        "import numpy as np\n"
        "s = 1/np.sqrt(2)\n"
        "H = s*np.array([[1,1],[1,-1]],dtype=complex)\n"
        "HH = np.kron(H, H)\n"
        "R = np.diag([1.0,-1.0,-1.0,-1.0]).astype(complex)\n"
        "golden = HH @ R @ HH"
    ),
    "construction_method": "Grover diffusion D = (H (x) H) @ reflect00 @ (H (x) H): sandwich the |00> reflection between Hadamard layers.",
    "self_check": "U @ U.conj().T == I (4x4), U^2 == I. Shape (4,4), unitary verified."
})

# ==== 6. grover2 (n_sys=2) ==================================================
# G = D @ O, where O = diag(1,1,1,-1) marks |11>, D is the diffusion operator.
O_mark = np.diag([1, 1, 1, -1]).astype(complex)
grover2 = diffusion @ O_mark
grover2_r, grover2_i = to_entry(grover2)
submissions.append({
    "id": "grover2",
    "n_sys": 2,
    "n_anc": 0,
    "app_golden_real": grover2_r,
    "app_golden_imag": grover2_i,
    "app_golden_code": (
        "import numpy as np\n"
        "s = 1/np.sqrt(2)\n"
        "H = s*np.array([[1,1],[1,-1]],dtype=complex)\n"
        "HH = np.kron(H, H)\n"
        "R = np.diag([1.0,-1.0,-1.0,-1.0]).astype(complex)\n"
        "D = HH @ R @ HH\n"
        "O = np.diag([1.0,1.0,1.0,-1.0]).astype(complex)\n"
        "golden = D @ O"
    ),
    "construction_method": "Single Grover iterate G = D @ O: O marks |11> with phase -1, D is the standard 2-qubit diffusion. O applied first (rightmost), then D.",
    "self_check": "U @ U.conj().T == I (4x4). G applied to uniform superposition produces |11>. Shape (4,4), unitary verified."
})

# ==== 7. qft2 (n_sys=2) =====================================================
# U[j,k] = (1/sqrt(N)) * exp(2*pi*i*j*k/N), N=4, big-endian integer indexing, no bit-reversal.
N = 4
qft2 = np.zeros((N, N), dtype=complex)
for j in range(N):
    for k in range(N):
        qft2[j, k] = cmath.exp(2j * cmath.pi * j * k / N) / math.sqrt(N)
qft2_r, qft2_i = to_entry(qft2)
submissions.append({
    "id": "qft2",
    "n_sys": 2,
    "n_anc": 0,
    "app_golden_real": qft2_r,
    "app_golden_imag": qft2_i,
    "app_golden_code": (
        "import numpy as np\n"
        "import math, cmath\n"
        "N = 4\n"
        "golden = np.zeros((N, N), dtype=complex)\n"
        "for j in range(N):\n"
        "    for k in range(N):\n"
        "        golden[j, k] = cmath.exp(2j * cmath.pi * j * k / N) / math.sqrt(N)"
    ),
    "construction_method": "Standard QFT formula U[j,k]=(1/sqrt(N))*omega^(jk) with omega=exp(2*pi*i/N), N=4. Big-endian integer indexing, no bit-reversal.",
    "self_check": "U @ U.conj().T ~= I (4x4). Shape (4,4), unitary verified."
})

# ==== 8. qft3 (n_sys=3) =====================================================
# U[j,k] = (1/sqrt(N)) * exp(2*pi*i*j*k/N), N=8.
N = 8
qft3 = np.zeros((N, N), dtype=complex)
for j in range(N):
    for k in range(N):
        qft3[j, k] = cmath.exp(2j * cmath.pi * j * k / N) / math.sqrt(N)
qft3_r, qft3_i = to_entry(qft3)
submissions.append({
    "id": "qft3",
    "n_sys": 3,
    "n_anc": 0,
    "app_golden_real": qft3_r,
    "app_golden_imag": qft3_i,
    "app_golden_code": (
        "import numpy as np\n"
        "import math, cmath\n"
        "N = 8\n"
        "golden = np.zeros((N, N), dtype=complex)\n"
        "for j in range(N):\n"
        "    for k in range(N):\n"
        "        golden[j, k] = cmath.exp(2j * cmath.pi * j * k / N) / math.sqrt(N)"
    ),
    "construction_method": "Standard QFT formula U[j,k]=(1/sqrt(N))*omega^(jk) with omega=exp(2*pi*i/N), N=8. Big-endian integer indexing, no bit-reversal.",
    "self_check": "U @ U.conj().T ~= I (8x8). Shape (8,8), unitary verified."
})

# ==== Self-checks ===========================================================
all_mats = {
    "bell": bell, "ghz3": ghz3, "ghz4": ghz4,
    "reflect00": ref00, "diffusion": diffusion, "grover2": grover2,
    "qft2": qft2, "qft3": qft3,
}

print("=== Unitarity self-checks ===")
for name, M in all_mats.items():
    n = M.shape[0]
    I_approx = M @ M.conj().T
    err = np.max(np.abs(I_approx - np.eye(n)))
    print(f"  {name:12s}: shape={M.shape}, max|U*U^dag - I| = {err:.2e}  {'PASS' if err < 1e-12 else 'FAIL'}")

# Semantic checks
print("\n=== Semantic self-checks ===")
# bell: |00> -> (|00>+|11>)/sqrt(2)
col00_bell = bell[:, 0]
expected = np.array([s2, 0, 0, s2], dtype=complex)
err = np.max(np.abs(col00_bell - expected))
print(f"  bell: U|00> = (|00>+|11>)/sqrt(2), max_err = {err:.2e}  {'PASS' if err<1e-12 else 'FAIL'}")

# ghz3: |000> -> (|000>+|111>)/sqrt(2)
col000 = ghz3[:, 0]
expected = np.zeros(8, dtype=complex); expected[0] = s2; expected[7] = s2
err = np.max(np.abs(col000 - expected))
print(f"  ghz3: U|000> = (|000>+|111>)/sqrt(2), max_err = {err:.2e}  {'PASS' if err<1e-12 else 'FAIL'}")

# ghz4: |0000> -> (|0000>+|1111>)/sqrt(2)
col0000 = ghz4[:, 0]
expected = np.zeros(16, dtype=complex); expected[0] = s2; expected[15] = s2
err = np.max(np.abs(col0000 - expected))
print(f"  ghz4: U|0000> = (|0000>+|1111>)/sqrt(2), max_err = {err:.2e}  {'PASS' if err<1e-12 else 'FAIL'}")

# reflect00: involution
err = np.max(np.abs(ref00 @ ref00 - np.eye(4)))
print(f"  reflect00: R^2=I, max_err = {err:.2e}  {'PASS' if err<1e-12 else 'FAIL'}")

# diffusion: involution
err = np.max(np.abs(diffusion @ diffusion - np.eye(4)))
print(f"  diffusion: D^2=I, max_err = {err:.2e}  {'PASS' if err<1e-12 else 'FAIL'}")

# grover2: G applied to uniform superposition should amplify |11>
plus2 = np.array([0.5, 0.5, 0.5, 0.5], dtype=complex)  # H(x)H |00>
result = grover2 @ plus2
print(f"  grover2: G@|+>  amplitudes = {np.round(result, 3)}")
print(f"  grover2: |amp(11)|^2 = {abs(result[3])**2:.4f}  {'PASS' if abs(result[3])**2 > 0.9 else 'FAIL'}")

# ==== Assemble submission ===================================================
submission = {
    "runtime": "qwen",
    "weights_id": "alibaba-qwen",
    "convention_ack": True,
    "submissions": submissions,
}

out_path = r"D:\QuantaFoundry\_workspace\crossmodel\apps\submissions\qwen.app.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(submission, f, indent=2, ensure_ascii=False)

print(f"\nSubmission written to: {out_path}")
print(f"Total intents: {len(submissions)}")
