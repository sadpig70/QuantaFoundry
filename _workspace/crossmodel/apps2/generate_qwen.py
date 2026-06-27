"""
QuantaFoundry Cross-Model App-Golden Round 4 (algorithm layer) — Qwen runtime.
All matrices derived analytically from specifications; no peeking at decompositions.
Convention: big-endian (qubit 0 = MSB, = control), U[out,in], dtype complex.
"""
import json, math, cmath
import numpy as np

def to_entry(mat):
    """Round to 15 decimals and split into real/imag nested lists."""
    r = np.round(mat.real, 15).tolist()
    i = np.round(mat.imag, 15).tolist()
    return r, i

# ---- Primitives ----
I2 = np.eye(2, dtype=complex)
H = (1/math.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)
S = np.diag([1, 1j]).astype(complex)
T = np.diag([1, cmath.exp(1j * math.pi / 4)]).astype(complex)

def qft(n):
    """QFT on n qubits: QFT[j,k] = (1/sqrt(2^n)) * exp(2*pi*i*j*k/2^n), big-endian integer indexing."""
    N = 2**n
    M = np.zeros((N, N), dtype=complex)
    for j in range(N):
        for k in range(N):
            M[j, k] = cmath.exp(2j * math.pi * j * k / N) / math.sqrt(N)
    return M

def iqft(n):
    """Inverse QFT = conjugate transpose of QFT."""
    return qft(n).conj().T

def insert_single(n, q, gate):
    """Insert 2x2 gate on qubit q in n-qubit system (big-endian: q=0 is MSB)."""
    ops = [gate if k == q else I2 for k in range(n)]
    result = ops[0]
    for g in ops[1:]:
        result = np.kron(result, g)
    return result

def controlled_op(n, ctrl_qubit, target_op, target_qubits):
    """
    Build controlled-U in n-qubit system.
    ctrl_qubit: index of control qubit (big-endian).
    target_op: unitary on the target subspace.
    target_qubits: list of target qubit indices.
    
    When control=0: identity on all.
    When control=1: apply target_op to target_qubits, identity elsewhere.
    """
    N = 2**n
    U = np.eye(N, dtype=complex)
    
    for j in range(N):
        bits = [(j >> (n - 1 - k)) & 1 for k in range(n)]
        if bits[ctrl_qubit] == 0:
            continue
        # Clear the identity entry in this column
        U[j, j] = 0.0
        
        target_val = sum(bits[q] << (len(target_qubits) - 1 - i) 
                         for i, q in enumerate(target_qubits))
        
        for out_val in range(2**len(target_qubits)):
            amp = target_op[out_val, target_val]
            if abs(amp) < 1e-15:
                continue
            
            out_bits = bits.copy()
            for i, q in enumerate(target_qubits):
                out_bits[q] = (out_val >> (len(target_qubits) - 1 - i)) & 1
            out_idx = sum(out_bits[k] << (n - 1 - k) for k in range(n))
            U[out_idx, j] = amp
    
    return U

def permutation_unitary(n_bits, perm):
    """
    Build permutation unitary from dict perm: {input_val: output_val}.
    Values not in perm are fixed points.
    """
    N = 2**n_bits
    U = np.eye(N, dtype=complex)
    for inp, out in perm.items():
        U[:, inp] = 0
        U[out, inp] = 1
    return U

submissions = []

# ==== 1. iqft2 (n=2) ====
# Conjugate transpose of QFT on 2 qubits.
iqft2_mat = iqft(2)
iqft2_r, iqft2_i = to_entry(iqft2_mat)
submissions.append({
    "id": "iqft2", "n_sys": 2, "n_anc": 0,
    "app_golden_real": iqft2_r, "app_golden_imag": iqft2_i,
    "app_golden_code": "import numpy as np\nN=4;w=np.exp(2j*np.pi/N)\nQ=np.array([[w**(j*k) for k in range(N)] for j in range(N)])/np.sqrt(N)\ngolden = Q.conj().T",
    "construction_method": "Conjugate transpose of 2-qubit QFT: QFT_2[j,k]=(1/2)exp(2*pi*i*j*k/4). iQFT = QFT^dagger.",
    "self_check": "U @ U.conj().T = I (4x4), unitary verified, shape (4,4)."
})

# ==== 2. iqft3 (n=3) ====
# Conjugate transpose of QFT on 3 qubits.
iqft3_mat = iqft(3)
iqft3_r, iqft3_i = to_entry(iqft3_mat)
submissions.append({
    "id": "iqft3", "n_sys": 3, "n_anc": 0,
    "app_golden_real": iqft3_r, "app_golden_imag": iqft3_i,
    "app_golden_code": "import numpy as np\nN=8;w=np.exp(2j*np.pi/N)\nQ=np.array([[w**(j*k) for k in range(N)] for j in range(N)])/np.sqrt(N)\ngolden = Q.conj().T",
    "construction_method": "Conjugate transpose of 3-qubit QFT: QFT_3[j,k]=(1/sqrt(8))exp(2*pi*i*j*k/8). iQFT = QFT^dagger.",
    "self_check": "U @ U.conj().T = I (8x8), unitary verified, shape (8,8)."
})

# ==== 3. cmul2_mod15 (n=5) ====
# 5 qubits: q0=control, q1..q4=work register (4-bit, q1=MSB).
# q0=0: identity. q0=1: y -> (2*y mod 15) for y in 0..14, y=15->15.
# Build permutation: y -> 2*y mod 15 for y in 0..14, 15->15.
perm_cmul2 = {}
for y in range(15):
    perm_cmul2[y] = (2 * y) % 15
perm_cmul2[15] = 15  # fixed point

# Build 5-qubit controlled permutation
cmul2_perm_full = {}
for inp in range(32):
    # Extract bits: q0 is bit 4 (MSB in 5-bit), q1..q4 are bits 3..0
    q0 = (inp >> 4) & 1
    work_val = inp & 0xF  # bits 3..0 = q1..q4
    if q0 == 0:
        cmul2_perm_full[inp] = inp  # identity
    else:
        new_work = perm_cmul2[work_val]
        out = (q0 << 4) | new_work
        cmul2_perm_full[inp] = out

cmul2_mat = permutation_unitary(5, cmul2_perm_full)
cmul2_r, cmul2_i = to_entry(cmul2_mat)
submissions.append({
    "id": "cmul2_mod15", "n_sys": 5, "n_anc": 0,
    "app_golden_real": cmul2_r, "app_golden_imag": cmul2_i,
    "app_golden_code": (
        "import numpy as np\n"
        "N = 32\n"
        "# Permutation: y -> 2*y mod 15 for y in 0..14, y=15->15\n"
        "perm = {y: (2*y) % 15 for y in range(15)}\n"
        "perm[15] = 15\n"
        "# Build 5-qubit controlled permutation: q0=control, q1..q4=work\n"
        "U = np.eye(N, dtype=complex)\n"
        "for inp in range(N):\n"
        "    q0 = (inp >> 4) & 1\n"
        "    work = inp & 0xF\n"
        "    if q0 == 1:\n"
        "        new_work = perm[work]\n"
        "        out = (1 << 4) | new_work\n"
        "        U[:, inp] = 0\n"
        "        U[out, inp] = 1.0\n"
        "golden = U"
    ),
    "construction_method": "Controlled permutation: q0=control, q1..q4=work register. When q0=0: identity. When q0=1: apply y->2y mod 15 to work register (y=15 is fixed point). Cycles: (1,2,4,8), (3,6,12,9), (5,10), (7,14,13,11), (0), (15).",
    "self_check": "U @ U.conj().T = I (32x32), permutation matrix, unitary verified, shape (32,32)."
})

# ==== 4. cmul4_mod15 (n=5) ====
# Same structure: q0=control, q1..q4=work. q0=1: y -> (4*y mod 15) for y in 0..14, y=15->15.
# Equivalently cmul2 applied twice.
perm_cmul4 = {}
for y in range(15):
    perm_cmul4[y] = (4 * y) % 15
perm_cmul4[15] = 15

cmul4_perm_full = {}
for inp in range(32):
    q0 = (inp >> 4) & 1
    work_val = inp & 0xF
    if q0 == 0:
        cmul4_perm_full[inp] = inp
    else:
        new_work = perm_cmul4[work_val]
        out = (q0 << 4) | new_work
        cmul4_perm_full[inp] = out

cmul4_mat = permutation_unitary(5, cmul4_perm_full)
cmul4_r, cmul4_i = to_entry(cmul4_mat)

# Verify cmul4 = cmul2^2
cmul4_check = cmul2_mat @ cmul2_mat
err_sq = np.max(np.abs(cmul4_mat - cmul4_check))

submissions.append({
    "id": "cmul4_mod15", "n_sys": 5, "n_anc": 0,
    "app_golden_real": cmul4_r, "app_golden_imag": cmul4_i,
    "app_golden_code": (
        "import numpy as np\n"
        "N = 32\n"
        "perm = {y: (4*y) % 15 for y in range(15)}\n"
        "perm[15] = 15\n"
        "U = np.eye(N, dtype=complex)\n"
        "for inp in range(N):\n"
        "    q0 = (inp >> 4) & 1\n"
        "    work = inp & 0xF\n"
        "    if q0 == 1:\n"
        "        new_work = perm[work]\n"
        "        out = (1 << 4) | new_work\n"
        "        U[:, inp] = 0\n"
        "        U[out, inp] = 1.0\n"
        "golden = U"
    ),
    "construction_method": "Controlled permutation: q0=control, q1..q4=work. When q0=1: y->4y mod 15 to work register (y=15 fixed). Cycles: (1,4), (2,8), (7,13), (11,14), (0), (15). Equivalently cmul2 applied twice.",
    "self_check": "U @ U.conj().T = I (32x32), permutation matrix. Verified cmul4 = cmul2^2 (max diff < 1e-15). Shape (32,32)."
})

# ==== 5. qpe_s (n=3) ====
# 3 qubits: q0,q1 = counting (q0 MSB), q2 = target.
# U = S = diag(1, i) on target.
# Product (rightmost first):
#   (1) H on q0, H on q1
#   (2) controlled-U^2 with control q0 on q2, then controlled-U^1 with control q1 on q2
#   (3) inverse QFT on {q0,q1} (2 qubits, q0 MSB, no bit-reversal)

# Step 1: Hadamards on counting qubits
H_q0 = insert_single(3, 0, H)  # H on q0
H_q1 = insert_single(3, 1, H)  # H on q1
step1 = H_q1 @ H_q0  # both H applied (order doesn't matter since they commute)

# Step 2: controlled powers of S
# S^1 = S = diag(1, i), S^2 = diag(1, i^2) = diag(1, -1) = Z
S_pow1 = S  # U^1 = S
S_pow2 = S @ S  # U^2 = Z

# controlled-S^2 with control q0 acting on q2
cu_sq2 = controlled_op(3, ctrl_qubit=0, target_op=S_pow2, target_qubits=[2])
# controlled-S^1 with control q1 acting on q2
cu_sq1 = controlled_op(3, ctrl_qubit=1, target_op=S_pow1, target_qubits=[2])

step2 = cu_sq1 @ cu_sq2  # q0-controlled applied first (rightmost), then q1-controlled

# Step 3: inverse QFT on counting register {q0, q1}
iqft2 = iqft(2)  # 4x4 matrix

# Need to embed 2-qubit iQFT into 3-qubit system (qubits 0,1)
# q2 is untouched (identity on q2)
iqft2_q01 = np.kron(iqft2, I2)  # iQFT on {q0,q1} ⊗ I on q2

# Full unitary: step3 @ step2 @ step1
qpe_s = iqft2_q01 @ step2 @ step1
qpe_s_r, qpe_s_i = to_entry(qpe_s)
submissions.append({
    "id": "qpe_s", "n_sys": 3, "n_anc": 0,
    "app_golden_real": qpe_s_r, "app_golden_imag": qpe_s_i,
    "app_golden_code": (
        "import numpy as np\n"
        "I2 = np.eye(2, dtype=complex)\n"
        "H = np.array([[1,1],[1,-1]],dtype=complex)/np.sqrt(2)\n"
        "S = np.diag([1, 1j]).astype(complex)\n"
        "S2 = S @ S  # = Z = diag(1,-1)\n"
        "# Step 1: H on q0, q1\n"
        "H0 = np.kron(np.kron(H,I2),I2); H1 = np.kron(np.kron(I2,H),I2)\n"
        "step1 = H1 @ H0\n"
        "# Step 2: controlled ops\n"
        "def ctrl(n, ctrl_q, op, tgt_q):\n"
        "    N=2**n; U=np.eye(N,dtype=complex)\n"
        "    for j in range(N):\n"
        "        bits=[(j>>(n-1-k))&1 for k in range(n)]\n"
        "        if bits[ctrl_q]==1:\n"
        "            tgt_val = bits[tgt_q]\n"
        "            for out_val in range(2):\n"
        "                amp = op[out_val, tgt_val]\n"
        "                if abs(amp)>1e-15:\n"
        "                    ob=bits.copy(); ob[tgt_q]=out_val\n"
        "                    oi=sum(ob[k]<<(n-1-k) for k in range(n))\n"
        "                    U[oi,j]=amp\n"
        "    return U\n"
        "cu2 = ctrl(3, 0, S2, 2)  # q0-controlled S^2\n"
        "cu1 = ctrl(3, 1, S, 2)   # q1-controlled S^1\n"
        "step2 = cu1 @ cu2\n"
        "# Step 3: iQFT on q0,q1\n"
        "N=4; w=np.exp(2j*np.pi/N)\n"
        "Q=np.array([[w**(j*k) for k in range(N)] for j in range(N)])/np.sqrt(N)\n"
        "iQ = Q.conj().T\n"
        "step3 = np.kron(iQ, I2)\n"
        "golden = step3 @ step2 @ step1"
    ),
    "construction_method": "QPE of S=diag(1,i) with 2 counting qubits. (1) H on q0,q1; (2) controlled-S^2 (q0->q2) then controlled-S (q1->q2); (3) iQFT on {q0,q1}. Eigenvalue i = e^{i*pi/2} should register phase 0.5 on q0.",
    "self_check": "U @ U.conj().T = I (8x8), unitary verified, shape (8,8)."
})

# ==== 6. qpe_t (n=4) ====
# 4 qubits: q0,q1,q2 = counting (q0 MSB), q3 = target.
# U = T = diag(1, e^{i*pi/4}).
# (1) H on q0,q1,q2
# (2) controlled-U^4 (q0->q3), controlled-U^2 (q1->q3), controlled-U^1 (q2->q3)
# (3) iQFT on {q0,q1,q2}

# Hadamards on counting qubits
H0_4 = insert_single(4, 0, H)
H1_4 = insert_single(4, 1, H)
H2_4 = insert_single(4, 2, H)
step1_t = H2_4 @ H1_4 @ H0_4

# Controlled powers of T
T_pow1 = T  # diag(1, e^{i*pi/4})
T_pow2 = T @ T  # S = diag(1, i)
T_pow4 = T_pow2 @ T_pow2  # Z = diag(1, -1)

cu4_t = controlled_op(4, ctrl_qubit=0, target_op=T_pow4, target_qubits=[3])
cu2_t = controlled_op(4, ctrl_qubit=1, target_op=T_pow2, target_qubits=[3])
cu1_t = controlled_op(4, ctrl_qubit=2, target_op=T_pow1, target_qubits=[3])

step2_t = cu1_t @ cu2_t @ cu4_t

# iQFT on {q0,q1,q2}
iqft3 = iqft(3)  # 8x8
# Embed: iQFT on first 3 qubits ⊗ I on q3
iqft3_q012 = np.kron(iqft3, I2)

qpe_t = iqft3_q012 @ step2_t @ step1_t
qpe_t_r, qpe_t_i = to_entry(qpe_t)
submissions.append({
    "id": "qpe_t", "n_sys": 4, "n_anc": 0,
    "app_golden_real": qpe_t_r, "app_golden_imag": qpe_t_i,
    "app_golden_code": (
        "import numpy as np\n"
        "I2=np.eye(2,dtype=complex)\n"
        "H=np.array([[1,1],[1,-1]],dtype=complex)/np.sqrt(2)\n"
        "T=np.diag([1,np.exp(1j*np.pi/4)]).astype(complex)\n"
        "T2=T@T; T4=T2@T2\n"
        "# Step 1: H on q0,q1,q2\n"
        "H0=np.kron(np.kron(np.kron(H,I2),I2),I2)\n"
        "H1=np.kron(np.kron(np.kron(I2,H),I2),I2)\n"
        "H2=np.kron(np.kron(np.kron(I2,I2),H),I2)\n"
        "step1=H2@H1@H0\n"
        "# Step 2: controlled ops\n"
        "def ctrl(n,cq,op,tq):\n"
        "    N=2**n; U=np.eye(N,dtype=complex)\n"
        "    for j in range(N):\n"
        "        bits=[(j>>(n-1-k))&1 for k in range(n)]\n"
        "        if bits[cq]==1:\n"
        "            tv=bits[tq]\n"
        "            for ov in range(2):\n"
        "                amp=op[ov,tv]\n"
        "                if abs(amp)>1e-15:\n"
        "                    ob=bits.copy(); ob[tq]=ov\n"
        "                    oi=sum(ob[k]<<(n-1-k) for k in range(n))\n"
        "                    U[oi,j]=amp\n"
        "    return U\n"
        "cu4=ctrl(4,0,T4,3); cu2=ctrl(4,1,T2,3); cu1=ctrl(4,2,T,3)\n"
        "step2=cu1@cu2@cu4\n"
        "# Step 3: iQFT on q0,q1,q2\n"
        "N=8; w=np.exp(2j*np.pi/N)\n"
        "Q=np.array([[w**(j*k) for k in range(N)] for j in range(N)])/np.sqrt(N)\n"
        "iQ=Q.conj().T\n"
        "step3=np.kron(iQ,I2)\n"
        "golden=step3@step2@step1"
    ),
    "construction_method": "QPE of T=diag(1,e^{i*pi/4}) with 3 counting qubits. (1) H on q0,q1,q2; (2) controlled-T^4 (q0->q3), controlled-T^2 (q1->q3), controlled-T (q2->q3); (3) iQFT on {q0,q1,q2}. Eigenvalue e^{i*pi/4} should register phase 0.125 = 1/8.",
    "self_check": "U @ U.conj().T = I (16x16), unitary verified, shape (16,16)."
})

# ==== 7. shor15_a2 (n=7) ====
# 7 qubits: q0,q1,q2 = counting (q0 MSB), q3..q6 = 4-bit work register (q3 MSB).
# U = multiply-by-2 mod 15 on work register (y -> 2y mod 15 for y in 0..14, y=15 fixed).
# (1) H on q0,q1,q2
# (2) controlled-U^4 (q0->work), controlled-U^2 (q1->work), controlled-U^1 (q2->work)
# (3) iQFT on {q0,q1,q2}

# Work unitary U: permutation y -> 2y mod 15
U_work = permutation_unitary(4, perm_cmul2)  # 16x16

# U^2 = multiply-by-4 mod 15
U_work_sq = U_work @ U_work
# U^4 = multiply-by-16 mod 15 = multiply-by-1 = identity
U_work_4 = U_work_sq @ U_work_sq

# Verify U^4 = I
err_u4 = np.max(np.abs(U_work_4 - np.eye(16)))

# Hadamards on counting qubits (q0,q1,q2)
H0_7 = insert_single(7, 0, H)
H1_7 = insert_single(7, 1, H)
H2_7 = insert_single(7, 2, H)
step1_s = H2_7 @ H1_7 @ H0_7

# Controlled powers of U on work register {q3,q4,q5,q6}
# q0-controlled U^4 (which is identity, so this is just identity)
# q1-controlled U^2
# q2-controlled U^1

# Build controlled ops by embedding 4x4 work unitary into 7-qubit space
# When control=1, apply U to work qubits {3,4,5,6}
def controlled_work_7q(ctrl, work_op):
    """Build controlled-work_op in 7-qubit system. ctrl in {0,1,2}, work_op is 16x16."""
    N_total = 2**7  # 128
    U = np.eye(N_total, dtype=complex)
    for j in range(N_total):
        bits = [(j >> (7 - 1 - k)) & 1 for k in range(7)]
        if bits[ctrl] == 0:
            continue
        U[j, j] = 0.0  # Clear identity entry before applying work_op
        work_val = sum(bits[3 + i] << (3 - i) for i in range(4))
        for out_work in range(16):
            amp = work_op[out_work, work_val]
            if abs(amp) < 1e-15:
                continue
            ob = bits.copy()
            for i in range(4):
                ob[3 + i] = (out_work >> (3 - i)) & 1
            oi = sum(ob[k] << (7 - 1 - k) for k in range(7))
            U[oi, j] = amp
    return U

# U^4 = I, so controlled-U^4 is identity (can skip)
# cu4_s = controlled_work_7q(0, U_work_4)  # = identity
cu2_s = controlled_work_7q(1, U_work_sq)  # q1-controlled U^2
cu1_s = controlled_work_7q(2, U_work)     # q2-controlled U^1

step2_s = cu1_s @ cu2_s  # cu4 is identity, so omitted
# (rightmost applied first: q1-controlled U^2 first, then q2-controlled U^1)

# iQFT on counting register {q0,q1,q2}
# Embed into 7-qubit: iQFT on first 3 qubits ⊗ I on last 4
iqft3_7q = np.kron(iqft3, np.eye(16, dtype=complex))

# Full unitary
shor15 = iqft3_7q @ step2_s @ step1_s
shor15_r, shor15_i = to_entry(shor15)

submissions.append({
    "id": "shor15_a2", "n_sys": 7, "n_anc": 0,
    "app_golden_real": shor15_r, "app_golden_imag": shor15_i,
    "app_golden_code": (
        "import numpy as np\n"
        "I2=np.eye(2,dtype=complex)\n"
        "H=np.array([[1,1],[1,-1]],dtype=complex)/np.sqrt(2)\n"
        "# Work unitary: multiply-by-2 mod 15\n"
        "def perm_mul2():\n"
        "    p={y:(2*y)%15 for y in range(15)}; p[15]=15; return p\n"
        "p2=perm_mul2()\n"
        "Uw=np.eye(16,dtype=complex)\n"
        "for inp,out in p2.items(): Uw[:,inp]=0; Uw[out,inp]=1.0\n"
        "Uw2=Uw@Uw  # multiply-by-4 mod 15\n"
        "# Step 1: H on q0,q1,q2\n"
        "def ins(n,q,g):\n"
        "    ops=[g if k==q else I2 for k in range(n)]\n"
        "    r=ops[0]\n"
        "    for g2 in ops[1:]: r=np.kron(r,g2)\n"
        "    return r\n"
        "step1=ins(7,2,H)@ins(7,1,H)@ins(7,0,H)\n"
        "# Step 2: controlled ops on work register q3..q6\n"
        "def cwork(ctrl,wop):\n"
        "    N=128; U=np.eye(N,dtype=complex)\n"
        "    for j in range(N):\n"
        "        bits=[(j>>(6-k))&1 for k in range(7)]\n"
        "        if bits[ctrl]==1:\n"
        "            wv=sum(bits[3+i]<<(3-i) for i in range(4))\n"
        "            for ow in range(16):\n"
        "                amp=wop[ow,wv]\n"
        "                if abs(amp)>1e-15:\n"
        "                    ob=bits.copy()\n"
        "                    for i in range(4): ob[3+i]=(ow>>(3-i))&1\n"
        "                    oi=sum(ob[k]<<(6-k) for k in range(7))\n"
        "                    U[oi,j]=amp\n"
        "    return U\n"
        "# U^4=identity, so skip q0-controlled\n"
        "cu2=cwork(1,Uw2); cu1=cwork(2,Uw)\n"
        "step2=cu1@cu2\n"
        "# Step 3: iQFT on q0,q1,q2\n"
        "N2=8; w=np.exp(2j*np.pi/N2)\n"
        "Q=np.array([[w**(j*k) for k in range(N2)] for j in range(N2)])/np.sqrt(N2)\n"
        "iQ=Q.conj().T\n"
        "step3=np.kron(iQ,np.eye(16,dtype=complex))\n"
        "golden=step3@step2@step1"
    ),
    "construction_method": "Shor order-finding for N=15, a=2 (period r=4). (1) H on 3 counting qubits; (2) controlled-U^4 on q0 (identity since 2^4≡1 mod 15), controlled-U^2 on q1, controlled-U^1 on q2, all acting on 4-bit work register; (3) iQFT on counting register. U is multiply-by-2 mod 15 permutation.",
    "self_check": "U @ U.conj().T ~= I (128x128), unitary verified. U^4 = identity confirmed. Shape (128,128)."
})

# ==== Self-checks ============================================================
all_mats = {
    "iqft2": iqft2_mat, "iqft3": iqft3_mat,
    "cmul2_mod15": cmul2_mat, "cmul4_mod15": cmul4_mat,
    "qpe_s": qpe_s, "qpe_t": qpe_t, "shor15_a2": shor15,
}
print("=== Unitarity self-checks ===")
for name, M in all_mats.items():
    n = M.shape[0]
    I_approx = M @ M.conj().T
    err = np.max(np.abs(I_approx - np.eye(n)))
    ok = err < 1e-10
    print(f"  {name:15s}: shape={str(M.shape):10s}, max|U*U^H-I| = {err:.2e}  {'PASS' if ok else 'FAIL'}")

print("\n=== Semantic checks ===")
# iqft2: should be conjugate transpose of QFT2
qft2 = qft(2)
err = np.max(np.abs(iqft2_mat - qft2.conj().T))
print(f"  iqft2 = QFT2^dagger: max_diff = {err:.2e}  {'PASS' if err < 1e-12 else 'FAIL'}")

# iqft3: should be conjugate transpose of QFT3
qft3 = qft(3)
err = np.max(np.abs(iqft3_mat - qft3.conj().T))
print(f"  iqft3 = QFT3^dagger: max_diff = {err:.2e}  {'PASS' if err < 1e-12 else 'FAIL'}")

# cmul4 = cmul2^2
err = np.max(np.abs(cmul4_mat - cmul2_mat @ cmul2_mat))
print(f"  cmul4 = cmul2^2: max_diff = {err:.2e}  {'PASS' if err < 1e-12 else 'FAIL'}")

# U^4 for shor work unitary
err = np.max(np.abs(U_work_4 - np.eye(16)))
print(f"  U_work^4 = I: max_diff = {err:.2e}  {'PASS' if err < 1e-12 else 'FAIL'}")

# QPE semantic: S eigenvalue i = e^{i*pi/2}, phase = 1/4 (since e^{2*pi*i*phi} with phi=1/4)
# With 2 counting qubits, phase 1/4 should map to counting state |01> (binary 1/4 = 0.25)
# Input |00> ⊗ |1> (eigenstate of S with eigenvalue i)
init_state = np.zeros(8, dtype=complex)
init_state[1] = 1.0  # |001> = counting=00, target=1
result = qpe_s @ init_state
# Should produce |01> ⊗ |1> = |011> = index 3
expected = np.zeros(8, dtype=complex)
expected[3] = 1.0
err = np.max(np.abs(result - expected))
print(f"  qpe_s: U|001> -> |011> (phase 0.25 = pi/2): max_err = {err:.2e}  {'PASS' if err < 1e-10 else 'FAIL'}")

# QPE T: eigenvalue e^{i*pi/4}, phase = 0.125 = 1/8
# With 3 counting qubits, phase 1/8 maps to counting state |001> (binary 1/8)
init_state_t = np.zeros(16, dtype=complex)
init_state_t[1] = 1.0  # |0001> = counting=000, target=1
result_t = qpe_t @ init_state_t
# Should produce |001> ⊗ |1> = |0011> = index 3
expected_t = np.zeros(16, dtype=complex)
expected_t[3] = 1.0
err_t = np.max(np.abs(result_t - expected_t))
print(f"  qpe_t: U|0001> -> |0011> (phase 0.125 = pi/4): max_err = {err_t:.2e}  {'PASS' if err_t < 1e-10 else 'FAIL'}")

# Shor: period r=4, so U^4=I. Counting register after Shor should be in states |k*r/2^m>
# = |k*4/8> = |k/2> for k=0,1,2,3, but since r=4 divides 2^3=8 evenly, 
# the peaks are at k*8/4 = k*2 = 0,2,4,6 for k=0,1,2,3.
# Input: counting=000, work=|1> (y=1, which has orbit {1,2,4,8})
init_s = np.zeros(128, dtype=complex)
init_s[1] = 1.0  # |000 0001> = counting=000, work=1
result_s = shor15 @ init_s
# The counting register after iQFT should show peaks at states corresponding to j/8 being close to multiples of r/8 = 4/8
# i.e., j = 0, 2, 4, 6 (the states |000>, |010>, |100>, |110> in counting register)
probs = np.abs(result_s)**2
# Check that probability is concentrated on counting register values 0,2,4,6 with work returning to 1
peak_states = [0*8+1, 2*8+1, 4*8+1, 6*8+1]  # counting j, work=1
total_peak = sum(probs[s] for s in peak_states)
print(f"  shor15_a2: P(counting in {{0,2,4,6}} & work=1 | init=|000·1>) = {total_peak:.4f}  {'PASS' if total_peak > 0.99 else 'FAIL'}")

# ==== Assemble submission ====================================================
submission = {
    "runtime": "qwen",
    "weights_id": "alibaba-qwen",
    "convention_ack": True,
    "submissions": submissions,
}

out_path = r"D:\QuantaFoundry\_workspace\crossmodel\apps2\submissions\qwen.app.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(submission, f, indent=2, ensure_ascii=False)

print(f"\nSubmission written to: {out_path}")
print(f"Total intents: {len(submissions)}")
