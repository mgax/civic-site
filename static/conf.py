# -*- coding: utf-8 -*-
#
# Civic DB documentation build configuration file, created by
# sphinx-quickstart on Sun May 29 11:57:45 2011.
#
# This file is execfile()d with the current directory set to its containing dir.

import sys, os

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#sys.path.insert(0, os.path.abspath('.'))

# -- General configuration -----------------------------------------------------

extensions = []
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'CivicDB'
copyright = u'2011, Alex Morega'
version = '1.0'
release = '1.0'
exclude_patterns = ['_build']
pygments_style = 'sphinx'
html_show_sourcelink = False
html_theme = 'agogo'
html_title = project
html_static_path = ['_static']
htmlhelp_basename = 'CivicDBdoc'
