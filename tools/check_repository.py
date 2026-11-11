"""Read-only integrity checks for the distributable benchmark (no submissions run)."""
from pathlib import Path
import hashlib
import json
import math
import re
import tomllib
from scoring import GROUPS, WEIGHTS

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    catalog = json.loads((ROOT / 'task_catalog.json').read_text())
    slugs = {entry['slug'] for entry in catalog}
    require(len(slugs) == len(catalog) == 10, 'Expected ten unique tasks')
    require(slugs == set(WEIGHTS), 'Catalog/scorer task mismatch')
    require(slugs == {p.name for p in (ROOT / 'tasks').iterdir() if p.is_dir()},
            'Unexpected task directories')
    weights = json.loads((ROOT / 'scoring_weights.json').read_text())['weights']
    for slug in sorted(slugs):
        task = ROOT / 'tasks' / slug
        config = tomllib.loads((task / 'task.toml').read_text())
        require(config['verifier']['environment_mode'] == 'separate', slug + ': verifier mode')
        require(config['artifacts'] == ['/app/submission'], slug + ': artifact scope')
        for name in ('verifier.py', 'scoring.py'):
            require((task / 'tests' / name).read_bytes() == (ROOT / 'tools' / name).read_bytes(),
                    slug + ': stale ' + name)
        require((task / 'solution/run.py').read_bytes() == (ROOT / 'tools/engine.py').read_bytes(),
                slug + ': stale reference solution')
        require((task / 'environment/spec/SCORING.md').read_bytes() == (ROOT / 'SCORING.md').read_bytes(),
                slug + ': stale scoring specification')
        require({p.name for p in (task / 'tests/cases').iterdir()} == {'0', '1', '2'},
                slug + ': expected three cases')
        rubric = json.loads((ROOT / 'rubrics' / (slug + '.json')).read_text())
        actual = {c['id']: c['max_score'] for c in rubric['criteria']}
        expected = dict(zip(GROUPS, WEIGHTS[slug]))
        require(actual == weights[slug] == expected, slug + ': rubric weight drift')
        require(math.isclose(sum(actual.values()), 1), slug + ': weights do not sum to one')
        for criterion in rubric['criteria']:
            atoms = criterion.get('subcriteria', [])
            if atoms:
                require(math.isclose(sum(a['max_score'] for a in atoms), criterion['max_score']),
                        slug + ': atomic score mismatch')
        visible = task / 'environment'
        require(not list(visible.rglob('truth.json')) and not list(visible.rglob('trace_truth.csv')),
                slug + ': truth in agent build context')
        for p in (visible / 'data').iterdir():
            require(p.read_bytes() == (task / 'tests/cases/0/data' / p.name).read_bytes(),
                    slug + ': visible fixture drift: ' + p.name)
    manifest = json.loads((ROOT / 'data_manifest.json').read_text())
    paths = [row['path'] for row in manifest]
    require(len(paths) == len(set(paths)), 'Duplicate manifest entry')
    require(set(paths) == {str(p.relative_to(ROOT)) for p in ROOT.glob('tasks/*/environment/data/*') if p.is_file()},
            'Manifest coverage mismatch')
    for row in manifest:
        require(hashlib.sha256((ROOT / row['path']).read_bytes()).hexdigest() == row['sha256'],
                'Checksum mismatch: ' + row['path'])
    # Root/documentation links only: task contracts also contain illustrative paths.
    for p in [*ROOT.glob('*.md'), *ROOT.glob('docs/*.md'), *ROOT.glob('rubrics/*.md')]:
        for target in re.findall(r'\]\(([^)]+)\)', p.read_text()):
            if '://' in target or target.startswith('#'):
                continue
            require((p.parent / target.split('#')[0]).exists(), f'Broken link in {p.name}: {target}')
    print(f'Repository integrity passed: {len(slugs)} tasks, {len(paths)} input checksums, synchronized rubrics and implementations.')


if __name__ == '__main__':
    main()
