from setuptools import setup, find_packages

version = '1.0.2'

requires = [
    'setuptools',
    'lxml',
    'argparse',
    'python-dateutil < 2.0dev',
    'unittest2',
    'zope.interface',
    'zope.schema',
]

setup(name='corejet.core',
      version=version,
      description="Defines test infrastructure for building CoreJet tests",
      long_description=open("README.txt").read() + "\n" +
                       open("CHANGES.txt").read(),
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='corejet zope.testing',
      author='Martin Aspeli',
      author_email='optilude@gmail.com',
      url='http://corejet.org',
      license='ZPL 2.1',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['corejet'],
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      entry_points="""
      [console_scripts]
      corejet2py = corejet.core.scripts.corejet2py:main
      """,
      )
