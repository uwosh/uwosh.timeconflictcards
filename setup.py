# -*- coding: utf-8 -*-
"""
This module contains the tool of uwosh.timeconflictcards
"""
import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.3.3'

long_description = (
    read('README.txt')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' +
    read('CHANGES.txt')
    + '\n' +
    'Detailed Documentation\n'
    '**********************\n'
    + '\n' +
    read('uwosh', 'timeconflictcards', 'README.txt')
    + '\n' +
    'Contributors\n'
    '************\n'
    + '\n' +
    read('CONTRIBUTORS.txt')
    + '\n' +
    'Download\n'
    '********\n')

tests_require = ['zope.testing']

setup(name='uwosh.timeconflictcards',
      version=version,
      description="UW Oshkosh Registrar's Office Time Conflict Cards",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Plone',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        ],
      keywords='',
      author='',
      author_email='',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['uwosh', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'Products.ATVocabularyManager',
                        'collective.easytemplate>=0.7.10',
                        'uwosh.policy.ldap',
                        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite='uwosh.timeconflictcards.tests.test_docs.test_suite',
      entry_points="""
      # -*- entry_points -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      # setup_requires=["collective.easytemplate"],
      # setup_requires=["PasteScript"],
      # paster_plugins=["ZopeSkel"],
      )
