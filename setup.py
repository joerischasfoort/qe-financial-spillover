from setuptools import setup

setup(name='abm',
      version='0.1',
      description='an agent based model to simulate the stock market',
      url='http://github.com/LCfP/qe-financial-spillover',
      author='',
      author_email='',
      license='MIT',
      packages=['stockmarket'],
      setup_requires=['pytest-runner', 'numpy', 'pandas'],
      tests_require=['pytest'])

