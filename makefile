console:
	$(shell bin/env) bin/console

test:
	python3 -m unittest discover -t. -stest

.PHONY: \
	console \
	test
