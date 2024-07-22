clean:
	find exercises -type f -name '*.html' -exec rm -f {} +
	find exercises -type f -name '*.ipynb' -exec rm -f {} +

render:
	quarto render

preview:
	quarto preview --port 4096