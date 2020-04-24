from setuptools import setup, find_packages

try:
    with open('requirements.txt', 'r') as fh:
        install_requires = [line.strip() for line in fh.readlines()]
except IOError:
    install_requires = []

setup(
    name='kia',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    entry_points='''
        [console_scripts]
        kia=commands.base:cli
    ''',
)
