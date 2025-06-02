import os
import tomllib
from typing import Any


class ConfigSection:
	"""
	ConfigSection
	A class to represent a section of a configuration file.
	Each section can be accessed like an object or a dictionary.
	"""

	def __init__(self, data: dict):
		self._data = data

	def __getattr__(self, name: str) -> Any:
		"""
		Access attributes like an object.
		"""

		if name not in self._data:
			raise AttributeError(f"'ConfigSection' object has no attribute '{name}'")
		value = self._data[name]
		if isinstance(value, dict):
			return ConfigSection(value)
		return value

	def __getitem__(self, key: Any) -> Any:
		"""
		Access items like a dictionary.
		"""
		if key not in self._data:
			raise KeyError(f"Key '{key}' not found in config.")
		if isinstance(self._data[key], dict):
			return ConfigSection(self._data[key])
		return self._data[key]

	def __repr__(self) -> str:
		return f'<ConfigSection {self._data!r}>'


class Config:
	"""
	Config
	"""

	def __init__(self, path: str) -> None:
		self._path = os.path.abspath(path)
		if not os.path.isfile(self._path):
			raise FileNotFoundError(f'file not exists: {self._path}')

		with open(self._path, 'rb') as f:
			self._data: dict[str, Any] = tomllib.load(f)

	def __getattr__(self, name: str) -> Any | ConfigSection:
		"""
		Access attributes like an object.
		"""
		data: dict[str, Any] = self._data
		if name in data:
			value = data[name]
			if isinstance(value, dict):
				return ConfigSection(value)
			return value

		raise AttributeError(f"'Config' object has no attribute '{name}'")

	def __getitem__(self, key: Any) -> Any | ConfigSection:
		"""
		Access items like a dictionary.
		"""
		if key not in self._data:
			raise KeyError(f"Key '{key}' not found in config.")
		if isinstance(self._data[key], dict):
			return ConfigSection(self._data[key])
		return self._data[key]

	def __repr__(self) -> str:
		return f'<Config path={self._path!r}>'

	def as_dict(self) -> dict:
		return self._data.copy()

	@staticmethod
	def from_dict(data: dict[str, Any]) -> 'Config':
		"""
		Create a Config instance from a dictionary.
		"""
		config = Config.__new__(Config)
		config._data = data
		return config
