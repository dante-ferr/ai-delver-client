ENTRYPOINT ?= main

run: on_run
	./run.sh $(ENTRYPOINT)