from setuptools import setup

setup(
    name='ledgeroni',
    version='0.1',
    py_modules=['ledgeroni'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        ledgeroni=ledgeroni.cli:cli
    ''',
)
