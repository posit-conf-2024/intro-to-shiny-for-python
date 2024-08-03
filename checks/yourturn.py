import os
import re

# Check for .qmd files that reference `yourturn` exercises that do not exist

def check_yourturn(file, regex, root_path, print_names=False):
  n_matches = 0
  n_correct = 0
  with open(file, 'r', encoding='utf-8') as f:
    for line_number, line in enumerate(f, start=1):
      match = re.search(regex, line)
      if match:
        n_matches += 1
        expected = match.group(1)
        folder_path = os.path.join(root_path, expected)
        folder_path = re.sub("^../", "", folder_path)
        if os.path.isdir(folder_path):
            if print_names:
                print(f"{file}:{line_number} := {expected}")
            n_correct += 1
        else:
            print(f"{file}:{line_number} := {expected} (Folder does not exist)")
            print(f"folder_path: {folder_path}")
  return n_matches, n_correct            


# Walk through the docs folder
def walk_dir(fn, regex, root_path, print_names=False):
  n_files = 0
  n_matches = 0
  n_correct = 0
  for root, dirs, files in os.walk(docs_dir):
    for file in files:
      if file.endswith('.qmd'):
        n_files += 1
        file_path = os.path.join(root, file)
        new_matches, new_correct = fn(file_path, regex, root_path, print_names)
        n_matches += new_matches
        n_correct += new_correct
  return n_files, n_matches, n_correct

def print_result(n_files, n_matches, n_correct):
  print(f"Total files checked: {n_files} with {n_matches} matches and {n_correct} correct.")
  print()

def main():

  regex = "{{< yourturn '(.*?)' .*>}}"
  print(f"=== regex: {regex} ===")
  n_files, n_matches, n_correct = walk_dir(check_yourturn, regex, "docs/exercises", print_names=False)
  print_result(n_files, n_matches, n_correct)
  
  regex = '"apps/(.*?)"'
  print(f"=== regex: {regex} ===")
  n_files, n_matches, n_correct = walk_dir(check_yourturn, regex, "docs/apps/", print_names=True)
  print_result(n_files, n_matches, n_correct)

  regex = '"../apps/examples/(.*?)"'
  print(f"=== regex: {regex} ===")
  n_files, n_matches, n_correct = walk_dir(check_yourturn, regex, "../apps/examples", print_names=True)
  print_result(n_files, n_matches, n_correct)

  regex = '"../apps/core/(.*?)"'
  print(f"=== regex: {regex} ===")
  n_files, n_matches, n_correct = walk_dir(check_yourturn, regex, "../apps/core", print_names=True)
  print_result(n_files, n_matches, n_correct)

docs_dir = 'docs'
if __name__ == '__main__':
  main()