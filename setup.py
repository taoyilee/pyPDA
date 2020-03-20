#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', 'matplotlib==3.1.3', 'numpy==1.18.1', 'scipy==1.4.1', 'scikit-learn==0.22.1']

setup_requirements = []

test_requirements = []

setup(
    author="Tao-Yi Lee",
    author_email='taoyil@uci.edu',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A Pythonic toolkit to generate synthetic blood pressure waveforms based on principle of pulse decomposition analysis (PDA).",
    entry_points={
        'console_scripts': [
            'pypda=pypda.cli:cli',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/x-rst',
    include_package_data=True,
    keywords='pypda',
    name='pypda',
    packages=find_packages(include=['pypda', 'pypda.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/taoyilee/pypda',
    version='0.4.1',
    zip_safe=False,
)
