from setuptools import setup
import implements_helper

DESCRIPTION = "Python実装時に利用できるユーティリティ群"
NAME = 'implements_helper'
AUTHOR = 'Mikimini9627'
AUTHOR_EMAIL = ''
URL = 'https://github.com/Mikimini9627/implements_helper'
LICENSE = 'MIT License'
DOWNLOAD_URL = 'https://github.com/Mikimini9627/implements_helper'
VERSION = implements_helper.__version__
PYTHON_REQUIRES = ">=3.12"

INSTALL_REQUIRES = [
    "numpy>=1.26.4,<2.0.0",
    "python-dateutil>=2.9.0.post0,<3.0.0",
    "bs4>=0.0.2,<0.0.3",
    "requests>=2.32.3,<3.0.0",
    "lxml>=5.3.0,<6.0.0",
    "useragent-changer>=0.3.2,<0.4.0",
    "ruff>=0.8.6,<0.9.0",
]

PACKAGES = [
    'implements_helper'
]

CLASSIFIERS = [
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.12',
]

with open('README.rst', 'r') as fp:
    readme = fp.read()

setup(name=NAME,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      maintainer=AUTHOR,
      maintainer_email=AUTHOR_EMAIL,
      description=DESCRIPTION,
      long_description=readme,
      license=LICENSE,
      url=URL,
      version=VERSION,
      download_url=DOWNLOAD_URL,
      python_requires=PYTHON_REQUIRES,
      install_requires=INSTALL_REQUIRES,
      packages=PACKAGES,
      classifiers=CLASSIFIERS
    )