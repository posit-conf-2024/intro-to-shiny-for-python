import glob
import os
import subprocess

# A simple makefile alternative to build docs/apps and docs/exercises
# It was too difficult to create a working makefile.
def update(type):
  g = f"docs/{type}/**/index.qmd"
  qmd_files = sorted(glob.glob(g, recursive=True))
  n = 0
  for qmd in qmd_files:
    html = qmd.replace('index.qmd', 'index.html').replace(f"docs/{type}", f"_site/docs/{type}")
    folder = os.path.dirname(qmd)
    children = glob.glob(f'{folder}/problem/*', recursive=True)
    deps = []
    deps.append(qmd)
    for child in children:
      deps.append(child)
    ts = [os.path.getmtime(dep) for dep in deps]
    recent = max(ts)
    if not os.path.exists(html):
      n += 1
      print(f"=== {html} does not exist ===")
      subprocess.run(['quarto', 'render', qmd, '--log-level=warning'])
    else:
      ts_htm = os.path.getmtime(html)
      if recent > ts_htm:
        n += 1
        print(f"=== {html} is out of date ===")
        subprocess.run(['quarto', 'render', qmd, '--log-level=warning'])
  return n

if __name__ == '__main__':
  n = update("exercises")
  if (n == 0):
    print("All exercises to update.")

  n = update("apps")
  if (n == 0):
    print("All apps to update.")
