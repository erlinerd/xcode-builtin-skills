#!/usr/bin/env python3
"""从 /Applications/Xcode.app 同步内置技能到本仓库。

用法: scripts/sync-from-xcode.py [Xcode.app 路径]
规则: 正文与官方源字节级一致；两个翻译 SKILL.md 的 frontmatter（skills CLI 契约）在重同步时保留。
自动发现: 专家技能 = 有 `<名>-ref-*.md.packaged` 参考资料的 `.idechatprompttemplate`。
"""
import glob, hashlib, os, plistlib, re, shutil, sys

app = sys.argv[1] if len(sys.argv) > 1 else '/Applications/Xcode.app'
chat = f'{app}/Contents/PlugIns/IDEIntelligenceChat.framework/Versions/A/Resources'
xcs  = f'{app}/Contents/PlugIns/IDEXCStringsSupport.framework/Versions/A/Resources/Skills'
repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root = os.path.join(repo, 'skill')

for p in (chat, xcs):
    if not os.path.isdir(p):
        sys.exit(f'找不到 {p}，请确认 Xcode 路径: {sys.argv[0]} <Xcode.app>')

with open(f'{app}/Contents/version.plist','rb') as f:
    v = plistlib.load(f)
build = v.get("ProductBuildVersion") or v.get("CFBundleVersion") or "?"
print(f'来源: Xcode {v["CFBundleShortVersionString"]} ({build})')

added = updated = unchanged = removed = 0

def sha(b): return hashlib.sha256(b).hexdigest()

def put(dst: str, data: bytes, keep_fm: bool = False):
    """写入文件；keep_fm 时保留 dst 已有的 frontmatter。返回动作标签。"""
    global added, updated, unchanged
    if keep_fm and os.path.exists(dst):
        old = open(dst, 'rb').read()
        m = re.match(rb'^(---\n.*?\n---\n\n)', old, re.S)
        if m: data = m.group(1) + data
    ensure = os.path.dirname(dst)
    os.makedirs(ensure, exist_ok=True)
    if os.path.exists(dst) and open(dst,'rb').read() == data:
        unchanged += 1; return 'unchanged'
    tag = 'updated' if os.path.exists(dst) else 'added'
    added += tag == 'added'; updated += tag == 'updated'
    open(dst,'wb').write(data)
    return tag

def clean_stale(dst_dir: str, keep: set):
    """删除 dst_dir 下源里已不存在的文件，返回删除数。"""
    global removed
    n = 0
    for r, _, fs in os.walk(dst_dir):
        for f in fs:
            p = os.path.join(r, f)
            if os.path.relpath(p, dst_dir) not in keep:
                os.remove(p); n += 1
    return n

def strip_fm(p: str) -> bytes:
    """去掉官方 packaged 文件不需要的包装——原样返回字节。"""
    return open(p,'rb').read()

# ── 翻译组 ──
for s in ('translation', 'translation-coordinator'):
    src_dir, dst_dir = f'{xcs}/{s}', f'{root}/xcode-integration/{s}'
    keep = set()
    for r, _, fs in os.walk(src_dir):
        for f in fs:
            src = os.path.join(r, f)
            rel = os.path.relpath(src, src_dir).replace('.packaged', '')
            dst = os.path.join(dst_dir, rel)
            keep.add(rel)
            put(dst, open(src,'rb').read(), keep_fm=(f == 'SKILL.md.packaged'))
    stale = clean_stale(dst_dir, keep)
    removed += stale
    print(f'[xcode-integration] {s}: 同步完成' + (f'，清理过期文件 {stale} 个' if stale else ''))

# ── 专家组：有参考资料的主模板才算技能，新增自动发现 ──
templates = sorted(f[:-len('.idechatprompttemplate')] for f in os.listdir(chat)
                   if f.endswith('.idechatprompttemplate')
                   and glob.glob(f'{chat}/{f[:-len(".idechatprompttemplate")]}-ref-*.md.packaged'))
for s in templates:
    dst_dir = f'{root}/ide-intelligence-chat/{s}'
    keep = {'SKILL.md'}
    put(f'{dst_dir}/SKILL.md', open(f'{chat}/{s}.idechatprompttemplate','rb').read())
    for f in glob.glob(f'{chat}/{s}-ref-*.md.packaged'):
        topic = os.path.basename(f)[len(s)+5:-len('.md.packaged')]
        put(f'{dst_dir}/references/{topic}.md', open(f,'rb').read())
        keep.add(f'references/{topic}.md')
    for f in glob.glob(f'{chat}/{s}-script-*.py'):
        rest = os.path.basename(f)[len(s)+len('-script-'):]
        put(f'{dst_dir}/scripts/{rest}', open(f,'rb').read())
        keep.add(f'scripts/{rest}')
    stale = clean_stale(dst_dir, keep)
    removed += stale
    print(f'[ide-intelligence-chat] {s}: 同步完成' + (f'，清理过期文件 {stale} 个' if stale else ''))

# ── 源里已消失的技能目录 ──
for group in ('xcode-integration', 'ide-intelligence-chat'):
    gdir = f'{root}/{group}'
    if not os.path.isdir(gdir): continue
    for d in sorted(os.listdir(gdir)):
        full = f'{gdir}/{d}'
        expect = (d in ('translation','translation-coordinator')) if group=='xcode-integration' else (d in templates)
        if os.path.isdir(full) and not expect:
            shutil.rmtree(full); removed += 1
            print(f'[{group}] 已删除源中消失的技能: {d}')

# ── 终验 ──
def sha_file(p): return sha(open(p,'rb').read())
same = diff = 0
for r, _, fs in os.walk(f'{root}/xcode-integration'):
    for f in fs:
        p = os.path.join(r, f)
        rel = os.path.relpath(p, f'{root}/xcode-integration')
        src = f'{xcs}/{rel}'
        src_p = src + '.packaged' if os.path.exists(src + '.packaged') else src
        if not os.path.exists(src_p): continue
        if f == 'SKILL.md':
            body = open(p,'rb').read()
            m = re.match(rb'^---\n.*?\n---\n\n', body, re.S)
            body = body[m.end():] if m else body
            same += sha(body) == sha_file(src_p); continue
        same += sha_file(p) == sha_file(src_p)
for s in templates:
    same += sha_file(f'{chat}/{s}.idechatprompttemplate') == sha_file(f'{root}/ide-intelligence-chat/{s}/SKILL.md')
    for f in glob.glob(f'{chat}/{s}-ref-*.md.packaged'):
        topic = os.path.basename(f)[len(s)+5:-len('.md.packaged')]
        same += sha_file(f) == sha_file(f'{root}/ide-intelligence-chat/{s}/references/{topic}.md')

print(f'\n结果: 新增 {added}，更新 {updated}，未变 {unchanged}，删除 {removed}')
print(f'终验: 与官方源字节级一致 {same} 个文件（翻译 SKILL.md 按"去 frontmatter 后正文"口径）')
print('后续: git add -A && git commit && git tag <Xcode版本号>')
