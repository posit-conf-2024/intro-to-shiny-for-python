.PHONY: clean render preview prerender html docs slds publish exer all

SITE := _site
SLIDES_DIR := slides
DOCS_DIR := docs
SITE_SLIDES := $(SITE)/$(SLIDES_DIR)
SITE_DOCS := $(SITE)/$(DOCS_DIR)

clean:
	find docs/exercises -type f -name '*.html' -exec rm -f {} +
	find docs/exercises -type f -name '*.ipynb' -exec rm -f {} +
	find docs/exercises -type d -name '*_files' -exec rm -rf {} +
	find . -type f -name '*.Identifier' -exec rm -rf {} +
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -type d -name '.jupyter_cache' -exec rm -rf {} +


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


# Rule to build index.html files in subfolders of docs/exercises
EXERCISE_DIRS := $(wildcard docs/exercises/*)
EXERCISE_QMD := $(foreach dir,$(EXERCISE_DIRS),$(wildcard $(dir)/index.qmd))
EXERCISE_HTML := $(patsubst docs/exercises/%,_site/docs/exercises/%,$(EXERCISE_QMD:.qmd=.html))

exer: $(EXERCISE_HTML)

# Include files in the problems subfolder as dependencies
$(EXERCISE_HTML): _site/docs/exercises/%/index.html: docs/exercises/%/index.qmd $(wildcard docs/exercises/%/problems/*)
# @echo "Files that will change: $@ and $(patsubst _site/docs/exercises/%,docs/exercises/%,$(@:.html=.qmd))"
	quarto render $(patsubst _site/docs/exercises/%,docs/exercises/%,$(@:.html=.qmd)) --log-level $(LOG_LEVEL)
