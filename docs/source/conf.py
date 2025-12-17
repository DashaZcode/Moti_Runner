import os
import sys

# Добавляем путь к проекту
sys.path.insert(0, os.path.abspath('../..'))

# Основные настройки
project = 'Moti Runner'
copyright = '2024, Автор'
author = 'Автор'
release = '1.0'
language = 'ru'

# Расширения
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

# Тема
html_theme = 'sphinx_rtd_theme'

# Настройки для Google-style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = False

# Настройки autodoc
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
}