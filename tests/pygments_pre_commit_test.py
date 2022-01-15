from __future__ import annotations

import os.path
import re
import subprocess
import sys

import pygments.formatters
import pygments.lexers
import pytest

import pygments_pre_commit

ANSI_LEXER = pygments.lexers.get_lexer_by_name('ansi', stripnl=False)
LEXER = pygments.lexers.get_lexer_by_name('pre-commit', stripnl=False)
HTML_FORMATTER = pygments.formatters.HtmlFormatter()

ANSI_ESCAPE = re.compile(r'\033\[[^m]*m')
NORM_WS_START_RE = re.compile(r'(<[^/][^>]+>)(\s*)')
NORM_WS_END_RE = re.compile(r'(\s*)(</[^>]+>)')
EMPTY_TAG_RE = re.compile(r'<[^/][^>]+></[^>]+>')

DEMO_DIR = os.path.join(os.path.dirname(__file__), '../demo')

HTML = '''\
<!doctype html>
<html><head>
<style>body { background-color: #2d0922; color: #fff; } STYLES</style>
</head><body>HTML</body></html>
'''
HTML = HTML.replace('STYLES', pygments_pre_commit.stylesheet())


def uncolor(s):
    return ANSI_ESCAPE.sub('', s)


def highlight(lexer, s):
    ret = pygments.highlight(s, lexer=lexer, formatter=HTML_FORMATTER)
    ret = NORM_WS_START_RE.sub(r'\2\1', ret)
    ret = NORM_WS_END_RE.sub(r'\2\1', ret)
    ret = EMPTY_TAG_RE.sub('', ret)
    return HTML.replace('HTML', ret)


def compare(request, *args, **kwargs):
    cmd = (sys.executable, '-mpre_commit', 'run', '--color=always') + args
    kwargs.update(stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    proc = subprocess.Popen(cmd, **kwargs)
    out = proc.communicate()[0].decode()

    assert 'No module named pre_commit' not in out

    ansi = highlight(ANSI_LEXER, out)
    pre_commit = highlight(LEXER, uncolor(out))

    fname = f'{request.node.name}_ansi.html'
    with open(os.path.join(DEMO_DIR, fname), 'w') as f:
        f.write(ansi)

    fname = f'{request.node.name}_pre_commit.html'
    with open(os.path.join(DEMO_DIR, fname), 'w') as f:
        f.write(pre_commit)

    assert ansi == pre_commit


PRE_COMMIT_CONFIG = '''\
repos:
-   repo: local
    hooks:
    -   id: passing
        name: passing
        language: system
        entry: 'true'
    -   id: failing
        name: failing
        language: system
        entry: python -c 'import sys; print(sys.argv[1:]); exit(1)'
    -   id: skipped-no-files
        name: skipped (no files)
        language: system
        entry: 'true'
        files: ^$
    -   id: skip-me
        name: skip me
        language: system
        entry: 'true'
'''


@pytest.fixture
def pcdir(tmpdir):
    with tmpdir.as_cwd():
        subprocess.check_call(('git', 'init'))
        tmpdir.join('.pre-commit-config.yaml').write(PRE_COMMIT_CONFIG)
        tmpdir.join('a').ensure()
        subprocess.check_call(('git', 'add', ':/'))
        yield tmpdir


def test_basic(pcdir, request):
    compare(request, env=dict(os.environ, SKIP='skip-me'))


def test_unstaged_changes(pcdir, request):
    pcdir.join('a').write('unstaged')
    compare(request, 'passing')


def test_error_unstaged_config(pcdir, request):
    pcdir.join('.pre-commit-config.yaml').write('\n\n', mode='a+')
    compare(request)
