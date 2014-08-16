from setuptools import setup, find_packages
import os

version = '2.1.3'

setup(name='collective.geo.mapwidget',
      version=version,
      description="collective.geo mapwidget",
      long_description=open(
          "README.rst").read() + "\n" + open(
              os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
          "Framework :: Plone",
          "Framework :: Plone :: 4.3",
          "Intended Audience :: End Users/Desktop",
          "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          "Topic :: Internet",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Scientific/Engineering :: GIS",
          "Topic :: Office/Business :: Groupware",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='Zope Plone GIS KML Google Maps Bing OpenLayers',
      author='Giorgio Borelli',
      author_email='giorgio@giorgioborelli.it',
      url='https://github.com/collective/collective.geo.mapwidget',
      license='GPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['collective', 'collective.geo'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'BeautifulSoup',
          'geopy>=0.98',
          'Products.CMFCore',
          'plone.app.z3cform',
          'collective.geo.openlayers >= 3.1',
          'collective.geo.settings >= 3.0',
          'collective.z3cform.colorpicker >= 1.1',
      ],
      extras_require={
          'test': [
              'plone.app.testing',
          ]
      },
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
