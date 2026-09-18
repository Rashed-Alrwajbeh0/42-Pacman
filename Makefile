
all : run

install:
	@pip install -r requirements.txt
run:
	@pip install -r requirements.txt > /dev/null
	@python3 pac-man.py config.json
debug:
	@python3 pac-man.py config.json
clean:
	@rm -rf __pycache__ .mypy_cache
lint:
	@flake8 *.py
	@mypy *.py --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs 
