from setuptools import setup, find_packages

setup(name='abm',
      version='0.1',
      description='an agent based model to simulate the stock market',
      url='http://github.com/LCfP/qe-financial-spillover',
      author='',
      author_email='',
      license='MIT',
      packages=find_packages(),
      setup_requires=['pytest-runner', 'numpy', 'pandas'],
      tests_require=['pytest'])

