# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import sys
sys.path.append('../src')

import recsys.data
import recsys.data.dataset
import recsys.job
import recsys.util
import recsys.service
import recsys.api
import recsys.tmdb_api
import recsys.logger
import recsys.database
import recsys.model
import recsys.model.surprise
import recsys.domain_context
import recsys.repository
import recsys.mapper

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'rec-sys-client-lib'
copyright = '2023, Adrian Norberto Marino'
author = 'Adrian Norberto Marino'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode'
]
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
