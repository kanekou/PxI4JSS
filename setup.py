from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), 'r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name="pxi4jss",
    packages=find_packages(),
    install_requires=['snakes-utils>=2.0.2', 'dwave-neal', 'pandas', 'pyqubo'],
    version="1.0",
    license="MIT",
    author='kanekou',
    author_email='k208580@ie.u-ryukyu.ac.jp',
    url='https://github.com/kanekou/pxi4jss',
    description='It is modeling tool for automatically generating Ising models from JSS Petri nets.',
    long_description=readme,
    long_description_content_type="text/markdown",
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
    ],
)
