from setuptools import setup

setup(name='qe-financial-spillover',
      version='0.1',
      description='an agent based model to simulate financial spillovers from QE,
      url='https://github.com/joerischasfoort/qe-financial-spillover',
      author='',
      author_email='',
      license='MIT',
      packages=['qe-financial-spillover'],
      setup_requires=['pytest-runner', 'numpy', 'pandas'],
      tests_require=['pytest'])

