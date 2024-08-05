import os
import sys
import re

# Read _quarto.yml file and search for the pattern '*.qmd'
# Then check if the file exists

def main():
  print()
  print("=== quarto_yml.py ===")
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
            print(f"In '_quarto.yml' on line {line_number}: Ref to {qmd} that doesn't exist")
            n_not_exists += 1
  if n_not_exists == 0:
    print("All references to `*.qmd` exist in _quarto.yml.")
    print()
  else:
    print()
