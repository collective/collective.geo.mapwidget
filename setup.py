from setuptools import setup, find_packages
import os

version = '1.5'

setup(name='collective.geo.mapwidget',
      version=version,
      description="collective.geo mapwidget",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=["Framework :: Plone",
        "Topic :: Internet",
        "Topic :: Scientific/Engineering :: GIS",
        "Programming Language :: Python",
        ],
      keywords='Zope Plone GIS KML Google Maps Bing Yahoo OpenLayers',
      author='Giorgio Borelli',
      author_email='giorgio@giorgioborelli.it',
      url='https://svn.plone.org/svn/collective/collective.geo.mapwidget',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.geo'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Plone',
          # -*- Extra requirements: -*-
          'collective.geo.openlayers',
          'collective.geo.settings',
          'plone.app.z3cform',
          'collective.z3cform.colorpicker',
      ],
      extras_require={
          'test': [
              'plone.testing',
          ]
      },
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
