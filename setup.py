from distutils.core import setup
from Cython.Build import cythonize

setup(
    name = 'frozenintervaltree',
    packages = ['frozenintervaltree'],
    version = '0.1',
    description = 'Frozen interval trees',
    author = 'Yue Zhang',
    author_email = 'yjzhang@cs.washington.edu',
    ext_modules = cythonize('src/frozenintervaltree.pyx')
)
