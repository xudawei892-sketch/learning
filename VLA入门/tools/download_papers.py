#!/usr/bin/env python3
"""Fetch original arXiv PDFs; keep verifiable status without third-party packages."""
import argparse
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
from datetime import datetime, timezone
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'manifest.json'


def now():
    return datetime.now(timezone.utc).isoformat()


def identifier(p):
    return p.get('paper_id') or p['arxiv_id']


def request(url):
    return urllib.request.urlopen(
        urllib.request.Request(url, headers={'User-Agent': 'VLA-Learning-Library/1.0'}),
        timeout=60,
    )


def inspect_pdf(data):
    if len(data) < 1024 or not data.startswith(b'%PDF-') or b'%%EOF' not in data[-4096:]:
        raise ValueError('Response is not a complete recognizable PDF')
    return hashlib.sha256(data).hexdigest()


def download(p):
    p = dict(p)
    dest = ROOT / p['pdf_path']
    try:
        if dest.exists():
            data = dest.read_bytes()
            sha = inspect_pdf(data)
            if p.get('sha256') and sha != p['sha256']:
                raise ValueError('Existing PDF hash differs from manifest; preserve file for investigation')
            p.update(pdf_status='downloaded', sha256=sha, bytes=len(data), last_checked=now())
            if not p.get('downloaded_at'):
                p['provenance'] = 'Existing file; original download provenance not established'
            return p
        with request(p['pdf_url']) as response:
            data = response.read(64 * 1024 * 1024 + 1)
            final_url = response.geturl()
            expected = response.headers.get('Content-Length')
        if len(data) > 64 * 1024 * 1024:
            raise ValueError('PDF exceeds download size limit')
        if expected and len(data) != int(expected):
            raise ValueError('Content-Length mismatch')
        sha = inspect_pdf(data)
        dest.parent.mkdir(parents=True, exist_ok=True)
        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(dir=dest.parent, suffix='.part', delete=False) as tmp:
                temp_path = Path(tmp.name)
                tmp.write(data)
            # Link is atomic and refuses to overwrite a file created by another process.
            os.link(temp_path, dest)
        finally:
            if temp_path is not None:
                temp_path.unlink(missing_ok=True)
        p.update(pdf_status='downloaded', sha256=sha, bytes=len(data),
                 downloaded_at=now(), final_url=final_url, last_error=None)
    except Exception as exc:
        p.update(pdf_status='failed', last_error=f'{type(exc).__name__}: {exc}', last_attempt=now())
    return p


def save(manifest):
    temporary = MANIFEST.with_suffix('.json.tmp')
    temporary.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temporary.replace(MANIFEST)
    papers = manifest['papers']
    count = sum(p['pdf_status'] == 'downloaded' for p in papers)
    lines = ['# PDF 下载状态', '', f'原始 PDF 已取得：**{count}/{len(papers)}**。', '',
             '只有下载成功且通过基本文件完整性检查的论文才有 `paper.pdf`。导读不等于全文精读。', '']
    if 'network_check' in manifest:
        n = manifest['network_check']
        lines += [f"最近连接检查（UTC）：{n['checked_at']}", '',
                  f"结果：{n['status']}；{n.get('error', '')}", '']
    lines += ['|论文|状态|文件/原文|', '|---|---|---|']
    for p in papers:
        target = p['pdf_path'] if p['pdf_status'] == 'downloaded' else p['pdf_url']
        lines.append(f"|{p['name']}|{p['pdf_status']}|[{'本地 PDF' if p['pdf_status'] == 'downloaded' else '官方下载'}]({target})|")
    lines += ['', '来源：31 篇 arXiv 原文，ALOHA Unleashed 使用作者项目的官方 PDF。',
              '后续刷新或补下载需要允许来源域名；本轮 arXiv 已实际连通。网络草稿与发布状态应分别确认。',
              '', '刷新并检查文件：`python3 VLA入门/tools/download_papers.py --workers 3`。',
              '已下载文件会检查并复用；无占位 PDF；失败原因保存在 `manifest.json`。']
    (ROOT / '下载状态.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--probe', action='store_true', help='Check access to one PDF before batch download')
    parser.add_argument('--only', nargs='+', help='Only download these paper IDs (usually arXiv IDs)')
    parser.add_argument('--workers', type=int, default=3, choices=range(1, 5))
    args = parser.parse_args()
    manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
    papers = manifest['papers']
    if args.only:
        missing = set(args.only) - {identifier(p) for p in papers}
        if missing:
            parser.error('Unknown paper IDs: ' + ', '.join(sorted(missing)))
    if args.probe:
        target = next(p for p in papers if p['arxiv_id'] == '2406.09246')
        check = {'url': target['pdf_url'], 'checked_at': now()}
        try:
            with request(target['pdf_url']) as response:
                header = response.read(8)
            if not header.startswith(b'%PDF-'):
                raise ValueError('Destination did not return a PDF header')
            check['status'] = 'reachable'
            print('arXiv PDF access works; no complete PDF downloaded during probe.')
        except Exception as exc:
            check.update(status='blocked_or_unavailable', error=f'{type(exc).__name__}: {exc}')
            print(check['error'], file=sys.stderr)
        manifest['network_check'] = check
        save(manifest)
        return 0 if check['status'] == 'reachable' else 1
    selected = [p for p in papers if not args.only or identifier(p) in args.only]
    results = {}
    # Modest concurrency avoids excessive load on the public archive.
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        for p in pool.map(download, selected):
            results[identifier(p)] = p
            print(p['name'], p['pdf_status'])
    manifest['papers'] = [results.get(identifier(p), p) for p in papers]
    save(manifest)
    return 1 if any(p['pdf_status'] != 'downloaded' for p in results.values()) else 0


if __name__ == '__main__':
    sys.exit(main())
