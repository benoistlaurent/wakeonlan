
"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst', 'rt') as f:
    readme = f.read()

with open('HISTORY.rst', 'rt') as f:
    history = f.read()

requirements = ['PyYAML>=3.13']

setup(
    author='Benoist LAURENT',
    author_email='benoist.laurent@ibpc.fr',
    name='wakeonlan',
    description='A tool to wake machine from LAN',
    long_description=readme + '\n\n' + history,
    url='https://github.com/benoistlaurent/wakeonlan',
    version='1.2.0',
    install_requires=requirements,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: MIT License',
    ],
    packages=find_packages(include=['wakeonlan']),
    entry_points={
        'console_scripts': [
            'wakeonlan=wakeonlan.cli:main',
        ],
    },
)
