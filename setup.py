try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


VERSION = open('VERSION').read().strip()

REQUIRES = open('requirements.txt').read()


setup(
  name='modeled.Qt',
  version=VERSION,
  description="Qt GUI Adapter for modeled objects.",

  author='Stefan Zimmermann',
  author_email='zimmermann.code@gmail.com',
  url='http://bitbucket.org/userzimmermann/python-modeled',

  license='GPLv3',

  install_requires=REQUIRES,

  namespace_packages=['modeled'],
  py_modules=[
    'modeled.Qt',
    ],

  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved ::'
    ' GNU Library or Lesser General Public License (LGPL)',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Topic :: Software Development',
    'Topic :: Utilities',
    ],
  keywords=[
    'modeled', 'model', 'modeling', 'modelled', 'modelling',
    'serialization', 'exchange', 'mapping',
    'class', 'object', 'member', 'property', 'typed',
    'ctypes', 'cfunc', 'funcptr',
    'python3',
    ],
  )
