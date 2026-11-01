"""Build a portable formula concordance from the supplied TeX, preserving provenance."""
from pathlib import Path
import re
import shutil

VAULT=Path(__file__).resolve().parents[1]
SOURCE=VAULT.parent/'main.tex'
if not SOURCE.exists():
    SOURCE=VAULT/'sources/main.tex'
tex=SOURCE.read_text(encoding='utf-8')
(VAULT/'sources').mkdir(exist_ok=True)
(VAULT/'assets').mkdir(exist_ok=True)
if SOURCE.parent != VAULT/'sources':
    for name in ('main.tex','references.bib','00README.json'):
        shutil.copy2(SOURCE.parent/name,VAULT/'sources'/name)
    for i in range(1,10):
        shutil.copy2(SOURCE.parent/f'fig{i}.png',VAULT/'assets'/f'fig{i}.png')

chapters={p.name[:2]:p.stem for p in VAULT.glob('*.md')}
def chapter_for(line):
    if line<193:return '07'
    if line<217:return '08'
    if line<335:return '14'
    if line<346:return '18'
    if line<366:return '10'
    if line<374:return '13'
    if line<439:return '11'
    if line<463:return '16'
    if line<529:return '17'
    if line<561:return '18'
    if line<630:return '06'
    if line<654:return '07'
    if line<717:return '13'
    if line<759:return '08'
    if line<790:return '09'
    if line<837:return '15'
    if line<982:return '16'
    if line<1000:return '16'
    if line<1105:return '11'
    if line<1217:return '17'
    if line<1313:return '18'
    if line<1356:return '19'
    if line<1883:return '15'
    return '18'

macros={
 'LLR':r'\mathrm{LLR}','Pacc':r'P_{\mathrm{acc}}','Plog':r'P_{\mathrm L}',
 'Peff':r'P_{\mathrm{eff}}','Phard':r'P_{\mathrm{hard}}','Puse':r'P_{\mathrm{use}}',
 'Pcond':r'P_{\mathrm{cond}}','fflag':r'f_{\mathrm{flag}}','alphaflag':r'\alpha_{\mathrm{flag}}',
 'alphatol':r'\alpha_{\mathrm{tol}}','Fflag':r'\mathcal F','sq':r'\mathrm{sq}',
 'Cfour':r'\mathrm{C4}','GKP':r'\mathrm{GKP}','MBQC':r'\mathrm{MBQC}',
 'PS':r'\mathrm{PS}','Cl':r'\mathrm{Cl}','Pauli':r'\mathcal P','proj':r'\Pi',
 'dB':r'\mathrm{dB}','PL':r'P_{\mathrm L}','Ptar':r'P_{\mathrm{tar}}',
 'MN':r'\mathrm{MN}','QRL':r'\mathrm{QRL}','act':'a',
 'bm':r'\boldsymbol'
}
def convert(body):
    body=re.sub(r'(?<!\\)%[^\n]*','',body)
    body=re.sub(r'\\label\{[^}]+\}','',body)
    body=body.replace(r'\nonumber','').replace(r'\notag','')
    body=re.sub(r'\\([A-Za-z]+)',lambda m: macros.get(m.group(1),m.group(0)),body)
    # Physics package macros absent from a default Obsidian MathJax setup.
    # Remaining ket arguments contain braces around \mathrm; handle balanced braces.
    for macro,left,right in [('ket',r'\lvert ',r'\rangle'),('bra',r'\langle ',r'\rvert')]:
        token='\\'+macro+'{'
        while token in body:
            start=body.index(token); i=start+len(token); depth=1; end=i
            while depth:
                if body[end]=='{':depth+=1
                elif body[end]=='}':depth-=1
                end+=1
            inner=body[i:end-1]
            body=body[:start]+left+inner+right+body[end:]
    body=re.sub(r'\\\\\[[^\]]*\]',lambda m:r'\\',body)
    return body.strip()

blocks=list(re.finditer(r'\\begin\{(equation\*?|align\*?)\}(.*?)\\end\{\1\}',tex,re.S))
index=['# 22 原論文の数式対応表','',
 '提供版のすべての `equation` / `align` 表示環境をソース順に拾った対応表です。元の組版上の式番号を推測せず、本教材では「式001」のような通し参照を付けます。インライン式は各章で説明し、表示式原文は [[25_表示数式の原文集]] に収録しています。','',
 '以下の「導出・解説先」は、式の前提、計算の手順、または定義の意味を説明する章です。定義式や学習済み写像は物理法則から導出する式ではありません。QRL固有の係数や未公開遷移表は引用・未公開の境界として明示しています。','',
 '| 本教材の式参照 | 原文ラベル／場所 | ソース行 | 導出・解説先 |','|---|---|---|---|']
atlas=['# 25 表示数式の原文集','',
 '本ノートは提供されたTeXの表示数式を、原文との照合用に集めた補遺です。学習は [[00_はじめに]] の順に進め、わからない式が出たときに参照してください。論文内マクロをMathJaxの標準表記へ展開し、式番号・ラベル命令・行間調整を除きました。式の変数は原文の規約です。','',
 '出典：同梱 [main.tex](sources/main.tex)。各式に提供版のソース行、原ラベル、解説ノートを示します。','']
for i,m in enumerate(blocks,1):
    line=tex[:m.start()].count('\n')+1
    labels=re.findall(r'\\label\{([^}]+)\}',m.group(2))
    label=', '.join(labels) if labels else 'ラベルなし'
    no=f'式{i:03d}'
    key=chapter_for(line)
    if 'eq:label_preserving_H' in labels:key='15'
    if 'eq:primary_residual_channel' in labels or 'eq:primary_canonical_failure' in labels:key='17'
    chapter=chapters[key]
    index.append(f'| [[25_表示数式の原文集#{no}]] | `{label}` | {line} | [[{chapter}]] |')
    body=convert(m.group(2))
    if m.group(1).startswith('align'):
        body='\\begin{aligned}\n'+body+'\n\\end{aligned}'
    atlas += [f'## {no}','',f'原文ラベル：`{label}`。ソース行 {line}。解説：[[{chapter}]]。','', '$$',body,'$$','']
(VAULT/'22_原論文の数式対応表.md').write_text('\n'.join(index)+'\n',encoding='utf-8')
(VAULT/'25_表示数式の原文集.md').write_text('\n'.join(atlas)+'\n',encoding='utf-8')
print(f'{len(blocks)} displayed equation environments indexed; source and nine figures copied.')
