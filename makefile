.PHONY: clean render preview prerender html

SITE := _site
SLIDES_DIR := slides
DOCS_DIR := docs
SITE_SLIDES := $(SITE)/$(SLIDES_DIR)
SITE_DOCS := $(SITE)/$(DOCS_DIR)

clean:
	find exercises -type f -name '*.html' -exec rm -f {} +
	find exercises -type f -name '*.ipynb' -exec rm -f {} +
	find exercises -type d -name '*_files' -exec rm -rf {} +
	find . -type f -name '*Zone.Identifier' -exec rm -rf {} +
	find . -type d -name '__pycache__' -exec rm -rf {} +


render:
	quarto render

preview:
	quarto preview --port 4096

prerender:
	quarto preview --render html --port 4096


LOG_LEVEL := warning
LOG_LEVEL := info

# Define lists of .qmd files recursively in the docs folder
QMD_FILES := $(shell find $(DOCS_DIR) -type f -name '*.qmd' ! -name '_*.qmd')

# Define corresponding .html files
HTML_FILES := $(patsubst $(DOCS_DIR)/%.qmd,$(SITE_DOCS)/%.html,$(QMD_FILES))

# Existing pattern rules for generating .html from .qmd
$(SITE_DOCS)/%.html: $(DOCS_DIR)/%.qmd
	quarto render $< --log-level $(LOG_LEVEL)

# New target to generate all .html files
html: $(HTML_FILES)