uv venv
uv sync --all-extras --all-groups

uv run pre-commit run --all-files
uv run pytest .
uv run coverage run --source=. -m pytest .
uv run coverage report -m --fail-under=97
uv run mypy .

cd docs/
uv run sphinx-apidoc -f -o source/ ../ ../tests/
./make.bat clean
./make.bat html
cd ..
