from checks import yourturn
from checks import exercises
from checks import quarto_yml

yourturn.main()
exercises.walk_dir()
quarto_yml.main()
# express.check_express()

from tests import test_express
errors, files, names = test_express.find_python_files_without_import('docs/exercises') 
if errors != 0:
    for name in names:
        print(name)

errors, files, names = test_express.find_python_files_without_import('docs/apps') 
if errors != 0:
    for name in names:
        print(name)

from checks import summary
summary.write_csv_summary()
  
   