# Py-File-Deleter
Python small utility that removes files in a given list or folder

This Python 3.x CLI script was made to remove files, given either a list of their paths or a folder path containing them.

## Parameters

```
usage: file_deleter.py [-h] {files,folder} ...

options:
   -h, --help      show this help message and exit

Deletion mode:
  The following are valid deletion modes:

  {files,folder}
    files         Delete a list of files
    folder        Delete files from a specified folder

--------------------------------------------------------------------------

usage: file_deleter.py files [-h] file_list

positional arguments:
  file_list   The list of files to be deleted (mandatory)

options:
  -h, --help  show this help message and exit

--------------------------------------------------------------------------

usage: file_deleter.py folder [-h] [-w WILDCARD] [-X] folder

positional arguments:
  folder                The folder where the to-be deleted files are
                        (mandatory)

options:
  -h, --help            show this help message and exit
  -w WILDCARD, --wildcard WILDCARD
                        A wildcard specifying which files to delete (default:
                        ALL)
  -X, --delete-folder   A flag to determine if the input folder will also be
                        deleted (default: false)
```

## How to use

1. Download the contents of the repository to an empty folder of your choice.
2. Run the following commands:

   ```
   $ python -m venv env
   $ source env/bin/activate   # If you're on Linux, or
   > .\env\Scripts\activate    # If you're on Windows
   $ python -m pip install -r requirements.txt
   ```

   This will install PyInstaller, to be able to generate a binary executable.
3. (Optional) Run the following command to create a binary executable:

   ```
   $ pyinstaller -F file_deleter.py
   ```

   The result will be in the `dist` directory.
