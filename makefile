.PHONY: clean render preview prerender html docs slds publish exer apps all check

SITE := _site
SLIDES_DIR := slides
DOCS_DIR := docs
SITE_SLIDES := $(SITE)/$(SLIDES_DIR)
SITE_DOCS := $(SITE)/$(DOCS_DIR)

clean:
	@find docs/exercises -type f -name '*.html' -exec rm -f {} +
	@find docs/exercises -type f -name '*.ipynb' -exec rm -f {} +
	@find docs/exercises -type d -name '*_files' -exec rm -rf {} +
	@find . -type f -name '*.Identifier' -exec rm -rf {} +
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type d -name '.jupyter_cache' -exec rm -rf {} +


render:
	quarto render

preview:
	quarto preview --port 4096

prerender:
	quarto preview --render html --port 4096


LOG_LEVEL := warning
LOG_LEVEL := info

# Define lists of .qmd files recursively in the docs folder
DOC_QMD := $(shell find $(DOCS_DIR) -maxdepth 1 -type f -name '*.qmd' ! -name '_*.qmd' ! -name '*-slides.qmd')
SLD_QMD := $(shell find $(DOCS_DIR) -maxdepth 1 -type f -name '*-slides.qmd' ! -name '_*.qmd')


# Define corresponding .html files
DOC_HTML := $(patsubst $(DOCS_DIR)/%.qmd, $(SITE_DOCS)/%.html, $(DOC_QMD))
SLD_HTML := $(patsubst $(DOCS_DIR)/%.qmd, $(SITE_DOCS)/%.html, $(SLD_QMD))

docs: $(DOC_HTML)

slds: $(SLD_HTML)

# Rule to build DOC_HTML
$(SITE_DOCS)/%.html: $(DOCS_DIR)/%.qmd _quarto.yml
	quarto render $< --log-level $(LOG_LEVEL)

# Rule to build SLD_HTML
$(SITE_SLDS)/%.html: $(SLDS_DIR)/%.qmd _quarto.yml
	quarto render $< --log-level $(LOG_LEVEL)

index: $(SITE)/index.html

$(SITE)/index.html: index.qmd _quarto.yml
	quarto render index.qmd --log-level $(LOG_LEVEL)


# New target to generate all .html files
html: index docs slds

publish:
	quarto publish gh-pages --no-render --no-prompt

all: html exer clean

exer:
	python make.py

check:
	python check.py

test:
	quarto render index.qmd --log-level warning
	quarto render docs/exercises/101-run-app --log-level warning
	quarto render docs/test.qmd --log-level warning
	quarto render docs/test-slides.qmd --log-level warning