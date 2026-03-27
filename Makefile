.PHONY: install run cron-install cron-uninstall

install:
	pip install -r requirements.txt

run:
	python scout.py

cron-install:
	python scheduler.py install

cron-uninstall:
	python scheduler.py uninstall
