# py-toml10n

Simple TOML-based localization manager for Python.

[![PyPI version](https://img.shields.io/pypi/v/py-toml10n)](https://pypi.org/project/py-toml10n/)
[![Tests](https://github.com/Pon4ick/py-toml10n/actions/workflows/publish.yml/badge.svg)](https://github.com/Pon4ick/py-toml10n/actions)
[![Python versions](https://img.shields.io/badge/python-3.11%2B-blue)](https://pypi.org/project/py-toml10n/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Installation

```bash
pip install py-toml10n
```

## Quick Start
1. Create localization files

```
locales/
├── en.toml
└── ru.toml
```

locales/en.toml:

```toml
hello = "Hello"
world = "World"
```

locales/ru.toml:

```toml
hello = "Привет"
world = "Мир"
```

2. Use in your code

```python
from toml10n import LocalizationManager

LM = LocalizationManager("locales/", default_language="en")

# Get a string in the default language
print(LM.get_string("hello"))  # Hello

# Short syntax
print(LM["hello"])  # Hello

# Get a string in a specific language
print(LM.get_string("hello", language="ru"))  # Привет


# List available languages
print(LM.supported_languages)  # ['en', 'ru']
```

# Features

- Simple — just TOML files, nothing else.

- Thread-safe — safe to use in multi-threaded applications.

- Hot reload — call reload() to pick up changes without restarting.

- Fallback — missing keys fall back to the default language.

- Type hints — full type annotation support.

- Zero dependencies — uses only stdlib tomllib (Python 3.11+).

# API Reference

```python
LocalizationManager(locale_dir="locales/", default_language="en")
```

Initialize the manager and load all .toml files from locale_dir.

    locale_dir — path to the folder with .toml files

    default_language — language code used when none is specified

---

```python
get_string(key, language=None)
```

Return a localized string by key.

    key — translation key

    language — language code, uses default_language if None

    Returns the string or [[key]] if not found

---

```python
reload()
```

Reload all localization files. Useful for hot-reload during development.

---

```python
load_file(filename)
```

Load a single .toml file by name.
supported_languages

Property that returns a list of all loaded language codes.

## Exceptions

    LocaleDirNotFoundError — the directory doesn't exist

    LanguageNotFoundError — requested language is not loaded

    LocaleFileLoadError — a TOML file cannot be parsed