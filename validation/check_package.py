#!/usr/bin/env python3
"""Validate a distributable Paper Study folder; requires PyYAML for development."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import tempfile

import yaml


def check_skill(skill):
    skill = Path(skill).resolve()
    files = sorted(p for p in skill.rglob('*') if p.is_file())
    if not files:
        raise ValueError('Empty skill folder')
    for p in skill.rglob('*'):
        if p.is_symlink():
            raise ValueError(f'Symlink prevents standalone distribution: {p.name}')
        if p.is_file() and (p.suffix.lower() in {'.pdf', '.png', '.pyc'} or p.name == '.DS_Store'):
            raise ValueError(f'Non-runtime artifact in instruction package: {p.name}')
    content = (skill / 'SKILL.md').read_text(encoding='utf-8')
    match = re.match(r'\A---\s*\n(.*?)\n---(?:\n|$)', content, re.S)
    if not match:
        raise ValueError('Missing YAML frontmatter')
    metadata = yaml.safe_load(match.group(1))
    if not isinstance(metadata, dict) or metadata.get('name') != skill.name:
        raise ValueError('Skill name must match its install folder')
    if not isinstance(metadata.get('description'), str) or not metadata['description'].strip():
        raise ValueError('Missing description')
    local_links = []
    for p in files:
        if p.suffix not in {'.md', '.yaml'} and p.name != 'LICENSE':
            raise ValueError(f'Unexpected runtime file type: {p.name}')
        body = p.read_text(encoding='utf-8')
        if '/Users/' in body or re.search(r'[A-Za-z]:\\Users\\', body):
            raise ValueError(f'Personal installation path in package: {p.name}')
        if p.suffix != '.md':
            continue
        for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', body):
            if target.startswith(('https://', 'http://', '#')):
                continue
            target = target.split('#', 1)[0]
            resolved = (p.parent / target).resolve()
            if not resolved.is_relative_to(skill) or not resolved.is_file():
                raise ValueError(f'Broken or escaping reference: {target}')
            local_links.append(resolved)
    referenced = set(local_links)
    for p in (skill / 'references').glob('*.md'):
        if p.resolve() not in referenced:
            raise ValueError(f'Undiscoverable reference: {p.name}')
    interface = yaml.safe_load((skill / 'agents/openai.yaml').read_text(encoding='utf-8'))['interface']
    for key in ('display_name', 'short_description', 'default_prompt'):
        if not isinstance(interface.get(key), str) or not interface[key].strip():
            raise ValueError(f'Missing UI field: {key}')
    if not 25 <= len(interface['short_description']) <= 64:
        raise ValueError('UI short_description must be 25–64 characters')
    if '$' + metadata['name'] not in interface['default_prompt']:
        raise ValueError('Default prompt does not invoke the skill')
    license_text = (skill / 'LICENSE').read_text(encoding='utf-8')
    if not license_text.startswith('MIT License\n') or 'Copyright (c)' not in license_text:
        raise ValueError('Standalone skill must retain its MIT notice')
    return {str(p.relative_to(skill)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}


def verify_copy(skill):
    before = check_skill(skill)
    with tempfile.TemporaryDirectory(prefix='paper-study-copy-') as tmp:
        dest = Path(tmp) / Path(skill).name
        shutil.copytree(skill, dest)
        after = check_skill(dest)
        if before != after:
            raise ValueError('Standalone copy changed package bytes')
        # Meaningful failure probes: incomplete install and broken relative reference.
        license_text = (dest / 'LICENSE').read_text(encoding='utf-8')
        (dest / 'LICENSE').unlink()
        try:
            check_skill(dest)
        except (ValueError, FileNotFoundError):
            pass
        else:
            raise ValueError('Incomplete install was accepted')
        (dest / 'LICENSE').write_text(license_text, encoding='utf-8')
        (dest / 'references/input-handling.md').unlink()
        try:
            check_skill(dest)
        except (ValueError, FileNotFoundError):
            pass
        else:
            raise ValueError('Broken local reference was accepted')
    return before


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('skill', type=Path)
    args = parser.parse_args()
    hashes = verify_copy(args.skill)
    print(json.dumps({'status': 'pass', 'files': hashes,
                      'checks': ['metadata', 'local_references', 'portable_paths',
                                 'UI', 'standalone_license', 'identical_copy',
                                 'reject_missing_license', 'reject_broken_reference']}, indent=2))


if __name__ == '__main__':
    main()
