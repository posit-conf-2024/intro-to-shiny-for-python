from pathlib import Path
import glob
import tempfile
import shutil
import os
import json


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


def list_files(path: str) -> list:
    files = glob.glob(path + "/**", recursive=True)
    files = [file for file in files if not glob.os.path.isdir(file)]
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


def _include_shiny_folder(
    path: str,
    file_name: str = "app.py",
    exclusions: list = [],
    # components: str = "editor, viewer, terminal",
    components: str = "editor, viewer",
    viewer_height: str = "800",
    extra_object: any = "",
) -> QuartoPrint:
    folder_path = Path(__name__).parent / path

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
    block.append_file(folder_path / file_name, None)

    exclude_list = ["__pycache__"] + [file_name] + exclusions

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
    out = [
        "",
        '::: {.callout-note collapse="false"}',
        "## Exercise",
        prompt,
        ":::",
        "",
    ]
    return out


def parse_readme(path: str) -> str:
    file_path = Path(__name__).parent / path / "README"
    file_contents = ""
    with open(file_path, "r") as file:
        file_contents = file.read()
    return file_contents

def problem_tabs_core(folder_name:str) -> None:
    return problem_tabs(folder_name, express=False)

def problem_tabs_express(folder_name:str) -> None:
    return problem_tabs(folder_name, express=True)

def problem_tabs(folder_name: str, express = False) -> None:

    import os

    def find_problem_set_folder(base_path, target_path, express = False):
        base_path = Path(base_path)
        secondary_path = "express" if express else "core"
        search_path = Path(base_path)/secondary_path
        for root, dirs, files in os.walk(search_path):
            for name in dirs:
                full_path = os.path.join(root, name)
                if target_path in full_path:
                    return full_path
        raise FileNotFoundError(
            f"Folder matching path '{target_path}' not found in '{search_path}'."
        )

    if (express):
        path = find_problem_set_folder("apps", folder_name, express=True)
    else:
        path = find_problem_set_folder("apps", folder_name, express = False)

    formatted_title = "## " + folder_name.replace("-", " ").title()

    block = QuartoPrint(
        [
            formatted_title,
            "::::: {.column-screen-inset}",
            "::: {.panel-tabset}",
            "## Goal",
        ]
    )
    prompt = parse_readme(path)
    block.extend(collapse_prompt(prompt))
    block.extend(
        _include_shiny_folder(
            path,
            "app-solution.py",
            exclusions=["app.py", "README"],
            components="viewer",
        )
    )
    block.append("## Problem")
    block.extend(collapse_prompt(prompt))
    block.extend(
        _include_shiny_folder(
            path, 
            "app.py", 
            exclusions=["app-solution.py", "README"]
        )
    )
    block.append("## Solution")
    block.extend(collapse_prompt(prompt))
    block.extend(
        _include_shiny_folder(
            path, 
            "app-solution.py", 
            exclusions=["app.py", "README"]
        )
    )
    block.append("## {{< bi github >}}")
    block.append(
        f"The source code for this exercise is [here]"
        f"(https://github.com/posit-conf-2024/intro-to-shiny-for-python/tree/main/{path})."
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
    shutil.copy("apps/utilities/multiple-choice/app.py", temp_dir)
    with open(os.path.join(temp_dir, "questions.json"), "w") as file:
        json.dump(questions, file)

    print("::: callout-note")
    print("## Test your understanding")
    include_shiny_folder(temp_dir, components="viewer", viewer_height="250")
    print(":::")
