from __future__ import annotations

import os.path
import re
from typing import Any

import pygments.lexer
import pygments.token

Color = pygments.token.Token.Color


class PreCommitLexer(pygments.lexer.RegexLexer):
    name = 'pre-commit'
    aliases = ('pre-commit',)
    flags = re.MULTILINE

    tokens = {
        'root': [
            (r'(?<=\.\.\.)Failed$', Color.BGRed, 'output'),
            (r'(?<=\.\.\.)Passed$', Color.BGGreen, 'output'),
            (r'(?<=\.\.\.)Skipped$', Color.Black.BGYellow, 'output'),
            (
                r'(?<=\.\.\.\(no files to check\))Skipped$',
                Color.Black.BGCyan,
                'output',
            ),
            (r'^\[WARNING\]', Color.Black.BGYellow),
            (r'^\[ERROR\]', Color.BGRed),
            (r'.', pygments.token.Text),  # prevent error tokens
        ],
        'output': [
            ('^-.*$', Color.Faint),
            ('\n', pygments.token.Text),
            ('', pygments.token.Text, '#pop'),
        ],
    }


COLORS = {
    'Black': '#2e3436',
    'Cyan': '#06989a', 'Green': '#4e9a06', 'Red': '#c00', 'Yellow': '#c4a000',
    'FaintNormal': '#ccc',
}

STYLESHEET = '''\
.-Color-BGRed{{ background-color: {Red}; }}
.-Color-BGGreen{{ background-color: {Green}; }}
.-Color-Black-BGYellow{{ background-color: {Yellow}; color: {Black}; }}
.-Color-Black-BGCyan{{ background-color: {Cyan}; color: {Black}; }}
.-Color-Faint{{ color: {FaintNormal}; }}
'''


def stylesheet(colors: dict[str, str] | None = None) -> str:
    colors = colors or {}
    assert set(colors) <= set(COLORS), set(colors) - set(COLORS)
    colors = dict(COLORS, **colors)
    return STYLESHEET.format(**colors)


def setup(app: Any) -> dict[str, object]:  # pragma: no cover (sphinx)
    def copy_stylesheet(app: Any, exception: BaseException | None) -> None:
        if exception:
            return

        path = os.path.join(
            app.builder.outdir, '_static/pygments_pre_commit.css',
        )
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(stylesheet(app.config.pygments_pre_commit_ansi_colors))

    app.require_sphinx('1.8')
    app.add_config_value('pygments_pre_commit_ansi_colors', {}, 'html')
    app.add_css_file('pygments_pre_commit.css')
    app.connect('build-finished', copy_stylesheet)
    return {
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
