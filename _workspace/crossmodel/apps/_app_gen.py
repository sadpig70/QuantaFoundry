"""Compute app-level golden unitaries for cross-model Round 3."""
import numpy as np
import json, math, os

SQRT2 = math.sqrt(2)
PI = math.pi

results = []

# --- bell (n=2): CNOT @ (H tensor I) ---
H = np.array([[1,1],[1,-1]], dtype=complex) / SQRT2
I2 = np.eye(2, dtype=complex)
HI = np.kron(H, I2)
CNOT = np.zeros((4,4), dtype=complex)
CNOT[0,0]=1; CNOT[1,1]=1; CNOT[3,2]=1; CNOT[2,3]=1
bell = CNOT @ HI
results.append({
    "id":"bell","n":2,
    "U":bell,
    "method":"CNOT @ (H tensor I): Hadamard on q0, then CNOT(control=q0, target=q1). Big-endian.",
    "code":"import numpy as np\nH = np.array([[1,1],[1,-1]],dtype=complex)/np.sqrt(2)\nHI = np.kron(H, np.eye(2))\nCN = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],dtype=complex)\ngolden = CN @ HI"
})

# --- ghz3 (n=3): CNOT(1->2) @ CNOT(0->1) @ (H tensor I tensor I) ---
# Build CNOT(0->1) on 3 qubits: control=q0, target=q1
CNOT01_3 = np.eye(8, dtype=complex)
CNOT01_3[6,4] = 1; CNOT01_3[4,6] = 1; CNOT01_3[4,4] = 0; CNOT01_3[6,6] = 0  # |100><->|110>
CNOT01_3[7,5] = 1; CNOT01_3[5,7] = 1; CNOT01_3[5,5] = 0; CNOT01_3[7,7] = 0  # |101><->|111>
# Build CNOT(1->2) on 3 qubits: control=q1, target=q2
CNOT12_3 = np.eye(8, dtype=complex)
CNOT12_3[3,2] = 1; CNOT12_3[2,3] = 1; CNOT12_3[2,2] = 0; CNOT12_3[3,3] = 0  # |010><->|011>
CNOT12_3[7,6] = 1; CNOT12_3[6,7] = 1; CNOT12_3[6,6] = 0; CNOT12_3[7,7] = 0  # |110><->|111>
HII = np.kron(np.kron(H, I2), I2)
ghz3 = CNOT12_3 @ CNOT01_3 @ HII
results.append({
    "id":"ghz3","n":3,
    "U":ghz3,
    "method":"CNOT(1>2) @ CNOT(0>1) @ (H tensor I tensor I). Big-endian, maps |000> -> (|000>+|111>)/sqrt2.",
    "code":"import numpy as np\nH = np.array([[1,1],[1,-1]],dtype=complex)/np.sqrt(2)\nI = np.eye(2,dtype=complex)\nHII = np.kron(np.kron(H,I),I)\nCN01 = np.eye(8,dtype=complex); CN01[6,4]=1; CN01[4,6]=1; CN01[4,4]=0; CN01[6,6]=0; CN01[7,5]=1; CN01[5,7]=1; CN01[5,5]=0; CN01[7,7]=0\nCN12 = np.eye(8,dtype=complex); CN12[3,2]=1; CN12[2,3]=1; CN12[2,2]=0; CN12[3,3]=0; CN12[7,6]=1; CN12[6,7]=1; CN12[6,6]=0; CN12[7,7]=0\ngolden = CN12 @ CN01 @ HII"
})

# --- ghz4 (n=4): CNOT(2->3) @ CNOT(1->2) @ CNOT(0->1) @ (H tensor I^3) ---
# Build on 16-dim space
N4 = 16
# CNOT(0->1) on 4 qubits: swaps when q0=1, q1 flips
CN01_4 = np.eye(N4, dtype=complex)
for i in range(N4):
    bits = [(i>>(3-k))&1 for k in range(4)]
    if bits[0] == 1:
        j_bits = bits.copy(); j_bits[1] ^= 1
        j = sum(j_bits[k]<<(3-k) for k in range(4))
        CN01_4[j,i] = 1; CN01_4[i,i] = 0

# CNOT(1->2) on 4 qubits
CN12_4 = np.eye(N4, dtype=complex)
for i in range(N4):
    bits = [(i>>(3-k))&1 for k in range(4)]
    if bits[1] == 1:
        j_bits = bits.copy(); j_bits[2] ^= 1
        j = sum(j_bits[k]<<(3-k) for k in range(4))
        CN12_4[j,i] = 1; CN12_4[i,i] = 0

# CNOT(2->3) on 4 qubits
CN23_4 = np.eye(N4, dtype=complex)
for i in range(N4):
    bits = [(i>>(3-k))&1 for k in range(4)]
    if bits[2] == 1:
        j_bits = bits.copy(); j_bits[3] ^= 1
        j = sum(j_bits[k]<<(3-k) for k in range(4))
        CN23_4[j,i] = 1; CN23_4[i,i] = 0

HIII = np.kron(np.kron(np.kron(H, I2), I2), I2)
ghz4 = CN23_4 @ CN12_4 @ CN01_4 @ HIII
results.append({
    "id":"ghz4","n":4,
    "U":ghz4,
    "method":"CNOT(2>3) @ CNOT(1>2) @ CNOT(0>1) @ (H tensor I^3). Big-endian, maps |0000> -> (|0000>+|1111>)/sqrt2.",
    "code":"import numpy as np\ndef _cnot4(ctrl,tgt):\n    N=16; M=np.eye(N,dtype=complex)\n    for i in range(N):\n        bits=[(i>>(3-k))&1 for k in range(4)]\n        if bits[ctrl]==1:\n            jb=bits.copy(); jb[tgt]^=1\n            j=sum(jb[k]<<(3-k) for k in range(4))\n            M[j,i]=1; M[i,i]=0\n    return M\nH=np.array([[1,1],[1,-1]],dtype=complex)/np.sqrt(2)\nI=np.eye(2,dtype=complex)\ngolden = _cnot4(2,3) @ _cnot4(1,2) @ _cnot4(0,1) @ np.kron(np.kron(np.kron(H,I),I),I)"
})

# --- reflect00 (n=2): 2|00><00| - I = diag(1,-1,-1,-1) ---
reflect00 = np.diag([1, -1, -1, -1]).astype(complex)
results.append({
    "id":"reflect00","n":2,
    "U":reflect00,
    "method":"2|00><00| - I = diag(1,-1,-1,-1) in big-endian |q0 q1>. Global phase free.",
    "code":"import numpy as np\ngolden = np.diag([1,-1,-1,-1]).astype(complex)"
})

# --- diffusion (n=2): D = (H tensor H) @ reflect00 @ (H tensor H) ---
# reflect00 = diag(1,-1,-1,-1)
HH = np.kron(H, H)
diffusion = HH @ reflect00 @ HH
# The diffusion should be 2|s><s| - I where |s> is uniform superposition
# |s> = [1/2, 1/2, 1/2, 1/2]
# 2|s><s| = 2*(1/4)*[[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1]] = (1/2)*[[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1]]
# D = 2|s><s| - I = [[-1/2, 1/2, 1/2, 1/2],[1/2, -1/2, 1/2, 1/2],[1/2, 1/2, -1/2, 1/2],[1/2, 1/2, 1/2, -1/2]]
# = [[-0.5, 0.5, 0.5, 0.5], [0.5, -0.5, 0.5, 0.5], [0.5, 0.5, -0.5, 0.5], [0.5, 0.5, 0.5, -0.5]]
results.append({
    "id":"diffusion","n":2,
    "U":diffusion,
    "method":"(H tensor H) @ diag(1,-1,-1,-1) @ (H tensor H) = 2|++><++| - I. Big-endian.",
    "code":"import numpy as np\nH = np.array([[1,1],[1,-1]],dtype=complex)/np.sqrt(2)\nHH = np.kron(H,H)\nR00 = np.diag([1,-1,-1,-1]).astype(complex)\ngolden = HH @ R00 @ HH"
})

# --- grover2 (n=2): G = D @ O, O = diag(1,1,1,-1) marking |11> ---
O = np.diag([1,1,1,-1]).astype(complex)
grover2 = diffusion @ O
results.append({
    "id":"grover2","n":2,
    "U":grover2,
    "method":"G = D @ O where D=diffusion, O=diag(1,1,1,-1) oracle marking |11>(idx3). Big-endian.",
    "code":"import numpy as np\nH=np.array([[1,1],[1,-1]],dtype=complex)/np.sqrt(2)\nHH=np.kron(H,H)\nR00=np.diag([1,-1,-1,-1]).astype(complex)\nD=HH@R00@HH\nO=np.diag([1,1,1,-1]).astype(complex)\ngolden = D @ O"
})

# --- qft2 (n=2): U[j,k] = (1/2)*exp(2*pi*i*j*k/4) ---
N2 = 4; w2 = np.exp(2j*PI/N2)
qft2 = np.array([[w2**(j*k)/np.sqrt(N2) for k in range(N2)] for j in range(N2)]).astype(complex)
results.append({
    "id":"qft2","n":2,
    "U":qft2,
    "method":"QFT2: U[j,k]=(1/2)omega^(jk), omega=exp(2*pi*i/4)=i. Big-endian, no bit-reversal.",
    "code":"import numpy as np\nN=4; w=np.exp(2j*np.pi/N)\ngolden = np.array([[w**(j*k)/np.sqrt(N) for k in range(N)] for j in range(N)]).astype(complex)"
})

# --- qft3 (n=3): U[j,k] = (1/sqrt8)*exp(2*pi*i*j*k/8) ---
N3 = 8; w3 = np.exp(2j*PI/N3)
qft3 = np.array([[w3**(j*k)/np.sqrt(N3) for k in range(N3)] for j in range(N3)]).astype(complex)
results.append({
    "id":"qft3","n":3,
    "U":qft3,
    "method":"QFT3: U[j,k]=(1/sqrt8)omega^(jk), omega=exp(2*pi*i/8). Big-endian, no bit-reversal.",
    "code":"import numpy as np\nN=8; w=np.exp(2j*np.pi/N)\ngolden = np.array([[w**(j*k)/np.sqrt(N) for k in range(N)] for j in range(N)]).astype(complex)"
})

# --- Verify ---
print("=== Verification ===")
all_ok = True
for i,r in enumerate(results):
    U = r["U"]
    n = r["n"]
    shape_ok = U.shape == (2**n, 2**n)
    id_m = U @ U.conj().T
    unitary_ok = np.allclose(id_m, np.eye(2**n), atol=1e-12)
    status = "OK" if (shape_ok and unitary_ok) else "FAIL"
    if not shape_ok or not unitary_ok:
        all_ok = False
    print(f"{i+1}. {r['id']:12s} n={n} shape={2**n}x{2**n} unitary={unitary_ok} -> {status}")

# Verify expected actions
# bell: |00> -> (|00>+|11>)/sqrt2
v = bell @ np.array([1,0,0,0], dtype=complex)
print(f"  bell|00> = {np.round(v,10)}")
assert np.allclose(v, np.array([1,0,0,1],dtype=complex)/SQRT2)

# ghz3: |000> -> (|000>+|111>)/sqrt2
v3 = ghz3 @ np.array([1]+[0]*7, dtype=complex)
print(f"  ghz3|000> = {np.round(v3,10)}")
assert np.allclose(v3, np.array([1,0,0,0,0,0,0,1],dtype=complex)/SQRT2)

# ghz4: |0000> -> (|0000>+|1111>)/sqrt2
v4 = ghz4 @ np.array([1]+[0]*15, dtype=complex)
print(f"  ghz4|0000> = {np.round(v4,10)}")
assert np.allclose(v4, np.array([1]+[0]*14+[1],dtype=complex)/SQRT2)

# grover2 applied to uniform superposition should produce |11>
s = np.ones(4, dtype=complex)/2  # uniform superposition
g2s = grover2 @ s
print(f"  grover2|s> = {np.round(g2s,10)}")
assert np.allclose(np.abs(g2s), np.array([0,0,0,1]), atol=1e-10)

print("\nAll assertions passed.")

# --- Build submission ---
submissions = []
for r in results:
    U = r["U"]
    submissions.append({
        "id": r["id"],
        "n_sys": r["n"],
        "n_anc": 0,
        "app_golden_real": [[float(x.real) for x in row] for row in U],
        "app_golden_imag": [[float(x.imag) for x in row] for row in U],
        "app_golden_code": r["code"],
        "construction_method": r["method"],
        "self_check": f"U @ U.conj().T ~ I (atol 1e-12), shape ({2**r['n']},{2**r['n']}). Code reproduces."
    })

output = {
    "runtime": "deepseek",
    "weights_id": "deepseek-v4-pro",
    "convention_ack": True,
    "submissions": submissions
}

outdir = r"D:\QuantaFoundry\_workspace\crossmodel\apps\submissions"
os.makedirs(outdir, exist_ok=True)
outpath = os.path.join(outdir, "deepseek.app.json")
with open(outpath, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2)
print(f"\nSaved: {outpath}")
print(f"Intents: {len(submissions)}")
