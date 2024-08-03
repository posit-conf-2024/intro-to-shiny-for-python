
import pytest
import os
import glob

def find_python_files_without_import(directory):
  search_shiny = 'from shiny import'
  search_express = 'from shiny.express import'
  exclude_folder = os.path.join(directory, "helpers")
  n_errors = 0
  n_files = 0
  to_fix = []
  py_files = glob.glob(os.path.join(directory, '**', '*.py'), recursive=True)
  py_files.sort()
  for name in py_files:
    if exclude_folder in name:
      continue
    n_files += 1
    if 'app-core.py' in name or 'app_core.py' in name or 'app-solution-core.py' in name:
      continue
    with open(name, 'r') as f:
      content = f.read()
      if search_shiny in content and search_express not in content:
        n_errors += 1
        to_fix.append(name)
        # print(name)
  return n_errors, n_files, to_fix

# def check_express():
#   directory = 'docs/exercises'
#   print("=== checking for app.py files that use shiny core without express ===")
#   find_python_files_without_import('docs/exercises')
#   find_python_files_without_import('docs/apps')




def test_exercises():
    errors, n_files, to_fix = find_python_files_without_import('docs/exercises')
    if errors != 0:
        print(f"To fix: {to_fix}")  
    assert n_files > 0 and errors == 0, f"Found files that use shiny core without express: {to_fix}"

def test_apps():
    errors, n_files, to_fix = find_python_files_without_import('docs/apps')
    if errors != 0:
        print(f"To fix: {to_fix}")  
    assert n_files > 0, "No files found"
    assert errors == 0 , "Found files that use shiny core without express"


