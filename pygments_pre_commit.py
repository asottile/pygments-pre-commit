import os.path
import re
from typing import Any
from typing import Dict
from typing import Optional

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


def stylesheet(colors: Optional[Dict[str, str]] = None) -> str:
    colors = colors or {}
    assert set(colors) <= set(COLORS), set(colors) - set(COLORS)
    colors = dict(COLORS, **colors)
    return STYLESHEET.format(**colors)


def setup(app: Any) -> None:  # pragma: no cover (sphinx)
    def copy_stylesheet(app: Any, exception: Optional[BaseException]) -> None:
        if exception:
            return

        path = os.path.join(
            app.builder.outdir, '_static/pygments_pre_commit.css',
        )
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(stylesheet(app.config.pygments_pre_commit_ansi_colors))

    app.require_sphinx('1.0')
    app.add_config_value('pygments_pre_commit_ansi_colors', {}, 'html')
    app.add_stylesheet('pygments_pre_commit.css')
    app.connect('build-finished', copy_stylesheet)
