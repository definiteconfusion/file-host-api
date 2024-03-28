import config
import os

class file_system:
    @staticmethod
    def indexer(directory):
        pysyncFiles = ["Project-Sync", "compiler.py", "config.py", "functions.py", "main.py", "config.json"]
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