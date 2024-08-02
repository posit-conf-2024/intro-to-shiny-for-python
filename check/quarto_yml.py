import os
import sys
import re

# Open the _quarto.yml file and search for the pattern '*.qmd'

def main():
  ptn = '.* (.*?.qmd)'
  file = './_quarto.yml'
  n_not_exists = 0
  with open(file, 'r', encoding='utf-8') as f:
    for line_number, line in enumerate(f, start=1):
        # print(line)
        match = re.search(ptn, line)
        if match:
          qmd = match.group(1)
          exists = os.path.exists(qmd)
          if not exists:
            print(f"Line {line_number}: {qmd} - {exists}")
            n_not_exists += 1
  if n_not_exists == 0:
    print("=== quarto_yml.py ===")
    print("All references to `*.qmd` exist in _quarto.yml.")
