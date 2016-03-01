from setuptools import setup
from Cython.Build import cythonize

setup(
    name = 'frozenintervaltree',
    packages = ['frozenintervaltree'],
    install_requires=['cython'],
    version = '0.1',
    description = 'Frozen interval trees',
    author = 'Yue Zhang',
    author_email = 'yjzhang@cs.washington.edu',
    ext_modules = cythonize('frozenintervaltree/frozenintervaltree.pyx'),
    test_suite='nose.collector',
    tests_require=['nose']
)
