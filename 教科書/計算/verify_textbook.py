"""教材の代数・算術の検算。論文の非公開工場シミュレーターではない。"""
from pathlib import Path
import itertools
import json
import math
import re
import sys

import numpy as np
from scipy.special import logsumexp
from scipy.stats import beta, norm

ROOT = Path(__file__).resolve().parents[1]


def odd_probability(variance, limit=12):
    """対称性と生存関数で右半直線の奇数区間を足す。"""
    a, sd = math.sqrt(math.pi), math.sqrt(variance)
    return 2 * sum(norm.sf((2*k + .5)*a/sd) -
                   norm.sf((2*k + 1.5)*a/sd) for k in range(limit))


def wrapped_log_odds(z, variance, limit=30):
    a = math.sqrt(math.pi)
    even = np.arange(-limit, limit+1, 2)
    odd = np.arange(-limit+1, limit, 2)
    return float(logsumexp(-(z-even*a)**2/(2*variance)) -
                 logsumexp(-(z-odd*a)**2/(2*variance)))


def kron_all(matrices):
    result = np.array([[1.]])
    for m in matrices:
        result = np.kron(result, m)
    return result


def validate_algebra():
    I = np.eye(2)
    X = np.array([[0., 1.], [1., 0.]])
    Z = np.diag([1., -1.])
    H = (X+Z)/math.sqrt(2)

    def pauli(word):
        return kron_all([{'I': I, 'X': X, 'Z': Z}[c] for c in word])

    SX, SZ = pauli('XXXX'), pauli('ZZZZ')
    XD, ZD, XG, ZG = [pauli(w) for w in ('XXII', 'ZIZI', 'XIXI', 'ZZII')]
    assert np.allclose(SX@SZ, SZ@SX)
    for op in [XD, ZD, XG, ZG]:
        assert np.allclose(op@SX, SX@op)
        assert np.allclose(op@SZ, SZ@op)
    assert np.allclose(XD@ZD, -ZD@XD)
    for d in [XD, ZD]:
        for g in [XG, ZG]:
            assert np.allclose(d@g, g@d)

    # 列順は |D,G> = 00,01,10,11。
    basis = np.zeros((16, 4))
    for col, pair in enumerate([(0, 15), (10, 5), (12, 3), (6, 9)]):
        basis[list(pair), col] = 1/math.sqrt(2)
    assert np.allclose(basis.T@basis, np.eye(4))
    assert np.allclose(SX@basis, basis) and np.allclose(SZ@basis, basis)
    swap = np.zeros((16, 16))
    for i in range(16):
        bits = list(f'{i:04b}')
        bits[1], bits[2] = bits[2], bits[1]
        swap[int(''.join(bits), 2), i] = 1
    assert np.allclose(swap@XD@swap.T, XG)
    assert np.allclose(swap@ZD@swap.T, ZG)
    H4 = kron_all([H]*4)
    assert np.allclose(basis.T@swap@H4@basis, np.kron(H, H))

    # 8 物理ビットの対応位置 CNOT を符号空間へ制限。
    U = np.zeros((256, 256))
    for a in range(16):
        for b in range(16):
            U[16*a+(a ^ b), 16*a+b] = 1
    encoded = np.kron(basis, basis)
    target = np.zeros((16, 16))
    for a in range(4):
        for b in range(4):
            target[4*a+(a ^ b), 4*a+b] = 1
    assert np.allclose(encoded.T@U@encoded, target)

    # 等尤度の周辺化を全 16 パターンの列挙と比較。
    p = .01
    weights = [0., 0.]
    for e in itertools.product([0, 1], repeat=4):
        if sum(e) % 2 == 0:
            weights[e[0] ^ e[2]] += p**sum(e)*(1-p)**(4-sum(e))
    formula = [(1-p)**4+p**4+2*p*p*(1-p)**2, 4*p*p*(1-p)**2]
    assert np.allclose(weights, formula)
    return weights[1]/sum(weights)


def validate_notes():
    notes = {p.stem: p for p in ROOT.glob('*.md')}
    count = 0
    for path in notes.values():
        text = path.read_text(encoding='utf-8')
        prose = re.sub(r'```.*?```', '', text, flags=re.S)
        prose = re.sub(r'\$\$.*?\$\$', '', prose, flags=re.S)
        prose = re.sub(r'\$[^$\n]*\$', '', prose)
        for link in re.findall(r'!?\[\[([^\]]+)\]\]', prose):
            target = link.split('|')[0]
            name, _, heading = target.partition('#')
            if name.startswith('assets/'):
                assert (ROOT/name).is_file(), (path.name, target)
            else:
                assert name in notes, (path.name, target)
                if heading:
                    headings = re.findall(r'^#+ (.+)$', notes[name].read_text(encoding='utf-8'), re.M)
                    assert heading in headings, (path.name, target, 'heading')
            count += 1
        without_code = re.sub(r'```.*?```', '', text, flags=re.S)
        assert without_code.count('$$') % 2 == 0, path.name
        inline_only = re.sub(r'\$\$.*?\$\$', '', without_code, flags=re.S)
        assert inline_only.count('$') % 2 == 0, path.name
        assert '\\(' not in without_code and '\\[' not in without_code, path.name
        expressions = re.findall(r'\$\$(.*?)\$\$|\$([^$\n]+)\$', without_code, re.S)
        for display, inline in expressions:
            expression = display or inline
            depth = 0
            for char in re.sub(r'\\[{}]', '', expression):
                depth += (char == '{') - (char == '}')
                assert depth >= 0, (path.name, expression, 'brace order')
            assert depth == 0, (path.name, expression, 'unbalanced braces')
            starts = re.findall(r'\\begin\{([^}]+)\}', expression)
            ends = re.findall(r'\\end\{([^}]+)\}', expression)
            assert sorted(starts) == sorted(ends), (path.name, 'math environment')
    return {'notes': len(notes), 'internal_links': count,
            'characters': sum(len(p.read_text(encoding='utf-8')) for p in notes.values())}


def main():
    c4 = validate_algebra()
    rows = []
    for s in [12.25, 14., 15.6]:
        v = .5*10**(-s/10)
        rows.append({'s_db': s, 'variance': v, 'sd': math.sqrt(v),
                     'single_coordinate_odd_probability': odd_probability(v),
                     'mn_added_variance': 4*10**(-.2)*v})
    cp_off = float(beta.ppf(.95, 4, 1000000-3))
    cp_on = float(beta.ppf(.95, 5, 1000000-4))
    assert math.isclose(cp_off, 7.7536e-6, rel_tol=1e-5)
    assert math.isclose(cp_on, 9.1535e-6, rel_tol=1e-5)
    a = math.sqrt(math.pi)
    assert abs(wrapped_log_odds(a/2, .1)) < 1e-10
    report = {
        'scope': 'Textbook identities and reported-count arithmetic; not a factory simulation.',
        'algebra_checks': 'passed', 'markdown_checks': validate_notes(),
        'gkp_examples': rows, 'c4_zero_syndrome_example_p001': c4,
        'wrapped_odds_v01_z0': wrapped_log_odds(0, .1),
        'wrapped_odds_v01_z045a': wrapped_log_odds(.45*a, .1),
        'CP_95_3_in_1M': cp_off, 'CP_95_4_in_1M': cp_on,
        'Jeffreys_one_sided_0_in_15000': float(beta.ppf(.95, .5, 15000.5)),
        'Jeffreys_one_sided_0_in_200000': float(beta.ppf(.95, .5, 200000.5)),
        'CP_0_in_200000': -math.expm1(math.log(.05)/200000),
        'zero_failure_n_for_CP_1e_5': math.ceil(math.log(.05)/math.log1p(-1e-5)),
        'R3_q095': 12*288/.95, 'cost_ratio': 12/.95,
        'retention_product': .7*.96,
    }
    (ROOT/'計算'/'検算結果.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
