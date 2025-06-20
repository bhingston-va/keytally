# | Command            | What it does                                          |
# | ------------------ | ----------------------------------------------------- |
# | `make`             | Set up venv, install deps, build the binary           |
# | `make run`         | Run key tracker via Python in venv                    |
# | `make stats`       | Show CLI stats                                        |
# | `make install`     | Should install deps in venv                           |
# | `make build`       | Builds the binary (run in venv; requires pyinstaller) |
# | `make clean`       | Remove build artifacts                                |
# | `make purge`       | Remove venv and build artifacts                       |
# | `make install-bin` | Copy compiled binary to `/usr/local/bin/keytally/kt`  |
# | `make update-bin`  | Replaces binary to `/usr/local/bin/keytally/kt`       |
# | `make link-bin`    | Links nested binary so that it can be ran with `kt`   |
# | `make unlink-bin`  | Removes `kt` symlink                                  |

# === CONFIG ===
APP_NAME = keytally
ENTRYPOINT = keytally.py
VENV_DIR = venv
REQ_FILE = requirements.txt
DIST_DIR = dist
INSTALL_PARENT_DIR = /usr/local/bin
INSTALL_DIR = /usr/local/bin/keytally
VERSION = $(shell cat VERSION)
LINK_PATH = /usr/local/bin/kt

# === DEFAULTS ===
.PHONY: all
all: build

# === SETUP ===
install:
	python3.12 -m venv $(VENV_DIR)
	$(VENV_DIR)/bin/pip install pyinstaller
	$(VENV_DIR)/bin/pip install -r $(REQ_FILE)
	@echo "✓ Virtualenv set up with dependencies."

# === BUILD ===
build: install
	@echo "🏗 Building standalone binary: $(APP_NAME) version $(VERSION)"
	sed "s/__version__ = \".*\"/__version__ = \"$(VERSION)\"/" $(ENTRYPOINT) > _tmp.py
	$(VENV_DIR)/bin/pyinstaller --onedir --name $(APP_NAME) _tmp.py
	rm _tmp.py

# === RUN ===
run:
	$(VENV_DIR)/bin/python $(ENTRYPOINT) track

stats:
	$(VENV_DIR)/bin/python $(ENTRYPOINT) stats

# === CLEANUP ===
clean:
	rm -rf build $(DIST_DIR) *.spec __pycache__ .pytest_cache

purge: clean
	rm -rf $(VENV_DIR)

# === INSTALL TO PATH ===
install-bin:
	@echo "📦 Installing keytally to $(INSTALL_DIR)"
	cp -r $(DIST_DIR)/$(APP_NAME) $(INSTALL_PARENT_DIR)/
	@echo "✓ Installed $(APP_NAME) to $(INSTALL_DIR)"

update-bin:
	@echo "📦 Removing existing keytally in $(INSTALL_DIR)"
	rm -rf $(INSTALL_DIR)
	@echo "📦 Installing keytally to $(INSTALL_DIR)"
	cp -r $(DIST_DIR)/$(APP_NAME) $(INSTALL_PARENT_DIR)/
	@echo "✓ Installed $(APP_NAME) to $(INSTALL_DIR)"

# === SYMLINK FOR GLOBAL USAGE ===
link-bin:
	@echo "🔗 Creating symlink at $(LINK_PATH)"
	ln -sf $(INSTALL_DIR)/$(APP_NAME) $(LINK_PATH)
	@echo "✓ Now you can run 'kt' from anywhere."

unlink-bin:
	@echo "🧹 Removing symlink at $(LINK_PATH)"
	rm -f $(LINK_PATH)
