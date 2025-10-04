# /usr/bin/bash

set -e
uv sync --all-extras --all-groups

uv run pre-commit run --all-files
uv run coverage run --source=. -m pytest . -vs
uv run coverage report -m --fail-under=95
uv run mypy . --strict
cd docs/
uv run sphinx-apidoc -f -o source/ ../ ../tests/
uv run sphinx-build -M clean source build
uv run sphinx-build -M html source build
cd ..
