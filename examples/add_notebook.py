#!/usr/bin/env python
""" file:   add_notebook.py
    author: Someone on StackOverflow
            see http://stackoverflow.com/questions/18734739

    description: Utility script to clean the output from an IPython notebook
        prior to adding it into the Git repository. This lets us put them in
        for version control without having large files uploaded when the
        output changes.
"""

from IPython.nbformat import current
import io
from os import remove, rename
from shutil import copyfile
from subprocess import Popen
from sys import argv

for filename in argv[1:]:
    # Backup the current file
    backup_filename = filename + ".backup"
    copyfile(filename, backup_filename)

    try:
        # Read in the notebook
        with io.open(filename, 'r', encoding='utf-8') as f:
            notebook = current.reads(f.read(), format="ipynb")

        # Strip out all of the output and prompt_number sections
        for worksheet in notebook["worksheets"]:
            for cell in worksheet["cells"]:
                cell.outputs = []
                if "prompt_number" in cell:
                    del cell["prompt_number"]

        # Write the stripped file
        with io.open(filename, 'w', encoding='utf-8') as f:
            current.write(notebook, f, format='ipynb')

        # Run git add to stage the non-output changes
        print("git add", filename)
        Popen(["git", "add", filename]).wait()

    finally:
        # Restore the original file;  remove is needed in case
        # we are running in windows.
        remove(filename)
        rename(backup_filename, filename)
