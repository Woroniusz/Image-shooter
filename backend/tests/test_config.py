import os
from typing import Any

import pytest
from _pytest.monkeypatch import MonkeyPatch

from source_app.utils.Config import Config, ConfigSection


def test_configsection_getattr_and_getitem() -> None:
	# Create: data for ConfigSection
	data: dict[str, Any] = {'foo': 42, 'bar': {'baz': 'hello', 'nested': {'x': 1, 'y': 2}}}

	section: ConfigSection = ConfigSection(data)

	assert section.foo == 42
	bar_section = section.bar
	assert isinstance(bar_section, ConfigSection)
	assert bar_section.baz == 'hello'

	nested_section = section.bar.nested
	assert isinstance(nested_section, ConfigSection)
	assert nested_section.x == 1
	assert nested_section.y == 2

	assert section['foo'] == 42
	bar_section2 = section['bar']
	assert isinstance(bar_section2, ConfigSection)
	assert bar_section2['baz'] == 'hello'
	assert bar_section2['nested']['y'] == 2


def test_configsection_getattr_keyerror() -> None:
	data: dict[str, int] = {'a': 1}
	section: ConfigSection = ConfigSection(data)

	with pytest.raises(AttributeError) as excinfo:
		_ = section.not_exists
	assert "has no attribute 'not_exists'" in str(excinfo.value)


def test_configsection_repr() -> None:
	data: dict[str, Any] = {'x': 10, 'y': {'z': 5}}
	section: ConfigSection = ConfigSection(data)
	rep = repr(section)
	assert '<ConfigSection' in rep and repr(data) in rep


def test_config_init_file_not_exists(monkeypatch: MonkeyPatch) -> None:
	stub_path = '/nonexistent/path/config.toml'

	# mock os.path.isfile to always return False
	monkeypatch.setattr(os.path, 'isfile', lambda p: False)  # noqa: F841

	# mock builtins.open to raise FileNotFoundError
	with pytest.raises(FileNotFoundError) as excinfo:
		Config(stub_path)
	assert f'file not exists: {os.path.abspath(stub_path)}' in str(excinfo.value)


def test_config_loads_mock_toml() -> None:
	# Mock data for testing
	cfg: Config = Config(os.path.abspath(os.path.join(os.path.dirname(__file__), 'config', 'mock_config.toml')))

	assert cfg.general.app_name == 'ImageShooter'
	assert cfg.general.version == '0.1.0'
	assert cfg.logging.enable is True
	assert cfg.logging.level == 'DEBUG'
	# Sprawdź sekcje platformowe
	assert cfg.platform.linux.temp_dir == '/tmp/imageshooter'


def test_config_from_dict() -> None:
	# Test creating ConfigSection from a dictionary
	data: dict[str, Any] = {'key1': 'value1', 'key2': {'subkey': 'subvalue'}}
	config: Config = Config.from_dict(data)

	assert config.key1 == 'value1'
	assert config.key2.subkey == 'subvalue'

	# Test accessing via __getitem__
	assert config['key1'] == 'value1'
	assert config['key2']['subkey'] == 'subvalue'
