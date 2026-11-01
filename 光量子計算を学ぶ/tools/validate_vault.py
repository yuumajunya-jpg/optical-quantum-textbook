"""Validate navigation, embedded files, Markdown math structure and source coverage."""
from pathlib import Path
import re
import json

ROOT=Path(__file__).resolve().parents[1]
notes=sorted(ROOT.glob('*.md'))
known={p.stem:p for p in notes}
files={p.name:p for p in ROOT.rglob('*') if p.is_file()}

# Add stable, idempotent chapter navigation. Obsidian itself needs no config.
for i,p in enumerate(notes):
    body=p.read_text(encoding='utf-8').split('\n<!-- navigation -->')[0].rstrip()
    nav=['[[00_はじめに|学習目次]]']
    if i:nav.append(f'[[{notes[i-1].stem}|前へ]]')
    if i+1<len(notes):nav.append(f'[[{notes[i+1].stem}|次へ]]')
    body+='\n\n<!-- navigation -->\n\n---\n\n'+' · '.join(nav)+'\n'
    p.write_text(body,encoding='utf-8')

errors=[]; linkcount=0; displays=0; chars=0
for p in notes:
    text=p.read_text(encoding='utf-8'); chars+=len(text)
    if text.count('$$')%2:errors.append(f'{p.name}: unpaired display delimiter')
    if text.count('```')%2:errors.append(f'{p.name}: unpaired code fence')
    prose=re.sub(r'```.*?```|`[^`]*`|\$\$.*?\$\$|(?<!\$)\$(?!\$)[^\n$]*\$', '', text, flags=re.S)
    for link in re.findall(r'!?\[\[([^\]]+)\]\]',prose):
        linkcount+=1
        target=link.split('|')[0]
        target,_,anchor=target.partition('#')
        dest=known.get(target) or files.get(target)
        if dest is None:errors.append(f'{p.name}: missing {target}')
        elif anchor:
            other=dest.read_text(encoding='utf-8')
            headings=re.findall(r'^#{1,6} (.+)$',other,re.M)
            if anchor not in headings:errors.append(f'{p.name}: missing anchor {target}#{anchor}')
    for block in re.findall(r'\$\$(.*?)\$\$',text,re.S):
        displays+=1
        depth=0
        # Exclude escaped literal braces when checking TeX argument grouping.
        clean=re.sub(r'\\[{}]','',block)
        for ch in clean:
            if ch=='{':depth+=1
            elif ch=='}':depth-=1
            if depth<0:errors.append(f'{p.name}: negative math brace depth');break
        if depth:errors.append(f'{p.name}: unmatched math braces')
        envs=[]
        for action,env in re.findall(r'\\(begin|end)\{([^}]+)\}',block):
            if action=='begin':envs.append(env)
            elif not envs or envs.pop()!=env:errors.append(f'{p.name}: math environment mismatch')
        if envs:errors.append(f'{p.name}: unclosed math environment')
    # Check relative Markdown file links, excluding external links.
    for target in re.findall(r'\]\(([^)]+)\)',text):
        if not re.match(r'[a-z]+://',target) and not (p.parent/target).exists():
            errors.append(f'{p.name}: missing Markdown file {target}')
    if re.search(r'四元数|\bTODO\b|\bTBD\b',text):errors.append(f'{p.name}: placeholder or terminology error')

source=(ROOT/'sources/main.tex').read_text(encoding='utf-8')
original_count=len(re.findall(r'\\begin\{(?:equation\*?|align\*?)\}',source))
atlas=(ROOT/'25_表示数式の原文集.md').read_text(encoding='utf-8')
atlas_count=len(re.findall(r'^## 式\d+',atlas,re.M))
if original_count!=atlas_count:errors.append('Source equation coverage mismatch')
report={'notes':len(notes),'characters_including_math_and_reference':chars,
        'wiki_links_and_embeds':linkcount,'display_math_blocks':displays,
        'original_display_environments':original_count,'indexed_display_environments':atlas_count,
        'source_figures':len(list((ROOT/'assets').glob('fig*.png'))),'errors':errors}
(ROOT/'tools/validation_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
if errors:raise SystemExit(1)
