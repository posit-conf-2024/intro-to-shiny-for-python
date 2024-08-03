
import os
import glob

def find_python_files_without_import(directory):
  search_shiny = 'from shiny import'
  search_express = 'from shiny.express import'
  exclude_folder = os.path.join(directory, "helpers")
  for root, dirs, files in os.walk(directory):
    if exclude_folder in root:
      continue
    for file in glob.glob(os.path.join(root, '*.py')):
      if 'app-core.py' in file or 'app_core.py' in file or 'app-solution-core.py' in file:
        continue
      with open(file, 'r') as f:
        content = f.read()
        if search_shiny in content and search_express not in content:
          print(file)

def check_express():
  directory = 'docs/exercises'
  print("=== checking for app.py files that use shiny core without express ===")
  find_python_files_without_import('docs/exercises')
  find_python_files_without_import('docs/apps')