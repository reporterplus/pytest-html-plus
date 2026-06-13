# docs/conf.py

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = "pytest-html-plus"
copyright = "2026, ReporterPlus"
author = "ReporterPlus"
release = "1.1.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "myst_parser",
]

# MyST is enabled for basic Markdown parsing only.
# Keep advanced syntax extensions disabled unless explicitly needed.
myst_enable_extensions = []

templates_path = ["_templates"]
exclude_patterns = []


html_theme = "furo"
html_static_path = ["_static"]
