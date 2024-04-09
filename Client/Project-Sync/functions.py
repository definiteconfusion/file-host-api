import yaml


class file_system:
    @staticmethod
    def indexer(directory):
        pysyncFiles = ["Project-Sync/config.py", "Project-Sync/functions.py", "Project-Sync/main.py", "Project-Sync/playground.py", "Project-Sync/setup.yaml"]
        storageFiles = ["__pycache__", ".DS_Store 2", ".DS_Store"]
        ignoredSuffixs = config.basic.details()[".ignore"] + pysyncFiles + storageFiles
        fileList = []
        for files in os.listdir(directory):
            fileList.append(files)
        return [value for value in fileList if not any(value.endswith(suffix) for suffix in ignoredSuffixs)]

    @staticmethod
    def fileRead(file_path):
        try:
            with open(file_path, 'r') as file:
                file_content = file.read()
            return file_content
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
            return None
        except IsADirectoryError:
            return None
def fileDictCompare(currDict: dict, lastDict: dict):
    for keys in currDict:
        try:
            lastDict[keys]
        except KeyError:
            click.echo("Detected New File Present -> Uploading to pySync")
            return True
    for keys in lastDict:
        try:
            currDict[keys]
        except KeyError:
            click.echo("Detected File Deletion -> Uploading to pySync")
            return True
    for keys in lastDict:
        if currDict[keys] != lastDict[keys]:
            click.echo(f"Detected File Change in {click.style(keys, bg='red')} -> Uploading to pySync")
            return True
    # click.echo(f"No changes detected -> Breaking")

def fileRead(file_path):
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
        return file_content
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None

def zipper(file_list: list, name: str):
    directory_path = config.synthDetails.header_dir()
    zip_name = name
    with ZipFile(zip_name, 'w') as zipf:
        for item in file_list:
            file_path = os.path.join(directory_path, item)
            if os.path.isfile(file_path):  # Check if it's a file
                with open(file_path, 'rb') as file:
                    zipf.write(file_path, os.path.relpath(file_path, directory_path))
            elif os.path.isdir(file_path):  # Check if it's a directory
                for dirpath, dirnames, filenames in os.walk(file_path):
                    for filename in filenames:
                        file_in_dir = os.path.join(dirpath, filename)
                        if os.path.relpath(file_in_dir, directory_path) in file_list:
                            with open(file_in_dir, 'rb') as file:
                                zipf.write(file_in_dir, os.path.relpath(file_in_dir, directory_path, "Project-Sync/"))
    print(f"Added {len(file_list)} to {name}")
    return zip_name

def serverSync(files:list):
    zipper(files, "pack.zip")
    return True

def setup():
    yamlData = config.basic.details()["setupYaml"]
    if yamlData["project-isInit"] == "False":
        projectNamePrompt = click.prompt("Project Name: ")
        yamlData["project-isInit"] = "True"; yamlData["project-title"] = projectNamePrompt
        file_path = "./setup.yaml"
        with open(file_path, 'w') as file:
            yaml.dump(yamlData, file, default_flow_style=False, Dumper=yaml.Dumper)
    pass

# serverSync(["exampletest.txt"])

import config
import os
from zipfile import ZipFile
import click

