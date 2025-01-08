# Makefile for GatorTicketMaster

PYTHON = python3
MAIN_SCRIPT = gatorTicketMaster.py
EXECUTABLE = gatorTicketMaster
INPUT_FILE ?= input.txt

.PHONY: all run clean

all: $(EXECUTABLE)

$(EXECUTABLE): $(MAIN_SCRIPT)
	$(PYTHON) -m pip install pyinstaller
	$(PYTHON) -m PyInstaller --onefile $(MAIN_SCRIPT) --name $(EXECUTABLE)
	mv dist/$(EXECUTABLE) .
	rm -rf build dist *.spec

run: $(EXECUTABLE)
	./$(EXECUTABLE) $(INPUT_FILE)

clean:
	rm -f $(EXECUTABLE)
	rm -rf build dist *.spec __pycache__