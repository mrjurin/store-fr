#!/usr/bin/env python
from setuptools import setup, find_packages

from store import VERSION


setup(
    name='store_fr',
    version=VERSION,
    url='https://github.com/tangentlabs/django-oscar-paypal',
    author="Nicolas Karageuzian",
    author_email="nicolas@karageuzian.com",
    description=(
        "Integrated webstore french legal compliance"),
    long_description=open('README.rst').read(),
    keywords="Store, PayPal, Oscar",
    license=open('LICENSE').read(),
    platforms=['linux'],
    packages=find_packages(exclude=['sandbox*', 'tests*']),
    include_package_data=True,
    install_requires=['requests>=1.0'],
    extras_require={
        'oscar': ["django-oscar>=0.6"]
    },
    # See http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Other/Nonlisted Topic'],
)
