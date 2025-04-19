# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
# sys.path.insert(0, os.path.abspath('..'))
# sys.path.insert(0, os.path.abspath('../SOURCE/modules/'))
# sys.path.insert(0, os.path.abspath('../SOURCE/modules/cfp_context.py'))
sys.path.insert(0, os.path.abspath('../../SOURCE'))
# for x in os.walk('../SOURCE'):
#   sys.path.insert(0, x[0])

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'cf pipeline'
copyright = '2025, Nathan Tolbert'
author = 'Nathan Tolbert'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
