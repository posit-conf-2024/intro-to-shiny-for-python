from pathlib import Path
import glob
import tempfile
import shutil
import os
import json
import re


class QuartoPrint(list):
    def __init__(self, data):
        super().__init__(data)

    def __str__(self):
        return "\n".join(str(item) for item in self)

    def append_file(self, file_path: str, file_name: str = None):
        if file_name is not None:
            self.append(f"## file: {file_name}")

        with open(file_path, "r") as app_file:
            app_contents = app_file.read()
            self.append(app_contents)


def getcwd() -> str:
    current =  os.getcwd()
    # relative = os.path.relpath(current)
    # return os.path.dirname(relative)
    ptn = ("^.*/docs/(.*)$")
    match = re.match(ptn, current)
    if match:
        folder = match.group(1)
    else:
        folder = current
    return folder

def list_files(path: str = "") -> list:
    files = glob.glob("*.*", recursive=True)
    files = [file for file in files if not glob.os.path.isdir(file)]
    exclusions = ["index.qmd", "index.quarto_ipynb"]
    files = [file for file in files if not any(exclusion in file for exclusion in exclusions)]
    return files


def include_shiny_folder(
    path: str,
    file_name: str = "app.py",
    exclusions: list = [],
    components: str = "editor, viewer",
    viewer_height: str = "800",
    extra_object: any = "",
) -> None:
    print(
        _include_shiny_folder(
            path, file_name, exclusions, components, viewer_height, extra_object
        )
    )

def print_cwd(path: str):
    # ptn = ("^.*/(docs/.*)$")
    # match = re.match(ptn, path)
    # if match:
    #     folder = match.group(1)
    # else:
    #     folder = "not found"
    block =  QuartoPrint("")
    block.append(path)
    print(block)

def _include_shiny_folder(
    path: str = "",
    file_name: str = "app.py",
    exclusions: list = [],
    # components: str = "editor, viewer, terminal",
    components: str = "editor, viewer",
    viewer_height: str = "800",
    extra_object: any = "",
) -> QuartoPrint:
    # folder_path = Path(__name__).parent / path
    folder_path = path

    additional_exclude = ['app-core.py', 'app-solution-core.py']

    # Start with the header
    block = QuartoPrint(
        [
            "```{shinylive-python}",
            "#| standalone: true",
            f"#| components: [{components}]",
            "#| layout: horizontal",
            f"#| viewerHeight: {viewer_height}",
        ]
    )

    # Print contents of the main application
    # block.append_file(folder_path / file_name, None)
    block.append_file(file_name, None)

    exclude_list = ["__pycache__"] + [file_name] + exclusions + additional_exclude

    files = list_files(path)

    path_list = [
        string
        for string in files
        if not any(exclusion in string for exclusion in exclude_list)
    ]

    file_names = [string.replace(f"{str(folder_path)}/", "") for string in path_list]

    # Additional files need to start with ## file:
    for x, y in zip(path_list, file_names):
        block.append_file(x, y)

    # Finish with the closing tag
    block.append("```")
    return block


def collapse_prompt(prompt: str) -> list:
    return [
        "",
        '::: {.callout-important collapse="false"}',
        "## Instructions",
        prompt,
        ":::",
        "",
    ]


def parse_readme(path: str) -> str:
    # file_path = Path(__name__).parent / path / "README"
    file_path = os.path.join(path, "README")
    file_path = "README"
    file_contents = ""
    with open(file_path, "r") as file:
        file_contents = file.read()
    return file_contents

def problem_app_express(folder_name) -> None:
    problem_tabs_express(folder_name, app=True)


# Inserts problem tab (goal, problem, solution) into the document as markdown
#
# Parameters:
#    - folder_name:  relative folder path
#    - app: If True, expects an app (app.py) and if False, expects a problem (app.py and app-solution.py)
def problem_tabs_express(
        folder_name:str = "", 
        app:bool = False,
        viewer_height:str="800",
        app_exclusions:list = [],
        sol_exclusions:list = [],
    ) -> None:
    # path = os.path.basename(folder_name)
    # path = os.path.join(path, "problem")
    # path = "problem"
    path = ""


    app_exclusions = ["app-solution.py", "README"] + app_exclusions
    sol_exclusions = ["app.py", "README"] + sol_exclusions

    
    # prompt = parse_readme("problem")
    prompt = parse_readme("")

    if prompt == "":
        block = QuartoPrint("")
    else:
        block = QuartoPrint(
                collapse_prompt(prompt)
        )
    block.extend(
        [
            "",
            "::::: {.column-screen-inset}",
            "::: {.panel-tabset}",
        ]
    )

    #---- Goal -------------------------------
    if not app:
        block.append( "## Goal")
        block.extend(
            _include_shiny_folder(
                path,
                "app-solution.py",
                exclusions=["app.py", "README"],
                components="viewer",
                viewer_height=viewer_height
            )
        )
        block.append("## Problem")
        block.extend(
            _include_shiny_folder(
                path, 
                "app.py", 
                exclusions=app_exclusions,
                viewer_height=viewer_height
            )
        )
    else:
        block.append("## App")
        block.extend(
            _include_shiny_folder(
                path, 
                "app.py", 
                exclusions=["app-solution.py", "README"],
                components="viewer",
                viewer_height=viewer_height

            )
        )
    if not app:
        block.append("## Solution")
        block.extend(
            _include_shiny_folder(
                path, 
                "app-solution.py", 
                exclusions=sol_exclusions,
                viewer_height=viewer_height
            )
        )
    else:
        block.append("## Edit this app")
        block.extend(
            _include_shiny_folder(
                path, 
                "app.py", 
                exclusions=["app.py", "README"],
                viewer_height=viewer_height
            )
        )

    block.append("## {{< bi github >}}")

    if app:
        # github_path = os.path.join("docs", folder_name, "problem")
        github_path = os.path.join("docs", folder_name)
    else:
        # github_path = os.path.join("docs", folder_name, "problem")
        github_path = os.path.join("docs", folder_name)
    block.append(
        f"The source code for this exercise is at "
        f"<https://github.com/posit-conf-2024/intro-to-shiny-for-python/tree/main/{github_path}>."
    )

    block.append(":::")
    block.append(":::::")
    print(block)


class Quiz(dict):
    def __init__(self, data):
        super().__init__(data)
        self.validate()

    def validate(self):
        if not isinstance(self, dict):
            raise ValueError("Invalid data format: The data should be a dictionary.")
        for key, value in self.items():
            if not isinstance(value, dict):
                raise ValueError(
                    f"Invalid data format for '{key}': The value should be a dictionary."
                )
            if "choices" not in value or "answer" not in value:
                raise ValueError(
                    f"Invalid data format for '{key}': Missing 'choices' or 'answer' key."
                )
            if not isinstance(value["choices"], list) or not all(
                isinstance(choice, str) for choice in value["choices"]
            ):
                raise ValueError(
                    f"Invalid data format for '{key}': 'choices' should be a list of strings."
                )
            if not isinstance(value["answer"], str):
                raise ValueError(
                    f"Invalid data format for '{key}': 'answer' should be a string."
                )
            if value["answer"] not in value["choices"]:
                raise ValueError(
                    f"Invalid data format for '{key}': '{value['answer']}' is not one of the choices."
                )

        return True


def multiple_choice_app(questions: Quiz):
    questions = Quiz(questions)
    temp_dir = tempfile.mkdtemp("temp_folder")

    # Get the directory of the current file (helpers.py)
    current_dir = os.path.dirname(__file__)
    # Construct the path to app.py assuming it's in the same directory as helpers.py
    app_path = os.path.join(current_dir, "multiple_choice/app.py")
    # Copy app.py directly to the temporary directory
    shutil.copy(app_path, os.path.join(temp_dir, "app.py"))

    with open(os.path.join(temp_dir, "questions.json"), "w") as file:
        json.dump(questions, file)

    print("::: callout-note")
    print("## Test your understanding")
    include_shiny_folder(temp_dir, components="viewer", viewer_height="250")
    print(":::")
