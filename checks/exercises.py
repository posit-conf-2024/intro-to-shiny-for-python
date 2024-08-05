import os
import re
import sys

def walk_dir():
  dirs = os.listdir(docs_dir)
  # remove dirs that start with _
  dirs = [dir for dir in dirs if not dir.startswith('_')]
  ptn = ".*?-(\d+)-.*"
  n_changed = 0
  for dir in dirs:
    match = re.search(ptn, dir)
    if match:
      number = match.group(1)
      index_path = os.path.join(docs_dir, dir, 'index.qmd')
      if os.path.isfile(index_path):
        changed = False
        with open(index_path, 'r', encoding='utf-8') as f:
          content = f.readlines()
          title_line = content[1]
          match = re.search('[Tt]itle: "(\d+ )*(.*)"', title_line)
          # print(f"Match: {match}")
          if match:
            title = match.group(2)
            # print(f"Title: {title}")
            new_content = f'title: "{number} {title}"\n'
            if title_line != new_content:
              content[1] = new_content
              changed = True
              n_changed += 1
              print(f"New contents: {new_content}")
              print(f"Dir: {dir}, number: {number}")
              print(f"Contents of {index_path}: {title_line}")
              print(f"New content: {new_content}")
        if changed:
          with open(index_path, 'w', encoding='utf-8') as f:
            f.writelines(content)
  if n_changed > 0:
    print(f"Changed {n_changed} files.")
  else:
    print("=== exercises.py ===")
    print("No files changed.")



docs_dir = 'docs/exercises'
if __name__ == '__main__':
  walk_dir()