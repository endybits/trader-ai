install:
	pip install -U pip &&\
	pip install -r requirements.txt
sem-release:
	python3 -m pip install python-semantic-release
install-plot:
	python -m pip install -U matplotlib
format:
	black .
lint:
	ruff check .
install-all:
	make install
	make install-plot