import os
import sys
import tomllib


class Config:
	"""
	Config
	"""

	def __init__(self, path: str) -> None:
		self._path = os.path.abspath(path)
		if not os.path.isfile(self._path):
			raise FileNotFoundError(f'file not exists: {self._path}')

		with open(self._path, 'rb') as f:
			self._data = tomllib.load(f)

	def __getattr__(self, name: str):
		"""
		Umożliwia dostęp do sekcji/kluczy configu poprzez atrybuty.
		Jeśli `name` nie istnieje w korzeniu _data, wyrzuci AttributeError.
		"""
		data = self._data
		if name in data:
			value = data[name]
			# Jeśli wartością jest dict, opakowujemy je w ConfigSection, by umożliwić
			# dalszy dostęp atrybutowy (np. cfg.database.host).
			if isinstance(value, dict):
				return ConfigSection(value)
			return value

		raise AttributeError(f"'Config' object has no attribute '{name}'")

	def __getitem__(self, key):
		"""
		Umożliwia dostęp do configu przez `cfg["section"]` albo zagnieżdżone
		`cfg["section"]["podsekcja"]`.
		Zwraca zwykłe dict / wartość.
		"""
		return self._data[key]

	def __repr__(self):
		return f'<Config path={self._path!r}>'

	def as_dict(self) -> dict:
		"""
		Zwraca całą zawartość pliku TOML jako standardowy słownik Pythona.
		"""
		return self._data.copy()


class ConfigSection:
	"""
	Pomocnicza klasa, która opakowuje słownik (sekcję configu)
	i pozwala na dostęp do kluczy poprzez atrybuty.

	Przykład:
	    cs = ConfigSection({"host": "localhost", "port": 5432})
	    print(cs.host)  # "localhost"
	    print(cs["port"])  # 5432
	"""

	def __init__(self, data: dict):
		self._data = data

	def __getattr__(self, name: str):
		if name in self._data:
			value = self._data[name]
			if isinstance(value, dict):
				return ConfigSection(value)
			return value

		raise AttributeError(f"'ConfigSection' object has no attribute '{name}'")

	def __getitem__(self, key):
		return self._data[key]

	def __repr__(self):
		return f'<ConfigSection {self._data!r}>'
