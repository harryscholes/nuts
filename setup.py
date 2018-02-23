from setuptools import setup, find_packages

setup(name='nuts',
      version='0.1',
      description='Python package for calculating kernels on graphs',
      author='Harry Scholes',
      author_email='@harryscholes',
      url='https://github.com/harryscholes/nuts',
      packages=find_packages(),
      install_requires=[
          'numpy',
          'networkx',
          'scipy',
          'tables',
          'nose',
          'codecov',
          ]
      )
