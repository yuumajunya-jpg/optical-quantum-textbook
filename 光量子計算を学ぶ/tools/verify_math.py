"""Public-equation checks and didactic examples; not the paper's simulator."""
from pathlib import Path
import math
import numpy as np
from scipy.special import ndtr, logsumexp
from scipy.stats import beta

ROOT = Path(__file__).resolve().parents[1]
rows = []

def record(name, value):
    rows.append((name, str(value)))

def odd_error(v):
    # Positive odd-bin intervals plus their reflected negative counterparts.
    # sf form avoids cancellation for small upper-tail probabilities.
    total = 0.0
    sd = math.sqrt(v)
    a = math.sqrt(math.pi)
    for j in range(40):
        lo, hi = (2*j+.5)*a/sd, (2*j+1.5)*a/sd
        total += 2 * (ndtr(-lo) - ndtr(-hi))
    return total

def llr(z, v):
    a = math.sqrt(math.pi)
    even = np.arange(-40, 41, 2)
    odd = np.arange(-39, 40, 2)
    return logsumexp(-(z-even*a)**2/(2*v))-logsumexp(-(z-odd*a)**2/(2*v))

for s in (12, 12.25, 14, 15.6):
    v = .5 * 10**(-s/10)
    exact = odd_error(v)
    tail = math.erfc(math.sqrt(math.pi)/(2*math.sqrt(2*v)))
    assert 0 <= exact <= tail * (1+1e-12)
    record(f's={s} dB：分散 / 単一座標奇数区画確率', f'{v:.10g} / {exact:.10g}')
for zfrac in (.1, .49):
    record(f'学習例 v=0.1, z={zfrac}√π：厳密格子LLR', f'{llr(zfrac*math.sqrt(math.pi), .1):.9f}')

I = np.eye(2)
X = np.array([[0,1],[1,0]])
Z = np.diag([1,-1])
H = np.array([[1,1],[1,-1]])/math.sqrt(2)
def tensor(*ops):
    out = np.ones((1,1))
    for op in ops:
        out = np.kron(out, op)
    return out
XD, ZD = tensor(X,X,I,I), tensor(Z,I,Z,I)
XG, ZG = tensor(X,I,X,I), tensor(Z,Z,I,I)
SX, SZ = tensor(X,X,X,X), tensor(Z,Z,Z,Z)
for logical in (XD,ZD,XG,ZG):
    assert np.allclose(logical@SX, SX@logical)
    assert np.allclose(logical@SZ, SZ@logical)
assert np.allclose(XD@ZD, -ZD@XD)
assert np.allclose(XG@ZG, -ZG@XG)
for d in (XD,ZD):
    for g in (XG,ZG):
        assert np.allclose(d@g, g@d)
P = np.zeros((16,16))
for k in range(16):
    bits = list(f'{k:04b}')
    bits[1], bits[2] = bits[2], bits[1]
    P[int(''.join(bits),2), k] = 1
H4 = tensor(H,H,H,H)
assert np.allclose(H4@XD@H4.T, ZG)
assert np.allclose(P@XD@P.T, XG)
U = P@H4
assert np.allclose(U@XD@U.T, ZD)
assert np.allclose(U@ZD@U.T, XD)

# Binary Pauli propagation for four index-matched physical CNOTs.
def cx_map(xa,za,xb,zb):
    return xa, za^zb, xa^xb, zb
dx = np.array([1,1,0,0]); dz = np.array([1,0,1,0])
gx = np.array([1,0,1,0]); gz = np.array([1,1,0,0]); zero=np.zeros(4,dtype=int)
for xx, zz in ((dx,dz),(gx,gz)):
    out = cx_map(xx,zero,zero,zero)
    assert np.array_equal(out[0],xx) and np.array_equal(out[2],xx)
    out = cx_map(zero,zero,zero,zz)
    assert np.array_equal(out[1],zz) and np.array_equal(out[3],zz)
record('C4代数、H、SWAP23、横断CNOT写像', '全assert通過')

p = .01
w = [0.,0.]
patterns = [[],[]]
for k in range(16):
    e = [int(c) for c in f'{k:04b}']
    if sum(e)%2 == 0:
        b = e[0]^e[2]
        wt = sum(e)
        w[b] += p**wt*(1-p)**(4-wt)
        patterns[b].append(''.join(map(str,e)))
record('学習用C4 Xのみ p=0.01：P(data X | syndrome=0)', f'{w[1]/sum(w):.10g}')
for b in (0,1):
    record(f'学習用C4：b={b}のパターン', ', '.join(patterns[b]))
for k, n in ((3,1_000_000),(4,1_000_000),(0,15_000),(0,200_000),(0,199_500)):
    cp = beta.ppf(.95,k+1,n-k)
    jeff = beta.ppf(.95,k+.5,n-k+.5)
    record(f'k={k}, n={n}：片側95% CP / Jeffreys', f'{cp:.10g} / {jeff:.10g}')
    if k == 0:
        assert abs(cp - (-math.expm1(math.log(.05)/n))) < 1e-13
assert abs(beta.ppf(.95,4,999997)-7.7536e-6) < 1e-10
assert abs(beta.ppf(.95,5,999996)-9.1535e-6) < 1e-10
record('R3=12×288/0.95；R3/R2', f'{12*288/.95:.10f}；{12/.95:.10f}')
record('q2q3q4q5；逆数', f'{.7*.96:.10f}；{1/(.7*.96):.10f}')
record('追加MN分散 / GKP分散', f'{4*10**(-.2):.10f}')
for L in (2,3,5):
    record(f'L={L}：距離 / ペア数 / 容量16でのバッチ数', f'{2**L} / {4**L} / {math.ceil(4**L/16)}')
R=(3-math.sqrt(5))/2
g=(1-R)/math.sqrt(R)
c=math.sqrt((1-R)/(1+R)); d=math.sqrt(R*(1-R)/(1+R))
B=np.array([[-c,0],[0,d],[d,0],[0,c]])
N=B@np.diag([.02,.03])@B.T
assert abs(g-1)<1e-12
assert abs(N[0,2]+c*d*.02)<1e-12
assert abs(N[1,3]-c*d*.03)<1e-12
assert np.linalg.eigvalsh(N).min()>-1e-12
record('SUM単位ゲインR / 共分散検算', f'{R:.10f} / assert通過')

text = '# 24 数値検算結果\n\n'
text += '同梱 `tools/verify_math.py` の実行結果です。著者のMonte Carloの再現ではなく、公開数式と学習用例の検算です。単一GKP座標の誤り確率を論文の工場出力誤り率と読み替えないでください。\n\n'
text += '| 検算対象 | 結果 |\n|---|---|\n'
text += ''.join('| '+name.replace('|',r'\|')+' | '+value.replace('|',r'\|')+' |\n' for name,value in rows)
text += '\n関連：[[07_GKP誤り確率とアナログ情報]]、[[09_ソフト復号の数式]]、[[17_数値結果と統計的確信]]、[[18_コストと深さと実行時間]]\n'
(ROOT/'24_数値検算結果.md').write_text(text, encoding='utf-8')
print(f'{len(rows)} records; all algebra and numeric assertions passed.')
