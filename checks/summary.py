import os
import glob
import re
import csv

def get_dirname(folder):
    return os.path.basename(folder)

def get_title(file):
    with open(file, 'r') as f:
        lines =  f.readlines()
        ptn = '^title: "(.+?)".*$'
        match = re.search(ptn, lines[1])
        if match:
            return match.group(1)
        else:
          return "No title found"
        
def get_readme(file):
    with open(file, 'r') as f:
        return f.read().strip()
    
def get_app_type(file):
    with open(file, 'r') as f:
        lines = f.read()
        if re.search('[Ww]eather', lines):
            return 'weather'
        elif re.search('penguins', lines):
            return 'penguins'
        elif re.search('[Aa]ccount', lines):
            return 'account'
        else:
           return 'other'

def get_shiny_express(file):
    with open(file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if re.search('shiny.express', line):
                return True
        return False

# walk the root folder and extract information into a dictionary
# - folder name
# - title contained in folder/index.qmd
# - contents of folder/problems/readme
# - whether folder/problems/app.py uses shiny express or not
# - whether folder/problems/app-solution.py uses shiny express or not
# - whether folder/problems/app.py refers to penguins, weather or accounts
def summary(root = 'docs/exercises'):
  # list the top-level directories and files
  z = []
  for entry in sorted(os.listdir(root)):
    entry_path = os.path.join(root, entry)
    if os.path.isdir(entry_path):
      # process the directory
      # print(f'Directory: {get_dirname(entry_path)}')
      for file in os.listdir(entry_path):
        file_path = os.path.join(entry_path, file)
        if 'index.qmd' in file_path:
          # extract exercise title
          title = get_title(file_path)
          # print(f' - Title: {title}')
        if 'problem' in file_path:
          # print(f' - {file_path}')

          # extract readme contents
          readme_file = os.path.join(file_path, 'README')
          readme = get_readme(readme_file)
          # print(f' - Readme: {readme}')

          # extract application type
          app_file = os.path.join(file_path, 'app-solution.py')
          if os.path.exists(app_file):
            app_type = get_app_type(app_file)
            shiny_express = get_shiny_express(app_file)
          else:
            app_type = None
            shiny_express = None
          # print(f' - App type: {app_type}')

          # extract shiny express usage

          z.append(
            {
              'root': root,
              'folder': get_dirname(entry_path), 
              'title': title, 
              'app_type': app_type, 
              'shiny_express': shiny_express,
              'readme': readme, 
            }
          )
  return z


def write_csv_summary():
  r_docs = summary('docs/exercises')
  r_apps = summary('docs/apps')
  r_docs.extend(r_apps)

  # print(r_docs)

  csv_file = 'results.csv'
  with open(csv_file, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['root', 'folder', 'title', 'app_type', 'shiny_express', 'readme'])
    writer.writeheader()
    writer.writerows(r_docs)
  
  print(f'Wrote results to {csv_file}')
