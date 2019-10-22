#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='Foot Print',
      version='1.0',
      description='Domain Foot Printing',
      author='Sudhara Dharmawardhana',
      author_email='sudharadharmawardhana@gmail.com',
      url='https://github.com/sud0x0/Foot-Print',
      license='GPL-2.0',
      install_requires= ['pandas','bs4','shodan'],
      packages=find_packages()+['.'],
      include_package_data=True,
     )
