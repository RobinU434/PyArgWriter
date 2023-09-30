all: 

test:
	python -m pytest tests/ -vv

clean:
	rm tests/temp/*.yaml
	rm tests/temp/*.yml
	rm tests/temp/*.json
	rm tests/temp/*.py

