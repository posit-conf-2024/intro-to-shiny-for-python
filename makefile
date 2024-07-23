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

# Define lists of .qmd files
DOCS_QMD_FILES := $(wildcard $(DOCS_DIR)/*.qmd)
SLIDES_QMD_FILES := $(wildcard $(SLIDES_DIR)/*.qmd)

# Define corresponding .html files
DOCS_HTML_FILES := $(patsubst $(DOCS_DIR)/%.qmd,$(SITE_DOCS)/%.html,$(DOCS_QMD_FILES))
SLIDES_HTML_FILES := $(patsubst $(SLIDES_DIR)/%.qmd,$(SITE_SLIDES)/%.html,$(SLIDES_QMD_FILES))

# Existing pattern rules for generating .html from .qmd
$(SITE_DOCS)/%.html: $(DOCS_DIR)/%.qmd
	quarto render $< --log-level $(LOG_LEVEL)

$(SITE_SLIDES)/%.html: $(SLIDES_DIR)/%.qmd
	quarto render $< --log-level $(LOG_LEVEL)

# New target to generate all .html files
html: $(DOCS_HTML_FILES) $(SLIDES_HTML_FILES)