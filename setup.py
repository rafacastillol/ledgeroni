from setuptools import setup, find_packages

setup(
    name='ledgeroni',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'arrow',
        'six',
        'colorama'
    ],
    entry_points='''
        [console_scripts]
        ledgeroni=ledgeroni.cli:cli
    ''',
)
