"""Validate the preserved A-2 package from any checkout (stdlib + ImageMagick)."""
import hashlib
import json
import pathlib
import re
import subprocess

PACKAGE = pathlib.Path(__file__).resolve().parent
VERSION = PACKAGE.parent.parent
ROOT = VERSION.parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    manifest = json.loads((PACKAGE / 'manifest.json').read_text())
    checked = 0

    def walk(value):
        nonlocal checked
        if isinstance(value, dict):
            if isinstance(value.get('path'), str):
                assert not pathlib.Path(value['path']).is_absolute(), value
                path = (VERSION / value['path']).resolve()
                assert path.is_file(), path
                assert path.is_relative_to(ROOT), path
                assert not path.is_relative_to(ROOT / 'tmp'), path
                if 'sha256' in value:
                    assert digest(path) == value['sha256'], path
                if 'bytes' in value:
                    assert path.stat().st_size == value['bytes'], path
                checked += 1
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    for record in manifest['generation_ancestry_records']:
        walk(json.loads((VERSION / record).read_text()))
    assert len(manifest['selected']) == 10
    for entry in manifest['selected']:
        assert digest(VERSION / entry['image']) == entry['sha256']
        data = json.loads((VERSION / entry['record']).read_text())
        assert data['user_selected'] is True
        source = data.get('final_image', data.get('output'))
        assert digest(VERSION / source['path']) == entry['sha256']
    copy_checks = 0
    for target, original in manifest['source_copy_map'].items():
        if (ROOT / original).is_file():
            assert digest(VERSION / target) == digest(ROOT / original), target
            copy_checks += 1
    pngs = list(PACKAGE.rglob('*.png'))
    for path in pngs:
        subprocess.run(['magick', str(path), 'null:'], check=True, capture_output=True)
    links = 0
    for file in [PACKAGE / 'README.md', VERSION / 'README.md']:
        for target in re.findall(r'\]\(([^)]+)\)', file.read_text()):
            if not target.startswith(('http:', 'https:', '#')):
                assert (file.parent / target.split('#')[0]).exists(), (file, target)
                links += 1
    result = {'status': 'pass', 'selected_images': 10,
              'generation_records': len(manifest['generation_ancestry_records']),
              'record_paths_sizes_hashes_checked': checked,
              'source_byte_comparisons': copy_checks,
              'source_comparisons_note': 'Optional comparisons against original ignored working files when present.',
              'png_full_decodes': len(pngs), 'markdown_links_checked': links,
              'active_paths_portable': True,
              'visual_review': 'Preserved generation-time reviews; no artwork changes during adoption.',
              'command': 'python3 akari-v3.1/situations/a2-home/verify.py'}
    (PACKAGE / 'validation.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
