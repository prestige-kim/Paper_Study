#!/usr/bin/env python3
"""Check Codex local skill discovery without starting a model turn."""

import argparse
import json
import os
from pathlib import Path
import selectors
import shutil
import subprocess
import tempfile
import time


def check_discovery(skill, codex_executable='codex'):
    version = subprocess.check_output([codex_executable, '--version'], text=True).strip()
    with tempfile.TemporaryDirectory(prefix='paper-study-discovery-') as tmp:
        root = Path(tmp).resolve()
        target = root / '.agents/skills/paper-study'
        target.parent.mkdir(parents=True)
        shutil.copytree(skill, target)
        subprocess.run(['git', 'init', '-q', str(root)], check=True)
        with tempfile.TemporaryFile() as stderr:
            proc = subprocess.Popen([codex_executable, 'app-server', '--stdio', '-c', 'analytics.enabled=false'],
                                    cwd=root, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=stderr)
            selector = selectors.DefaultSelector()
            selector.register(proc.stdout, selectors.EVENT_READ)
            pending = b''

            def send(message):
                proc.stdin.write((json.dumps(message) + '\n').encode())
                proc.stdin.flush()

            def receive(request_id):
                nonlocal pending
                deadline = time.monotonic() + 30
                while time.monotonic() < deadline:
                    while b'\n' in pending:
                        line, pending = pending.split(b'\n', 1)
                        response = json.loads(line)
                        if response.get('id') == request_id:
                            if 'error' in response:
                                raise RuntimeError(response['error'])
                            return response['result']
                    if selector.select(timeout=min(1, max(0, deadline - time.monotonic()))):
                        chunk = os.read(proc.stdout.fileno(), 65536)
                        if not chunk:
                            raise RuntimeError('App server closed before responding')
                        pending += chunk
                raise TimeoutError(f'No response for request {request_id}')

            try:
                send({'id': 1, 'method': 'initialize', 'params': {
                    'clientInfo': {'name': 'paper_study_validation', 'version': '0.1.0'}}})
                receive(1)
                send({'method': 'initialized'})
                send({'id': 2, 'method': 'skills/list', 'params': {
                    'cwds': [str(root)], 'forceReload': True}})
                result = receive(2)
                entries = result['data']
                matches = [s for e in entries for s in e['skills']
                           if Path(s['path']).resolve() == (target / 'SKILL.md').resolve()]
                relevant_errors = [e for entry in entries for e in entry['errors']
                                   if str(target) in e['path']]
                if relevant_errors or len(matches) != 1:
                    raise RuntimeError({'matches': len(matches), 'errors': relevant_errors})
                found = matches[0]
                if found['name'] != 'paper-study' or found['scope'] != 'repo' or not found['enabled']:
                    raise RuntimeError('Copied skill was not enabled at repo scope')
                if found.get('interface', {}).get('displayName') != 'Paper Study':
                    raise RuntimeError('OpenAI UI metadata was not loaded')
                return {'status': 'pass', 'codex_version': version,
                        'name': found['name'], 'scope': found['scope'], 'enabled': found['enabled'],
                        'relative_path': '.agents/skills/paper-study/SKILL.md',
                        'interface': found['interface'], 'model_turn_started': False}
            finally:
                selector.close()
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait(timeout=5)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('skill', type=Path)
    parser.add_argument('--codex-executable', default='codex', help='CLI path when codex is not on PATH')
    args = parser.parse_args()
    print(json.dumps(check_discovery(args.skill.resolve(), args.codex_executable), indent=2))
