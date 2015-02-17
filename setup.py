#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('requirements.txt') as f:
    install_reqs = [line for line in f.read().split('\n') if line]

with open('test_requirements.txt') as f:
    test_reqs = [line for line in f.read().split('\n') if line]

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = install_reqs

test_requirements = test_reqs

setup(
    name='tmuxipy',
    version='0.1.7',
    description="Manage Tmux sessions legitly",
    long_description=readme + '\n\n' + history,
    author="Milind Shakya",
    author_email='sh.milind@gmail.com',
    url='https://github.com/milin/tmuxipy',
    packages=[
        'tmuxipy',
    ],
    package_dir={'tmuxipy':
                 'tmuxipy'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='tmux',
    entry_points={
        'console_scripts': [
            'tmuxipy = tmuxipy.main:main',
        ]
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
