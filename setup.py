from setuptools import setup, find_packages
import sys, os


sys.path.insert(0, os.path.dirname(__file__))
version = '0.0'

setup(name='simplesync',
      version=version,
      description="one-line desc",
      long_description="""\
long_desc""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='python django asynchrone',
      author='Grindizer',
      author_email='grindizer@gmail.com',
      url='http://URL',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      test_suite="tests",
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
