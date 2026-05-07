# docs/conf.py

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = "pytest-html-plus"
copyright = "2026, ReporterPlus"
author = "ReporterPlus"
release = "1.0.1"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "myst_parser",
]

templates_path = ["_templates"]
exclude_patterns = []


html_theme = "furo"
html_static_path = ["_static"]
