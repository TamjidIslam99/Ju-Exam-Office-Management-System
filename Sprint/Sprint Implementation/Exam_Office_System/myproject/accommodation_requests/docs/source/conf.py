# Configuration file for the Sphinx documentation builder.
import os
import sys
import django

#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'SpecialAccommodationRequest'
copyright = '2024, Suraiya Mahmuda'
author = 'Suraiya Mahmuda'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Adds the project root directory to the system path
sys.path.insert(0, os.path.abspath('../'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'
django.setup()

extensions = [
    'sphinx.ext.autodoc',           
    'sphinx.ext.viewcode',          
    'sphinx.ext.napoleon',          
    'sphinx_autodoc_typehints',     
]

templates_path = ['_templates']  
exclude_patterns = []  

language = 'python'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
