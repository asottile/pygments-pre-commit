from setuptools import setup

setup(
    name='pygments_pre_commit',
    description='A pygments lexer for pre-commit output.',
    url='https://github.com/asottile/pygments-pre-commit',
    version='1.0.0',
    author='Anthony Sottile',
    author_email='asottile@umich.edu',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    install_requires=['pygments'],
    py_modules=['pygments_pre_commit'],
    entry_points={
        'pygments.lexers': ['pre-commit=pygments_pre_commit:PreCommitLexer'],
    },
)
