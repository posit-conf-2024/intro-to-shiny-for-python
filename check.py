# import check
from checks import yourturn
from checks import exercises
from checks import quarto_yml
from checks import express

yourturn.main()
exercises.walk_dir()
quarto_yml.main()
express.check_express()