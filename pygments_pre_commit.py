import os.path
import re

import pygments.lexer
import pygments.token

Color = pygments.token.Token.Color


class PreCommitLexer(pygments.lexer.RegexLexer):
    name = 'pre-commit'
    aliases = ('pre-commit',)
    flags = re.MULTILINE

    tokens = {
        'root': [
            (r'(?<=\.\.\.)Failed$', Color.BGRed),
            (r'(?<=\.\.\.)Passed$', Color.BGGreen),
            (r'(?<=\.\.\.)Skipped$', Color.BlackBGYellow),
            (r'(?<=\.\.\.\(no files to check\))Skipped$', Color.BlackBGCyan),
            (r'^\[WARNING\]', Color.BlackBGYellow),
            (r'^\[ERROR\]', Color.BGRed),
            (r'.', pygments.token.Text),  # prevent error tokens
        ],
    }


COLORS = {
    'Black': '#2e3436',
    'Cyan': '#06989a', 'Green': '#4e9a06', 'Red': '#c00', 'Yellow': '#c4a000',
}

STYLESHEET = '''\
.-Color-BGRed{{ background-color: {Red}; }}
.-Color-BGGreen{{ background-color: {Green}; }}
.-Color-BlackBGYellow{{ background-color: {Yellow}; color: {Black}; }}
.-Color-BlackBGCyan{{ background-color: {Cyan}; color: {Black}; }}
'''


def stylesheet(colors=None):
    colors = colors or {}
    assert set(colors) <= set(COLORS), set(colors) - set(COLORS)
    colors = dict(COLORS, **colors)
    return STYLESHEET.format(**colors)


def setup(app):  # pragma: no cover (sphinx)
    def copy_stylesheet(app, exception):
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
