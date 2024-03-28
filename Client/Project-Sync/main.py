import functions
import config

while True:
    files = functions.file_system.indexer(config.synthDetails.header_dir())
    fileContent = functions.file_system.fileRead(f"")