#!/usr/bin/env bash
set -euo pipefail

# Sprawdzamy, czy mamy plik pyproject.toml
if [[ ! -f /app/pyproject.toml ]]; then
  echo "Nie znaleziono pyproject.toml w bieżącym katalogu" >&2
  exit 1
fi

# sprawdz czy jest tomllib
if ! python3 -c "import tomllib" &>/dev/null; then
  echo "Brak modułu tomllib. Upewnij się, że używasz Pythona 3.11 lub nowszego." >&2
  pip3 install tomllib
  echo "Zainstalowano tomllib"
fi

# Wygeneruj requirements.txt
python3 - << 'PYCODE' > /app/requirements.txt
import tomllib

# Wczytujemy pyproject.toml
with open("pyproject.toml", "rb") as f:
    data = tomllib.load(f)

# Szukamy dependencies wg PEP 621 ([project].dependencies) lub Poetry ([tool.poetry.dependencies])
deps = {}
if "project" in data and "dependencies" in data["project"]:
    deps = data["project"]["dependencies"]
elif "tool" in data and "poetry" in data["tool"] and "dependencies" in data["tool"]["poetry"]:
    deps = data["tool"]["poetry"]["dependencies"]
else:
    raise SystemExit("Nie znalazłem sekcji dependencies w pyproject.toml")

requirements = []
for item in deps:
    # w PEP 621 element to string np. "requests>=2.0"
    if isinstance(item, str):
        if item == "detectron2":
            requirements.append('git+https://github.com/facebookresearch/detectron2.git')
            continue
        requirements.append(item)
    # w Poetry klucz→wartość, gdzie wartość może być wersją lub tabelą
    else:
        version = deps[item]
        if isinstance(version, str):
            requirements.append(f"{item}{version}")
        elif isinstance(version, dict) and "version" in version:
            requirements.append(f"{item}{version['version']}")
        else:
            # np. git, path etc. pomijamy lub można dopisać obsługę
            continue

# Sortujemy i drukujemy
for req in sorted(requirements, key=str.lower):
    print(req)
PYCODE

echo "Wygenerowano /app/requirements.txt:"
cat requirements.txt
