try:
    import tomllib
except ImportError:
    import tomli as tomllib

import threading
from pathlib import Path

class LocaleDirNotFoundError(Exception):
    """Raised when the locale directory is not found."""
    pass

class LanguageNotFoundError(Exception):
    """Raised when the requested language is not loaded."""
    pass

class LocaleFileLoadError(Exception):
    """Raised when a TOML file cannot be parsed."""
    pass

class LocalizationManager:
    """A localization manager based on TOML files.

    Attributes:
        locale_dir: Path to the folder with .toml files.
        default_language: Default language code.
    """

    def __init__(
        self,
        locale_dir: str | Path = "locales/",
        default_language: str = "en"
    ) -> None:
        """
        Initialize the manager and load all .toml files.
        
        Args:
            locale_dir: Path to the folder with localization files.
            default_language: Default language code.
            
        Raises:
            LocaleDirNotFoundError: If the directory does not exist.
        """

        self.locale_dir = Path(locale_dir)
        self.languages: dict[str, dict[str, str]] = {}
        self.default_language = default_language
        self._lock = threading.Lock()

        if not self.locale_dir.exists():
            raise LocaleDirNotFoundError(
                f"Locale directory not found: {self.locale_dir}"
            )

        self._load_all()

    @property
    def supported_languages(self) -> list[str]:
        """Return a list of loaded language codes."""

        with self._lock:
            return list(self.languages.keys())
    
    def _load_all(self) -> None:
        """Load all .toml files from the default locale directory."""

        for file in self.locale_dir.glob("*.toml"):
            self._load_file(file)

    def _load_file(self, path) -> None:
        """Load a single TOML file by its full path."""

        try:
            with open(path, "rb") as f:
                data = tomllib.load(f)
        except Exception as e:
            raise LocaleFileLoadError(f"Failed to load {path.name}: {e}") from e
        with self._lock:
            self.languages[path.stem] = data

    def load_file(self, filename: str) -> None:
        """Load a single TOML file by name.
        
        Args:
            filename: File name (e.g., 'ru.toml').
            
        Raises:
            FileNotFoundError: If the file doesn't exist.
            LocaleFileLoadError: If the file cannot be parsed.
        """

        full_path = self.locale_dir / filename
        if not full_path.exists():
            raise FileNotFoundError(f"File not found: {full_path}")
        self._load_file(full_path)
        
    def reload(self) -> None:
        """Reload all localization files."""

        with self._lock:
            self.languages.clear()
        self._load_all()

    def get_string(self, key: str, language: str | None = None) -> str:
        """Return a localized string by key.
        
        Args:
            key: Translation key.
            language: Language code. If None, default_language is used.
            
        Returns:
            The localized string or [[key]] if the key is not found.
            
        Raises:
            LanguageNotFoundError: If the language is not loaded.
        """

        with self._lock:
            lang = language or self.default_language
            if lang not in self.languages:
                raise LanguageNotFoundError(
                    f"Language '{lang}' not loaded. "
                    f"Available: {self.languages}"
                )
            return (
                self.languages[lang].get(key)
                or self.languages[self.default_language].get(key, f"[[{key}]]")
        )

    def __getitem__(self, key: str) -> str:
        return self.get_string(key)