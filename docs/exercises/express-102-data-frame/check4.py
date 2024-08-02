
import sys
import os

print(os.getcwd())

helpers_path = "docs/exercises"
if helpers_path not in sys.path:
    sys.path.append(helpers_path)
from helpers import problem_tabs_express, getcwd

print(getcwd())

# print(
#     problem_tabs_express(getcwd())
# )