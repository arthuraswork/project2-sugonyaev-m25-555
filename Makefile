install:
	poetry install

database:
	poetry run database

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install dist/*.whl

lint:
	poetry run ruff check .

run:
	poetry lock
	poetry install
	poetry build
	poetry run database